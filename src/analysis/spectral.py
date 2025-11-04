"""Frequency-domain feature extraction helpers."""

import numpy as np
from scipy.fft import rfft, rfftfreq

def calculate_relative_energy(signal: np.ndarray, sample_rate: int, bands: list[tuple[int, int]]) -> list[float]:
    """Calculates the relative energy in different frequency bands."""
    n = len(signal)
    if n == 0:
        return [0.0] * len(bands)
        
    yf = rfft(signal)
    xf = rfftfreq(n, 1 / sample_rate)
    
    power_spectrum = np.abs(yf)**2
    relative_energies = []
    band_powers = []
    for low, high in bands:
        band_mask = (xf >= low) & (xf < high)
        band_power = np.sum(power_spectrum[band_mask])
        band_powers.append(band_power)
    total_band_power = np.sum(band_powers)
    if total_band_power == 0:
        return [0.0] * len(bands)

    for band_power in band_powers:
        relative_energies.append(band_power / total_band_power)
        
    return relative_energies