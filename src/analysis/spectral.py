# in src/analysis/spectral.py
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
    total_power = np.sum(power_spectrum)
    
    if total_power == 0:
        return [0.0] * len(bands)

    relative_energies = []
    for low, high in bands:
        band_mask = (xf >= low) & (xf < high)
        band_power = np.sum(power_spectrum[band_mask])
        relative_energies.append(band_power / total_power)
        
    return relative_energies