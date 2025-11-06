# Task Execution Plan: ACCOUGH Acoustic Feature Analysis

**Branch**: `001-acoustic-feature-analysis` | **Date**: 2025-11-06 | **Spec**: [spec.md](./spec.md)

This execution plan focuses on extending the acoustic feature pipeline so the final CSV output contains the complete FR-009 metric set (length, normalized amplitude contour, amplitude contour slope, amplitude contour curvature, sample entropy contour, kurtosis contour, crest factor, and the crest factor position) while respecting the existing TDD workflow.

## Implementation Strategy

- Keep Python 3.11, Parselmouth, NumPy, SciPy, and Pandas stack from the plan.
- Apply strict TDD: add or update failing tests before modifying implementation files.
- Incrementally extend feature extraction helpers in `src/analysis/features.py`, then surface the new metrics in `src/main.py` and end-to-end tests.
- Reuse existing pipeline structure; minimize changes to preprocessing other than what is necessary for feature calculations.

## Phase 1: Setup

- [ ] T001 Verify development environment is active (venv) and dependencies from `requirements.txt` are installed.
- [ ] T002 Create or refresh local test audio fixtures if needed under `tests/test_data/` to exercise new contour metrics.

## Phase 2: Foundational Preparation

- [ ] T003 Review `specs/001-acoustic-feature-analysis/data-model.md` and `research.md` to confirm statistical definitions for the FR-009 metrics.
- [ ] T004 Ensure `tests/unit/test_features.py` has reusable helpers for generating synthetic segments to cover new feature calculations.

## Phase 3: User Story 1 – Extended Acoustic Feature Set (Priority P1)

**Story Goal**: Enhance the cough feature extraction so every segment row in the CSV includes all FR-009 acoustic metrics in addition to existing values.

**Independent Test Criteria**: Running `python -m pytest` (unit + integration) after implementation must confirm the new columns exist and contain deterministic values for known inputs.

- [ ] T005 [US1] Add failing unit tests in `tests/unit/test_features.py` covering amplitude contour slope and curvature extraction from synthetic signals.
- [ ] T006 [US1] Add failing unit tests in `tests/unit/test_features.py` for sample entropy contour and kurtosis contour calculations.
- [ ] T007 [US1] Add failing unit tests in `tests/unit/test_features.py` validating crest factor and crest factor position outputs.
- [ ] T008 [US1] Implement amplitude contour slope and curvature helpers in `src/analysis/features.py` using DCT-based calculations to satisfy T005.
- [ ] T009 [US1] Implement sample entropy contour and kurtosis contour computations in `src/analysis/features.py` to satisfy T006.
- [ ] T010 [US1] Implement crest factor and crest position calculations in `src/analysis/features.py` and ensure outputs align with T007 expectations.
- [x] T011 [US1] Update `_analyze_segment` in `src/main.py` to record the new FR-009 metrics in each segment dictionary and include them in the CSV schema.
- [x] T012 [US1] Extend `tests/integration/test_pipeline.py` to assert the presence and basic correctness of the new FR-009 columns when running the full pipeline.

## Phase 4: Polish & Validation

- [ ] T013 Update `README.md` quickstart/output sections to document the expanded CSV column list.
- [ ] T014 Run the full pytest suite and capture results to ensure regression-free integration.
- [ ] T015 Sanity-check a manual CLI run (`python -m src.main`) on a representative WAV file and confirm the CSV contains the expected FR-009 columns.
- [ ] T016 Review and update `specs/001-acoustic-feature-analysis/tasks.md` status and note any follow-up work.

## Dependencies

- US1 (Extended FR-009 Feature Set) depends on completion of Phases 1 and 2.
- Post-implementation polish tasks (Phase 4) require US1 tasks to be complete.

## Parallel Execution Examples

- T005–T007 modify the same test module and should run sequentially; once they are in place, T008–T010 can proceed in parallel when touching distinct helper functions.
- T011 and T012 must follow the feature helper implementations but can be executed consecutively as they touch different files (`src/main.py` vs `tests/integration/test_pipeline.py`).
- Polish tasks T013–T016 can largely run in order, with T014/T015 often executed back-to-back during validation.

# Task Execution Plan: ACCOUGH Acoustic Feature Analysis

**Branch**: `001-acoustic-feature-analysis` | **Date**: 2025-11-04 | **Spec**: [spec.md](./spec.md)

This plan breaks down the "ACCOUGH Acoustic Feature Analysis" feature into a series of concrete, executable tasks. The structure follows a Test-Driven Development (TDD) approach as mandated by the project constitution.

## Implementation Strategy

The implementation will follow the user story priorities defined in the specification. Since there is only one primary user story, we will build the feature incrementally, ensuring each component is fully tested before moving to the next. The MVP (Minimum Viable Product) will consist of the complete implementation of User Story 1.

## Phase 1: Project Setup

- [x] T001 Create the project directory structure as defined in `plan.md` (`src/analysis`, `src/data`, `src/utils`, `tests/unit`, `tests/integration`).
- [x] T002 Create empty Python files: `src/analysis/preprocessing.py`, `src/analysis/features.py`, `src/analysis/spectral.py`, `src/utils/audio_io.py`, and `src/main.py`.
- [x] T003 Create empty test files: `tests/unit/test_preprocessing.py`, `tests/unit/test_features.py`, `tests/unit/test_spectral.py`, `tests/unit/test_audio_io.py`, and `tests/integration/test_pipeline.py`.
- [x] T004 Create `requirements.txt` and add primary dependencies: `parselmouth`, `numpy`, `pandas`, `scipy`.
- [x] T005 Create a virtual environment and install dependencies from `requirements.txt`.

## Phase 2: Foundational Tasks (Audio I/O)

- [x] T006 [US1] Write a failing unit test in `tests/unit/test_audio_io.py` to verify that a WAV file can be loaded into a NumPy array.
- [x] T007 [US1] Implement the `load_wav` function in `src/utils/audio_io.py` to pass the test.
- [x] T008 [US1] Write a failing unit test in `tests/unit/test_audio_io.py` for saving segmented audio data to a new WAV file.
- [x] T009 [US1] Implement the `save_wav` function in `src/utils/audio_io.py` to pass the test.

## Phase 3: User Story 1 - Acoustic Feature Extraction

### Sub-phase 3.1: Preprocessing

- [x] T010 [US1] Write a failing unit test in `tests/unit/test_preprocessing.py` for the downsampling function.
- [x] T011 [US1] Implement the `downsample_signal` function in `src/analysis/preprocessing.py`.
- [x] T012 [US1] Write a failing unit test in `tests/unit/test_preprocessing.py` for the energy-based segmentation logic.
- [x] T013 [US1] Implement the `segment_by_energy` function in `src/analysis/preprocessing.py`.
- [x] T014 [US1] Write a failing unit test in `tests/unit/test_preprocessing.py` for the SNR filtering logic.
- [x] T015 [US1] Implement the `filter_by_snr` function in `src/analysis/preprocessing.py`.
- [x] T016 [US1] Write a failing unit test in `tests/unit/test_preprocessing.py` for the energy normalization function.
- [x] T017 [US1] Implement the `normalize_energy` function in `src/analysis/preprocessing.py`.

### Sub-phase 3.2: Acoustic Feature Calculation

- [x] T018 [P] [US1] In `tests/unit/test_features.py`, write failing tests for each acoustic feature in FR-009 (Length, Amplitude Contour, etc.).
- [x] T019 [P] [US1] In `src/analysis/features.py`, implement functions to calculate each acoustic feature from FR-009 to pass the tests.
- [x] T020 [P] [US1] In `tests/unit/test_spectral.py`, write failing tests for spectral features (Relative Energy, Weighted Frequency) from FR-010 and FR-011.
- [x] T021 [P] [US1] In `src/analysis/spectral.py`, implement functions to calculate the spectral features to pass the tests.
- [x] T022 [P] [US1] In `tests/unit/test_spectral.py`, write failing tests for perturbation features (Salience, Perturbation Percentage) from FR-012 and FR-013.
- [x] T023 [P] [US1] In `src/analysis/spectral.py`, implement functions to calculate the perturbation features to pass the tests.

### Sub-phase 3.3: Vowel Feature Calculation

- [x] T024 [P] [US1] In `tests/unit/test_features.py`, write failing tests for vowel features (F0, HNR, Jitter, Shimmer) from FR-014.
- [x] T025 [P] [US1] In `src/analysis/features.py`, implement a separate function `analyze_vowel` to calculate these features.

### Sub-phase 3.4: Pipeline and Output

- [x] T026 [US1] Write a failing integration test in `tests/integration/test_pipeline.py` that runs the full process on a sample audio file and checks the output CSV structure.
- [x] T027 [US1] Implement the main pipeline logic in `src/main.py` to connect all the modules: load, preprocess, analyze, and save results to a CSV file.
- [x] T028 [US1] Refine `src/main.py` to handle command-line arguments for input/output paths as specified in `quickstart.md`.

### Sub-phase 3.5: Extended FR-009 Feature Set

- [ ] T033 [US1] Add failing unit tests in `tests/unit/test_features.py` for amplitude contour slope/curvature, sample entropy contour, kurtosis contour, crest factor, and crest factor position.
- [ ] T034 [US1] Implement the additional FR-009 feature calculations in `src/analysis/features.py` to satisfy the new tests.
- [ ] T035 [US1] Update `src/main.py` (and helper modules if needed) to include the new FR-009 metrics in segment records and CSV output.
- [ ] T036 [US1] Extend `tests/integration/test_pipeline.py` to assert the presence of the new columns and representative values in the pipeline output.

### Sub-phase 3.6: SNR Filtering Removal

- [x] T037 [US1] Update `tests/unit/test_preprocessing.py` to reflect that segments are no longer discarded based on `filter_by_snr` thresholds.
- [x] T038 [US1] Modify `src/analysis/preprocessing.py` to disable SNR-based segment removal so the provided WAV data is processed directly.
- [x] T039 [US1] Adjust `src/main.py` to ignore SNR gating logic and ensure the entire input audio proceeds through the pipeline.
- [x] T040 [US1] Adapt `tests/integration/test_pipeline.py` to validate that all segments remain in the output without SNR filtering.

## Phase 4: Polish & Finalization

- [x] T029 Add comprehensive docstrings to all functions and modules.
- [x] T030 Review and update `README.md` with final usage instructions.
- [x] T031 Manually run the pipeline on a few test files to ensure robustness.
- [x] T032 Clean up any temporary code or comments.

## Dependencies

- **User Story 1 (US1)** is the only story and is self-contained.
- Within US1, tasks are ordered sequentially based on the TDD cycle and data flow (I/O -> Preprocessing -> Features -> Pipeline).

## Parallel Execution

- Within Sub-phase 3.2 and 3.3, the implementation of individual feature calculations (marked with `[P]`) can be parallelized, as they are independent of each other once the preprocessed data is available. For example, one developer could work on spectral features while another works on basic acoustic features.
