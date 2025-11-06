"""Signal preprocessing utilities for the cough analysis pipeline."""

import numpy as np
from scipy.signal import resample


def downsample_signal(signal: np.ndarray, original_rate: int, target_rate: int) -> np.ndarray:
    """Resample the signal to the target sample rate."""
    if original_rate == target_rate:
        return signal

    if original_rate <= 0 or target_rate <= 0:
        raise ValueError("Sample rates must be positive integers.")

    num_samples = int(len(signal) * target_rate / original_rate)
    if num_samples <= 0:
        raise ValueError("Calculated number of samples is non-positive.")

    return resample(signal, num_samples)


def segment_by_energy(
    signal: np.ndarray,
    sample_rate: int,
    frame_length: int,
    hop_length: int,
    energy_threshold: float,
    min_duration: float,
) -> list[tuple[int, int]]:
    """
    Segments an audio signal based on energy.

    Args:
        signal: The input audio signal.
        sample_rate: The sample rate of the signal.
        frame_length: The length of each frame in samples.
        hop_length: The step size between frames in samples.
        energy_threshold: The energy threshold to consider a frame as active.
        min_duration: The minimum duration of a segment in seconds.

    Returns:
        A list of tuples, where each tuple contains the start and end
        sample index of a detected segment.
    """
    # Calculate RMS energy for each frame
    energy = np.array([
        np.sqrt(np.mean(signal[i:i+frame_length]**2))
        for i in range(0, len(signal) - frame_length, hop_length)
    ])

    # Find frames above the threshold
    is_active = energy > energy_threshold

    # Find start and end points of active segments
    min_segment_length_frames = int(min_duration * sample_rate / hop_length)
    segments = []
    start_frame = None
    for i, active in enumerate(is_active):
        if active and start_frame is None:
            start_frame = i
        elif not active and start_frame is not None:
            if (i - start_frame) >= min_segment_length_frames:
                start_sample = start_frame * hop_length
                end_sample = i * hop_length
                segments.append((start_sample, end_sample))
            start_frame = None

    # Check for a segment that runs to the end of the file
    if start_frame is not None:
        if (len(is_active) - start_frame) >= min_segment_length_frames:
            start_sample = start_frame * hop_length
            end_sample = len(signal)
            segments.append((start_sample, end_sample))

    return segments

def filter_by_snr(
    signal: np.ndarray,
    segments: list[tuple[int, int]],
    snr_threshold: float,
    noise_percentile: int = 10,
) -> list[tuple[int, int]]:
    """Return segments unchanged; SNR-based pruning is disabled."""
    if not segments:
        return []

    return list(segments)

def normalize_energy(signal: np.ndarray) -> np.ndarray:
    """
    Normalizes the signal to have a peak amplitude of 1.0.

    Args:
        signal: The input audio signal.

    Returns:
        The normalized audio signal.
    """
    max_abs = np.max(np.abs(signal))
    if max_abs == 0:
        return signal
    return signal / max_abs