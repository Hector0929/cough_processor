<!--
Sync Impact Report:
- Version change: 0.1.0 -> 1.0.0
- Modified principles:
  - [PRINCIPLE_1_NAME] -> Python-First Development
  - [PRINCIPLE_2_NAME] -> Audio Processing with Parselmouth
  - [PRINCIPLE_3_NAME] -> Test-Driven Development (TDD)
- Added sections: None
- Removed sections: Principles 4 and 5, Sections 2 and 3
- Templates requiring updates:
  - ⚠ pending: .specify/templates/plan-template.md
  - ⚠ pending: .specify/templates/spec-template.md
  - ⚠ pending: .specify/templates/tasks-template.md
  - ⚠ pending: .specify/templates/commands/*.md
- Follow-up TODOs:
  - TODO(RATIFICATION_DATE): Confirm the official project ratification date.
-->

# Constitution of Project cough_processor

**Version**: 1.0.0
**Ratification Date**: TODO(RATIFICATION_DATE): Confirm the official project ratification date.
**Last Amended**: 2025-11-04

## 1. Core Principles

### 1.1. Principle 1: Python-First Development

**Rule**: All core application logic, data processing, and backend services MUST be implemented in Python.

**Rationale**: Standardizing on Python streamlines the development process, simplifies dependency management, and leverages the extensive ecosystem of scientific and data analysis libraries.

### 1.2. Principle 2: Audio Processing with Parselmouth

**Rule**: The `Parselmouth` library MUST be used for all acoustic analysis and audio manipulation tasks.

**Rationale**: `Parselmouth` provides a robust, scientifically validated interface to the Praat phonetics software, ensuring accuracy and reproducibility in audio feature extraction.

### 1.3. Principle 3: Test-Driven Development (TDD)

**Rule**: All new functionality MUST be developed following a strict Test-Driven Development (TDD) cycle. This means writing a failing test before writing the corresponding production code, and ensuring all tests pass before refactoring.

**Rationale**: TDD ensures that the codebase is thoroughly tested, reduces bugs, improves design, and serves as living documentation for the system's behavior.

## 2. Governance

### 2.1. Amendment Process

Amendments to this constitution require a formal proposal and review. Changes are categorized by impact:
- **MAJOR**: Backward-incompatible changes.
- **MINOR**: New principles or significant additions.
- **PATCH**: Clarifications and non-substantive edits.

### 2.2. Versioning

This document follows Semantic Versioning 2.0.0. The version number—MAJOR.MINOR.PATCH—is updated with each amendment.

### 2.3. Compliance

All project artifacts, including code, specifications, and documentation, MUST adhere to the principles outlined herein.

