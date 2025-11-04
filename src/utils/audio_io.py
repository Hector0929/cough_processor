import wave
import numpy as np

def load_wav(file_path: str) -> tuple[np.ndarray, int]:
    """
    Loads a WAV file into a NumPy array.

    Args:
        file_path: The path to the WAV file.

    Returns:
        A tuple containing:
            - A NumPy array with the audio signal.
            - The sample rate of the audio file.
    """
    with wave.open(file_path, 'rb') as wf:
        sample_rate = wf.getframerate()
        n_frames = wf.getnframes()
        channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        
        frames = wf.readframes(n_frames)
        
        # Convert byte string to numpy array
        if sampwidth == 1:
            # 8-bit unsigned
            signal = np.frombuffer(frames, dtype=np.uint8)
            signal = (signal - 128) / 128.0
        elif sampwidth == 2:
            # 16-bit signed
            signal = np.frombuffer(frames, dtype=np.int16)
            signal = signal / 32768.0
        elif sampwidth == 3:
            # 24-bit signed
            # numpy doesn't have a 24-bit type, so we read as bytes and convert
            signal = np.empty((n_frames, channels), dtype=np.float64)
            for i in range(n_frames):
                frame = frames[i*3*channels : (i+1)*3*channels]
                for c in range(channels):
                    val_bytes = frame[c*3:(c+1)*3]
                    # Add a sign byte
                    if val_bytes[2] & 0x80:
                        val_bytes += b'\xff'
                    else:
                        val_bytes += b'\x00'
                    val = int.from_bytes(val_bytes, 'little', signed=True)
                    signal[i, c] = val / 8388608.0
        else:
            raise ValueError(f"Unsupported sample width: {sampwidth}")

        if channels > 1:
            # For stereo, just take the first channel
            signal = signal[::channels]

    return signal, sample_rate

def save_wav(file_path: str, signal: np.ndarray, sample_rate: int):
    """
    Saves a NumPy array as a WAV file.

    Args:
        file_path: The path to save the WAV file.
        signal: The NumPy array containing the audio signal.
        sample_rate: The sample rate of the audio.
    """
    # Normalize to 16-bit signed integer range
    signal_int = np.int16(signal * 32767)

    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 2 bytes for 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(signal_int.tobytes())
