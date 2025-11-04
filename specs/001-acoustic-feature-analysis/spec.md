# Feature Specification: ACCOUGH Acoustic Feature Analysis

**Feature Branch**: `001-acoustic-feature-analysis`
**Created**: 2025-11-04
**Status**: Draft
**Input**: User description: "ACCOUGH 聲學特徵分析"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Acoustic Feature Extraction (Priority: P1)

As a researcher, I want to process a cough audio file to extract a comprehensive set of acoustic features, so that I can analyze the characteristics of respiratory protective actions.

**Why this priority**: This is the core functionality of the system, enabling the primary research goal of understanding the link between acoustic features and patient conditions.

**Independent Test**: This can be tested by providing a WAV audio file (e.g., `34927020_cough.wav`) and verifying that the system outputs a data file (e.g., CSV) containing all specified acoustic parameters for the segmented cough sounds.

**Acceptance Scenarios**:

1. **Given** a valid WAV audio file containing cough sounds, **When** the analysis process is executed, **Then** the system generates an output file with calculated acoustic features for each valid segment.
2. **Given** an audio file with segments where the Signal-to-Noise Ratio (SNR) is below 30 dB, **When** the analysis is run, **Then** these low-quality segments are excluded from the final output.
3. **Given** a processed audio file, **When** the output is generated, **Then** the segmented audio files are correctly named with suffixes (e.g., `_01`, `_02`).

### Edge Cases

- **Empty Audio File**: What happens when an empty or silent audio file is provided? The system should report an error and skip processing.
- **Unsupported Format**: How does the system handle an audio file in a format other than WAV? It should raise an error indicating the format is not supported.
- **No Valid Segments**: What is the output if no audio segments meet the SNR > 30 dB criteria? The system should produce an empty output file or a message indicating no valid data was found.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST be able to read and process WAV audio files.
- **FR-002**: The system MUST handle audio samples that have been manually pre-segmented.
- **FR-003**: The system MUST perform automatic segmentation using an energy threshold method. A segment starts when the signal energy rises above a predefined threshold and ends when it falls below it.
- **FR-004**: The system MUST calculate background noise energy from adjacent non-coughing sections.
- **FR-005**: The system MUST filter out and discard any audio segment with a Signal-to-Noise Ratio (SNR) of 30 dB or less.
- **FR-006**: The system MUST downsample the audio signal to a target rate of 16,000 Hz.
- **FR-007**: The system MUST normalize the energy of each cough segment to an average of 1.
- **FR-008**: The system MUST save the processed, segmented audio into new files with a sequential suffix (e.g., `filename_01.wav`).
- **FR-009**: The system MUST calculate and output the following acoustic features for each segment:
    - Length (duration in seconds)
    - Amplitude contour (normalized)
    - Amplitude contour slope (2nd DCT coefficient)
    - Amplitude contour curvature (3rd DCT coefficient)
    - Sample entropy contour
    - Kurtosis contour
    - Crest factor
    - Relative position of crest factor
- **FR-010**: The system MUST calculate and report the relative energy distribution across these frequency bands: 0–400 Hz, 400–800 Hz, 800–1600 Hz, 1600–3200 Hz, and 3200 Hz to Nyquist frequency.
- **FR-011**: The system MUST calculate and report the weighted frequency by finding the highest energy spectral peaks and calculating their weighted average based on their energy.
- **FR-012**: The system MUST calculate the "Salience of Periodicity" for the whole signal and for the 0-400 Hz and 400-800 Hz bands.
- **FR-013**: The system MUST calculate the "Perturbation Percentage of Cycle Durations" for the 0-400 Hz and 400-800 Hz bands.
- **FR-014**: The system MUST support the analysis of the vowel /a/ to extract F0, HNR, Jitter, and Shimmer.
- **FR-015**: The system MUST output all calculated feature values in a tabular format (e.g., CSV), with segments as columns or rows.
- **FR-016**: The system MUST generate data ready for statistical analysis, including median, quartiles, min/max, confidence intervals, DCT coefficients, p-values, OR values, and AUC values.

### Key Entities

- **Audio Signal**: The raw input data from a WAV file, representing a recorded cough or throat-clearing sound.
- **Audio Segment**: A distinct portion of the Audio Signal, isolated through manual or automatic segmentation, representing a single cough event.
- **Acoustic Feature Set**: The collection of calculated parameters (e.g., Length, Crest Factor, F0) derived from an Audio Segment.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The system successfully processes 100% of valid input WAV files and generates a corresponding feature output file.
- **SC-002**: The output data contains all features as specified in FR-009, FR-010, FR-011, FR-012, FR-013, and FR-014 for every segment that meets the quality criteria (SNR > 30 dB).
- **SC-003**: The generated statistical values (p-value, OR, AUC) are verifiable and can be used directly in subsequent research analysis without further manual data transformation.
- **SC-004**: The processing time for a standard 5-minute audio file is under 60 seconds on a standard research machine.
