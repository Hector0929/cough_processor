import numpy as np
from scipy.signal import resample

# in src/analysis/preprocessing.py

# ... (existing code) ...

def segment_by_energy(
    signal: np.ndarray,
    sample_rate: int,
    frame_length: int,
    hop_length: int,
    energy_threshold: float,
    min_duration: float,
) -> list[tuple[int, int]]:
    """
    Segments an audio signal based on energy.

    Args:
        signal: The input audio signal.
        sample_rate: The sample rate of the signal.
        frame_length: The length of each frame in samples.
        hop_length: The step size between frames in samples.
        energy_threshold: The energy threshold to consider a frame as active.
        min_duration: The minimum duration of a segment in seconds.

    Returns:
        A list of tuples, where each tuple contains the start and end
        sample index of a detected segment.
    """
    # Calculate RMS energy for each frame
    energy = np.array([
        np.sqrt(np.mean(signal[i:i+frame_length]**2))
        for i in range(0, len(signal) - frame_length, hop_length)
    ])

    # Find frames above the threshold
    is_active = energy > energy_threshold

    # Find start and end points of active segments
    min_segment_length_frames = int(min_duration * sample_rate / hop_length)
    segments = []
    start_frame = None
    for i, active in enumerate(is_active):
        if active and start_frame is None:
            start_frame = i
        elif not active and start_frame is not None:
            if (i - start_frame) >= min_segment_length_frames:
                start_sample = start_frame * hop_length
                end_sample = i * hop_length
                segments.append((start_sample, end_sample))
            start_frame = None

    # Check for a segment that runs to the end of the file
    if start_frame is not None:
        if (len(is_active) - start_frame) >= min_segment_length_frames:
            start_sample = start_frame * hop_length
            end_sample = len(signal)
            segments.append((start_sample, end_sample))

    return segments

def filter_by_snr(
    signal: np.ndarray,
    segments: list[tuple[int, int]],
    snr_threshold: float,
    noise_percentile: int = 10,
) -> list[tuple[int, int]]:
    """
    Filters segments based on their Signal-to-Noise Ratio (SNR).

    Args:
        signal: The input audio signal.
        segments: A list of tuples with start/end samples for each segment.
        snr_threshold: The SNR threshold in dB. Segments below this are discarded.
        noise_percentile: The percentile of signal energy to consider as noise level.

    Returns:
        A list of filtered segments that meet the SNR criteria.
    """
    if not segments:
        return []

    # Estimate noise level from the quieter parts of the signal
    frame_length = 1024
    hop_length = 512
    energies = np.array([
        np.sqrt(np.mean(signal[i:i+frame_length]**2))
        for i in range(0, len(signal) - frame_length, hop_length)
    ])
    
    # Handle case where energies might be empty or all zero
    if len(energies) == 0 or np.all(energies == 0):
        noise_level = 1e-9 # A very small number to avoid division by zero
    else:
        noise_level = np.percentile(energies[energies > 0], noise_percentile)
        if noise_level == 0:
            noise_level = 1e-9

    filtered_segments = []
    for start, end in segments:
        segment_signal = signal[start:end]
        if len(segment_signal) == 0:
            continue
        
        segment_energy = np.sqrt(np.mean(segment_signal**2))
        if segment_energy == 0:
            continue

        snr = 20 * np.log10(segment_energy / noise_level)

        if snr >= snr_threshold:
            filtered_segments.append((start, end))

    return filtered_segments

def normalize_energy(signal: np.ndarray) -> np.ndarray:
    """
    Normalizes the signal to have a peak amplitude of 1.0.

    Args:
        signal: The input audio signal.

    Returns:
        The normalized audio signal.
    """
    max_abs = np.max(np.abs(signal))
    if max_abs == 0:
        return signal
    return signal / max_abs