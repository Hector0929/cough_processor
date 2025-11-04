import pytest
import numpy as np
from src.analysis import spectral

def test_calculate_relative_energy():
    # Arrange
    signal = np.random.randn(16000)
    sample_rate = 16000
    bands = [(0, 1000), (1000, 4000)]

    # Act
    relative_energies = spectral.calculate_relative_energy(signal, sample_rate, bands)

    # Assert
    assert len(relative_energies) == len(bands)
    assert np.isclose(np.sum(relative_energies), 1.0)