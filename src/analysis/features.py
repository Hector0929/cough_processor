"""Feature extraction utilities for time-domain and vowel-specific metrics."""

from __future__ import annotations

import math

import numpy as np
import parselmouth
from parselmouth.praat import call
from scipy.fft import dct
from scipy.stats import kurtosis

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
    """Calculate the frame-wise RMS amplitude contour without normalization."""

    if frame_length <= 0 or hop_length <= 0:
        raise ValueError("frame_length and hop_length must be positive integers")

    if len(signal) < frame_length:
        return np.zeros(0, dtype=float)

    contour = np.array([
        np.sqrt(np.mean(signal[i : i + frame_length] ** 2))
        for i in range(0, len(signal) - frame_length, hop_length)
    ])

    return contour


def normalize_contour(contour: np.ndarray) -> np.ndarray:
    """Normalize a contour so its maximum absolute value equals 1.0."""

    if contour.size == 0:
        return contour.copy()

    peak = float(np.max(np.abs(contour)))
    if math.isclose(peak, 0.0):
        return np.zeros_like(contour, dtype=float)

    return contour / peak


def _safe_dct_coefficient(contour: np.ndarray, index: int) -> float:
    """Return a DCT coefficient, guarding short contours and index bounds."""

    if contour.size == 0:
        return 0.0

    coefficients = dct(contour, norm="ortho")
    if index >= coefficients.size:
        return 0.0

    return float(coefficients[index])


def calculate_amplitude_contour_slope(contour: np.ndarray) -> float:
    """Second DCT coefficient (slope) of the normalized amplitude contour."""

    return _safe_dct_coefficient(contour, 1)


def calculate_amplitude_contour_curvature(contour: np.ndarray) -> float:
    """Third DCT coefficient (curvature) of the normalized amplitude contour."""

    return _safe_dct_coefficient(contour, 2)


def calculate_sample_entropy(contour: np.ndarray, m: int = 2, r: float = 0.2) -> float:
    """Compute sample entropy for the provided contour."""

    if contour.size <= m + 1:
        return 0.0

    signal = np.asarray(contour, dtype=float)
    std = np.std(signal)
    if math.isclose(std, 0.0):
        return 0.0

    tolerance = r * std

    def _phi(embed_dim: int) -> float:
        embedded = np.array([signal[i : i + embed_dim] for i in range(0, signal.size - embed_dim + 1)])
        if embedded.size == 0:
            return 0.0

        matches = 0
        comparisons = 0
        for i in range(embedded.shape[0] - 1):
            diffs = np.max(np.abs(embedded[i + 1 :] - embedded[i]), axis=1)
            matches += np.sum(diffs <= tolerance)
            comparisons += diffs.size

        return (matches / comparisons) if comparisons else 0.0

    phi_m = _phi(m)
    phi_m1 = _phi(m + 1)

    if phi_m == 0.0 or phi_m1 == 0.0:
        return 0.0

    return float(-np.log(phi_m1 / phi_m))


def calculate_kurtosis(contour: np.ndarray) -> float:
    """Return excess kurtosis of the contour (Fisher definition)."""

    if contour.size == 0:
        return 0.0

    return float(kurtosis(contour, fisher=True, bias=False))


def calculate_crest_factor(signal: np.ndarray) -> float:
    """Peak-to-RMS ratio for the given signal."""

    if signal.size == 0:
        return 0.0

    peak = float(np.max(np.abs(signal)))
    if math.isclose(peak, 0.0):
        return 0.0

    rms = float(np.sqrt(np.mean(np.square(signal))))
    if math.isclose(rms, 0.0):
        return float("inf")

    return peak / rms


def calculate_crest_factor_position(contour: np.ndarray) -> float:
    """Return normalized position of the crest (max) within the contour."""

    if contour.size == 0:
        return 0.0

    crest_index = int(np.argmax(np.abs(contour)))
    if contour.size == 1:
        return 0.0

    return crest_index / (contour.size - 1)

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