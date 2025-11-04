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