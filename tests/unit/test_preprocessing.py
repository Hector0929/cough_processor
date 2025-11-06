import pytest
import numpy as np
from src.analysis import preprocessing

# ...existing code...

def test_segment_by_energy():
    """
    Test that a signal is correctly segmented based on energy.
    """
    # Arrange
    sample_rate = 16000
    signal = np.zeros(sample_rate) # 1 second of audio

    # Create two loud segments
    segment_1_start, segment_1_end = int(0.1 * sample_rate), int(0.3 * sample_rate)
    segment_2_start, segment_2_end = int(0.6 * sample_rate), int(0.8 * sample_rate)

    signal[segment_1_start:segment_1_end] = 1.0
    signal[segment_2_start:segment_2_end] = 1.0

    # Act
    segments = preprocessing.segment_by_energy(
        signal,
        sample_rate,
        frame_length=int(0.02 * sample_rate),
        hop_length=int(0.01 * sample_rate),
        energy_threshold=0.1,
        min_duration=0.1
    )

    # Assert
    assert len(segments) == 2
    assert abs(segments[0][0] - segment_1_start) < 500
    assert abs(segments[0][1] - segment_1_end) < 500
    assert abs(segments[1][0] - segment_2_start) < 500
    assert abs(segments[1][1] - segment_2_end) < 500

def test_filter_by_snr_preserves_segments():
    """Previously filtered segments should now pass through unchanged."""
    sample_rate = 16000
    noise = np.random.randn(sample_rate) * 0.1
    signal = noise.copy()

    high_snr_segment = (int(0.1 * sample_rate), int(0.3 * sample_rate))
    low_snr_segment = (int(0.6 * sample_rate), int(0.8 * sample_rate))

    signal[high_snr_segment[0]:high_snr_segment[1]] += 1.0
    signal[low_snr_segment[0]:low_snr_segment[1]] += 0.01

    all_segments = [high_snr_segment, low_snr_segment]

    filtered_segments = preprocessing.filter_by_snr(signal, all_segments, snr_threshold=30.0)

    assert filtered_segments == all_segments

def test_normalize_energy():
    """
    Test that the energy of a signal is normalized to a peak of 1.0.
    """
    # Arrange
    signal = np.array([0.1, 0.2, -0.5, 0.3, -0.1]) # Peak is 0.5

    # Act
    normalized_signal = preprocessing.normalize_energy(signal)

    # Assert
    assert np.max(np.abs(normalized_signal)) == pytest.approx(1.0)