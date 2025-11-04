"""Command-line entry point and pipeline orchestration for cough analysis."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import parselmouth

from src.analysis import features, preprocessing, spectral
from src.utils import audio_io


TARGET_SAMPLE_RATE = 16_000
FRAME_LENGTH = int(0.02 * TARGET_SAMPLE_RATE)  # 20 ms windows
HOP_LENGTH = int(0.01 * TARGET_SAMPLE_RATE)  # 10 ms hop
MIN_SEGMENT_DURATION = 0.1  # seconds
ENERGY_THRESHOLD_RATIO = 0.1  # relative to peak energy
SNR_THRESHOLD_DB = 10.0


@dataclass
class PipelineConfig:
	target_sample_rate: int = TARGET_SAMPLE_RATE
	frame_length: int = FRAME_LENGTH
	hop_length: int = HOP_LENGTH
	min_segment_duration: float = MIN_SEGMENT_DURATION
	energy_threshold_ratio: float = ENERGY_THRESHOLD_RATIO
	snr_threshold_db: float = SNR_THRESHOLD_DB


def _collect_audio_files(input_file: str | None, input_dir: str | None) -> list[Path]:
	"""Resolve and validate the set of input WAV files to process."""
	if input_file and input_dir:
		raise ValueError("Specify either --input-file or --input-dir, not both.")
	if not input_file and not input_dir:
		raise ValueError("You must provide --input-file or --input-dir.")

	if input_file:
		file_path = Path(input_file)
		if not file_path.exists():
			raise FileNotFoundError(f"Input file not found: {file_path}")
		return [file_path]

	directory = Path(input_dir)  # type: ignore[arg-type]
	if not directory.exists():
		raise FileNotFoundError(f"Input directory not found: {directory}")

	return sorted(p for p in directory.glob("**/*.wav") if p.is_file())


def _analyze_segment(
	segment_id: str,
	segment_signal: np.ndarray,
	config: PipelineConfig,
) -> dict[str, float | str]:
	"""Calculate all configured features for a normalized segment."""
	length_seconds = features.calculate_length(segment_signal, config.target_sample_rate)
	rms_energy = features.calculate_rms_energy(segment_signal)
	zcr = features.calculate_zcr(segment_signal)

	amplitude_contour = features.calculate_amplitude_contour(
		segment_signal, config.frame_length, config.hop_length
	)
	amplitude_mean = float(np.mean(amplitude_contour)) if amplitude_contour.size else 0.0

	band_limits = [(0, 400), (400, 800), (800, 1_600), (1_600, 3_200), (3_200, config.target_sample_rate // 2)]
	relative_energy = spectral.calculate_relative_energy(
		segment_signal, config.target_sample_rate, band_limits
	)

	praat_sound = parselmouth.Sound(segment_signal, sampling_frequency=config.target_sample_rate)
	vowel_features = features.analyze_vowel(praat_sound, config.target_sample_rate)

	record: dict[str, float | str] = {
		"segment_id": segment_id,
		"length": length_seconds,
		"rms_energy": float(rms_energy),
		"zcr": float(zcr),
		"amplitude_mean": amplitude_mean,
		"F0": vowel_features.get("F0", 0.0),
		"HNR": vowel_features.get("HNR", 0.0),
		"Jitter": vowel_features.get("Jitter", 0.0),
		"Shimmer": vowel_features.get("Shimmer", 0.0),
	}

	for idx, value in enumerate(relative_energy, start=1):
		record[f"relative_energy_band_{idx}"] = float(value)

	return record


def _process_file(
	audio_path: Path,
	output_dir: Path,
	config: PipelineConfig,
) -> Iterable[dict[str, float | str]]:
	"""Process a single input file and yield feature records for each segment."""
	signal, original_rate = audio_io.load_wav(str(audio_path))
	signal = preprocessing.downsample_signal(signal, original_rate, config.target_sample_rate)
	signal = preprocessing.normalize_energy(signal)

	frame_length = config.frame_length
	hop_length = config.hop_length

	dynamic_threshold = config.energy_threshold_ratio * float(np.max(np.abs(signal)) or 1.0)
	segments = preprocessing.segment_by_energy(
		signal,
		config.target_sample_rate,
		frame_length,
		hop_length,
		dynamic_threshold,
		config.min_segment_duration,
	)
	segments = preprocessing.filter_by_snr(signal, segments, config.snr_threshold_db)

	if not segments:
		return []

	segment_dir = output_dir / "segments"
	segment_dir.mkdir(parents=True, exist_ok=True)

	records: list[dict[str, float | str]] = []
	for index, (start, end) in enumerate(segments, start=1):
		segment_signal = preprocessing.normalize_energy(signal[start:end])
		segment_id = f"{audio_path.stem}_{index:02d}"

		segment_path = segment_dir / f"{segment_id}.wav"
		audio_io.save_wav(str(segment_path), segment_signal, config.target_sample_rate)

		record = _analyze_segment(segment_id, segment_signal, config)
		record["source_file"] = audio_path.name
		records.append(record)

	return records


def run_pipeline(
	*,
	input_file: str | None = None,
	input_dir: str | None = None,
	output_dir: str = "results",
	config: PipelineConfig | None = None,
) -> pd.DataFrame:
	"""Execute the cough analysis pipeline and return the feature table."""

	cfg = config or PipelineConfig()
	audio_paths = _collect_audio_files(input_file, input_dir)
	output_path = Path(output_dir)
	output_path.mkdir(parents=True, exist_ok=True)

	all_records: list[dict[str, float | str]] = []
	for audio_path in audio_paths:
		records = _process_file(audio_path, output_path, cfg)
		all_records.extend(records)

	if not all_records:
		columns = [
			"segment_id",
			"source_file",
			"length",
			"rms_energy",
			"zcr",
			"amplitude_mean",
			"F0",
			"HNR",
			"Jitter",
			"Shimmer",
		]
		df = pd.DataFrame(columns=columns)
	else:
		df = pd.DataFrame(all_records)

	output_csv = output_path / "features.csv"
	df.to_csv(output_csv, index=False)
	return df


def _build_parser() -> argparse.ArgumentParser:
	"""Create the CLI argument parser used by the entry point."""
	parser = argparse.ArgumentParser(description="Analyze cough audio files and extract features.")
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("--input-file", type=str, help="Path to a single WAV file to analyze.")
	group.add_argument("--input-dir", type=str, help="Directory containing WAV files to analyze.")
	parser.add_argument("--output-dir", type=str, default="results", help="Directory to store outputs.")
	return parser


def main(argv: list[str] | None = None) -> int:
	"""Parse CLI arguments, run the pipeline, and return an exit code."""
	parser = _build_parser()
	args = parser.parse_args(argv)

	run_pipeline(input_file=args.input_file, input_dir=args.input_dir, output_dir=args.output_dir)
	return 0


if __name__ == "__main__":
	raise SystemExit(main(sys.argv[1:]))
