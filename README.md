# Cough Processor

Pipeline for extracting acoustic features from cough recordings using Python and Parselmouth.

## Prerequisites

- Python 3.11
- Recommended on Windows/macOS/Linux with standard laptop hardware

## Setup

```powershell
python3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Optional: run `python -m pytest` to verify the environment.

## Running the Pipeline

Analyze a single WAV file and store results under `results/`:

```powershell
venv\Scripts\activate
python -m src.main --input-file tests/test_data/sample.wav --output-dir results
```

Analyze every WAV inside a directory:

```powershell
venv\Scripts\activate
python -m src.main --input-dir path\to\wav_folder --output-dir results
Example: python -m src.main --input-file D:\audio_processor\audio_processor\segments_loudness_processed\4_yi_reflex_01.wav --output-dir D:\cough_processor\results
```

The pipeline saves:

- `results/features.csv` – aggregated feature table
- `results/segments/*.wav` – normalized segments extracted by the pipeline

CLI flags:
- Provide exactly one of `--input-file` or `--input-dir`; the short form `--input` is not supported.
- Use `--output-dir` to choose where `features.csv` and segment WAVs are written; defaults to `results/`.

## Testing

```powershell
venv\Scripts\activate
python -m pytest
```

Integration tests are marked with `@pytest.mark.integration` and exercise the full pipeline end-to-end.
