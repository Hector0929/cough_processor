# Research: ACCOUGH Acoustic Feature Analysis

**Date**: 2025-11-04
**Spec**: [spec.md](./spec.md)

This document summarizes the decisions made to resolve the technical unknowns from the initial plan.

## 1. Energy Threshold for Segmentation

- **Decision**: A dynamic threshold will be used, calculated as a percentage of the peak energy of the signal. A value of 10% (-10 dB from the peak) is a common starting point.
- **Rationale**: A fixed absolute threshold may not work well for recordings with different volume levels. A dynamic, relative threshold adapts to each file's characteristics.
- **Alternatives Considered**:
    - **Fixed Threshold**: Simpler to implement but less robust across different recordings.
    - **Hysteresis Thresholding**: More complex, using two thresholds to avoid creating multiple segments from a single event with fluctuating energy. This can be considered as a future improvement if the simpler method proves insufficient.

## 2. Statistical Value Generation (p-value, OR, AUC)

- **Decision**: These statistical values will NOT be generated directly by this feature's core pipeline. The pipeline's responsibility will end at generating the clean, tabular data (CSV) of acoustic features.
- **Rationale**: Calculating p-values, Odds Ratios (OR), and Area Under the Curve (AUC) requires a statistical model and a clear hypothesis (e.g., comparing two groups of patients). This is part of the *data analysis* phase, not the *feature extraction* phase. The feature's goal is to provide the necessary *input* for that analysis. Forcing it into this pipeline would violate the Single Responsibility Principle.
- **Alternatives Considered**:
    - **Integrating `statsmodels` or `scikit-learn`**: This would involve making assumptions about the research questions and data groups, which is beyond the scope of this feature. The analysis should be done separately, for example, in a Jupyter Notebook or a dedicated analysis script that consumes the output of this pipeline.

## 3. Vowel /a/ Analysis

- **Decision**: The analysis of the vowel /a/ will be implemented as a separate function or module. It will not be integrated into the main cough processing pipeline unless the input files are guaranteed to contain isolated vowel sounds.
- **Rationale**: The algorithms for analyzing a sustained vowel (like F0, Jitter, Shimmer) are different from those for transient, explosive sounds like coughs. Mixing them would complicate the main pipeline. The spec requires the system to "support" this analysis, which can be interpreted as providing the capability as a distinct tool.
- **Alternatives Considered**:
    - **A single pipeline for all sounds**: This would require a sound classification step to differentiate between coughs and vowels, adding significant complexity. It's better to process them separately based on the file type or name.
