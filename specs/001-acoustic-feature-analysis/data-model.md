# Data Model: ACCOUGH Acoustic Feature Analysis

**Date**: 2025-11-04
**Spec**: [spec.md](./spec.md)

This document defines the key data structures for the feature.

## 1. AudioSegment

Represents a single, processed cough segment ready for feature extraction.

- **Fields**:
    - `id` (string): A unique identifier, typically derived from the original filename and a segment index (e.g., `34927020_cough_01`).
    - `signal` (numpy.ndarray): The raw audio data of the segment as a 1D NumPy array.
    - `sampling_rate` (int): The sampling rate of the audio signal (e.g., 16000).
    - `original_filename` (string): The name of the source audio file.

- **State Transitions**:
    - `raw` -> `preprocessed` (Downsampled, Filtered) -> `normalized` -> `features_extracted`

## 2. AcousticFeatureSet

A collection of all acoustic and spectral features calculated for a single `AudioSegment`. This will be the primary data structure for the final output.

- **Fields**:
    - `segment_id` (string): Foreign key linking to the `AudioSegment`.
    - `length` (float): Duration in seconds.
    - `amplitude_contour_slope` (float): 2nd DCT coefficient.
    - `amplitude_contour_curvature` (float): 3rd DCT coefficient.
    - `sample_entropy` (float): A single value representing the mean of the contour.
    - `kurtosis` (float): A single value representing the mean of the contour.
    - `crest_factor` (float)
    - `relative_position_crest_factor` (float)
    - `relative_energy_band_1` (float): Energy in 0-400 Hz band.
    - `relative_energy_band_2` (float): Energy in 400-800 Hz band.
    - `relative_energy_band_3` (float): Energy in 800-1600 Hz band.
    - `relative_energy_band_4` (float): Energy in 1600-3200 Hz band.
    - `relative_energy_band_5` (float): Energy in 3200-Nyquist band.
    - `weighted_frequency` (float)
    - `salience_periodicity_total` (float)
    - `salience_periodicity_band_1` (float): For 0-400 Hz.
    - `salience_periodicity_band_2` (float): For 400-800 Hz.
    - `perturbation_percentage_band_1` (float): For 0-400 Hz.
    - `perturbation_percentage_band_2` (float): For 400-800 Hz.

## 3. VowelFeatureSet

A separate data structure for the features of a vowel /a/ sound.

- **Fields**:
    - `segment_id` (string)
    - `f0` (float): Fundamental frequency.
    - `hnr` (float): Harmonics-to-Noise Ratio.
    - `jitter` (float)
    - `shimmer` (float)

## Output Format

The final output will be a CSV file where each row represents an `AcousticFeatureSet` for one `AudioSegment`.

**Example CSV:**

| segment_id | length | amplitude_contour_slope | ... | perturbation_percentage_band_2 |
|------------|--------|-------------------------|-----|--------------------------------|
| cough_01   | 0.45   | -0.123                  | ... | 1.234                          |
| cough_02   | 0.51   | -0.145                  | ... | 1.567                          |
