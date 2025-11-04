"""Feature extraction utilities for time-domain and vowel-specific metrics."""

import numpy as np
import parselmouth
from parselmouth.praat import call

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


def analyze_vowel(sound: parselmouth.Sound, sample_rate: int | None = None) -> dict[str, float]:
    """Extracts vowel-based acoustic features using Parselmouth."""
    if not isinstance(sound, parselmouth.Sound):
        raise TypeError("sound must be a parselmouth.Sound instance")

    if sample_rate is None:
        sample_rate = int(sound.sampling_frequency)

    # Fundamental frequency (F0)
    pitch = sound.to_pitch()
    frequencies = pitch.selected_array["frequency"]
    voiced_frequencies = frequencies[frequencies > 0]
    f0 = float(np.nanmean(voiced_frequencies)) if voiced_frequencies.size else 0.0

    # Harmonics-to-noise ratio (HNR)
    harmonicity = sound.to_harmonicity_cc()
    hnr = float(call(harmonicity, "Get mean", 0, 0))

    # Jitter and shimmer require a point process derived from the pitch contour
    point_process = call(sound, "To PointProcess (periodic, cc)", 75, 500)
    jitter = float(
        call(
            point_process,
            "Get jitter (local)",
            0,
            0,
            0.0001,
            0.02,
            1.3,
        )
    )
    shimmer = float(
        call(
            [sound, point_process],
            "Get shimmer (local)",
            0,
            0,
            0.0001,
            0.02,
            1.3,
            1.6,
        )
    )

    return {
        "F0": max(f0, 0.0),
        "HNR": hnr,
        "Jitter": max(jitter, 0.0),
        "Shimmer": max(shimmer, 0.0),
    }