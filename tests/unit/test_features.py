import pytest
import numpy as np
from src.analysis import features

def test_calculate_length():
    """
    Test that the length of a segment is calculated correctly in seconds.
    """
    # Arrange
    sample_rate = 16000
    segment = np.random.randn(int(0.5 * sample_rate)) # 0.5 seconds

    # Act
    length_in_seconds = features.calculate_length(segment, sample_rate)

    # Assert
    assert length_in_seconds == pytest.approx(0.5)

def test_calculate_amplitude_contour():
    """
    Test that the amplitude contour is calculated correctly.
    """
    # Arrange
    sample_rate = 16000
    signal = np.sin(np.linspace(0, 2 * np.pi, sample_rate)) # Simple sine wave
    frame_length = 400
    hop_length = 160

    # Act
    contour = features.calculate_amplitude_contour(signal, frame_length, hop_length)

    # Assert
    expected_num_frames = (len(signal) - frame_length) // hop_length + 1
    assert len(contour) == expected_num_frames
    assert np.all(contour >= 0)

def test_calculate_rms_energy():
    """
    Test that the RMS energy of a signal is calculated correctly.
    """
    # Arrange
    signal = np.array([1, -1, 1, -1]) # RMS should be 1
    
    # Act
    rms_energy = features.calculate_rms_energy(signal)

    # Assert
    assert rms_energy == pytest.approx(1.0)