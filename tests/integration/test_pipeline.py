from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src import main
from src.utils import audio_io


@pytest.mark.integration
def test_pipeline_generates_feature_csv(tmp_path):
	"""
	Full pipeline should generate a features CSV with the expected schema.
	"""
	input_file = Path("tests/test_data/sample.wav").resolve()
	assert input_file.exists(), "Sample input audio is missing for integration test."

	output_dir = tmp_path / "results"
	output_dir.mkdir()

	main.run_pipeline(input_file=str(input_file), output_dir=str(output_dir))

	output_csv = output_dir / "features.csv"
	assert output_csv.exists(), "Pipeline did not produce the features.csv output file."

	df = pd.read_csv(output_csv)
	expected_columns = {
		"segment_id",
		"length",
		"rms_energy",
		"zcr",
		"amplitude_mean",
		"amplitude_contour",
		"amplitude_contour_slope",
		"amplitude_contour_curvature",
		"sample_entropy_contour",
		"kurtosis_contour",
		"crest_factor",
		"crest_factor_position",
		"F0",
		"HNR",
	}

	missing = expected_columns.difference(df.columns)
	assert not missing, f"Missing expected columns in output: {missing}"

	first_row = df.iloc[0]
	assert isinstance(first_row["amplitude_contour"], str)
	assert first_row["amplitude_contour"] != ""
	assert np.isfinite(first_row["amplitude_contour_slope"])
	assert np.isfinite(first_row["sample_entropy_contour"])
	assert 0.0 <= first_row["crest_factor_position"] <= 1.0


@pytest.mark.integration
def test_pipeline_keeps_low_snr_segments(tmp_path):
	sample_rate = 16_000
	duration = 1.0
	n_samples = int(sample_rate * duration)

	rng = np.random.default_rng(42)
	noise = rng.normal(scale=0.05, size=n_samples)
	segment = noise.copy()
	start = int(0.2 * sample_rate)
	end = int(0.5 * sample_rate)
	segment[start:end] += 0.02  # barely above noise floor
	segment = np.clip(segment, -1.0, 1.0)

	input_file = tmp_path / "low_snr.wav"
	audio_io.save_wav(str(input_file), segment.astype(np.float32), sample_rate)

	output_dir = tmp_path / "output"
	output_dir.mkdir()

	df = main.run_pipeline(input_file=str(input_file), output_dir=str(output_dir))

	assert not df.empty, "Low-SNR segment should persist through the pipeline."
	assert any(df["segment_id"].str.contains("low_snr")), "Segment IDs should include low_snr recording."
