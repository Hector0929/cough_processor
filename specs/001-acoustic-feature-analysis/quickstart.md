# Quickstart: ACCOUGH Acoustic Feature Analysis

**Date**: 2025-11-04
**Spec**: [spec.md](./spec.md)

This guide provides instructions on how to set up and run the acoustic feature analysis pipeline.

## 1. Prerequisites

- Python 3.11 or higher
- `pip` for package installation

## 2. Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd cough_processor
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: The `requirements.txt` file will be created during the implementation phase).*

## 3. Running the Analysis

The main analysis is run via the `main.py` script.

1.  **Place your audio files**:
    Put the WAV files you want to analyze into the `src/data/` directory.

2.  **Execute the script**:
    You can run the analysis on a single file or an entire directory.

    - **Single File**:
      ```bash
      python src/main.py --input-file src/data/your_audio_file.wav --output-dir results/
      ```

    - **Directory**:
      ```bash
      python src/main.py --input-dir src/data/ --output-dir results/
      ```

## 4. Output

- The script will generate a CSV file in the specified output directory (e.g., `results/`).
- The CSV file will contain the extracted acoustic features for each valid cough segment found in the input audio.
- Processed audio segments will also be saved in the output directory.

**Example Output CSV (`results/features.csv`):**

| segment_id | length | amplitude_contour_slope | ... |
|------------|--------|-------------------------|-----|
| your_audio_file_01 | 0.45 | -0.123 | ... |
| your_audio_file_02 | 0.51 | -0.145 | ... |
