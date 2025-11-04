import pytest
import numpy as np
import os
from src.utils import audio_io

@pytest.fixture
def sample_wav_path():
    # Create a dummy WAV file for testing
    # This path is relative to the project root
    test_data_dir = 'tests/test_data'
    if not os.path.exists(test_data_dir):
        os.makedirs(test_data_dir)
    
    path = os.path.join(test_data_dir, 'sample.wav')
    
    # The file is already created in the previous step, so we just return the path
    # If you need to create it dynamically in a test:
    # from scipy.io.wavfile import write
    # sample_rate = 16000
    # frequency = 440
    # duration = 1
    # t = np.linspace(0., duration, int(sample_rate * duration))
    # amplitude = np.iinfo(np.int16).max * 0.5
    # data = amplitude * np.sin(2. * np.pi * frequency * t)
    # write(path, sample_rate, data.astype(np.int16))
    
    return path

def test_load_wav_returns_numpy_array(sample_wav_path):
    """
    Test that load_wav returns a numpy array and the correct sample rate.
    """
    # Act
    signal, sample_rate = audio_io.load_wav(sample_wav_path)

    # Assert
    assert isinstance(signal, np.ndarray)
    assert isinstance(sample_rate, int)
    assert sample_rate == 16000 # As created in the fixture

def test_save_wav_creates_file(sample_wav_path):
    """
    Test that save_wav creates a new WAV file.
    """
    # Arrange
    signal, sample_rate = audio_io.load_wav(sample_wav_path)
    output_path = os.path.join('tests/test_data', 'output.wav')
    if os.path.exists(output_path):
        os.remove(output_path)

    # Act
    audio_io.save_wav(output_path, signal, sample_rate)

    # Assert
    assert os.path.exists(output_path)
    
    # Cleanup
    os.remove(output_path)
