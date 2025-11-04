# in src/analysis/features.py
import numpy as np

def calculate_length(segment: np.ndarray, sample_rate: int) -> float:
    """
    Calculates the duration of an audio segment in seconds.

    Args:
        segment: The audio segment as a NumPy array.
        sample_rate: The sample rate of the audio.

    Returns:
        The duration of the segment in seconds.
    """
    if sample_rate == 0:
        return 0.0
    return len(segment) / sample_rate

def calculate_amplitude_contour(signal: np.ndarray, frame_length: int, hop_length: int) -> np.ndarray:
    """
    Calculates the amplitude contour (envelope) of a signal.

    Args:
        signal: The input audio signal.
        frame_length: The length of each frame.
        hop_length: The step size between frames.

    Returns:
        An array representing the amplitude contour.
    """
    return np.array([
        np.sqrt(np.mean(signal[i:i+frame_length]**2))
        for i in range(0, len(signal) - frame_length, hop_length)
    ])

def calculate_rms_energy(signal: np.ndarray) -> float:
    """Calculates the Root Mean Square (RMS) energy of a signal."""
    return np.sqrt(np.mean(signal**2))

def calculate_zcr(signal: np.ndarray) -> float:
    """Calculates the Zero Crossing Rate of a signal."""
    if len(signal) < 2:
        return 0.0
    return np.sum(np.diff(np.sign(signal)) != 0) / (len(signal) - 1)