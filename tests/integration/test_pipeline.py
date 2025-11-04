import pandas as pd
import pytest
from pathlib import Path

from src import main


@pytest.mark.integration
def test_pipeline_generates_feature_csv(tmp_path):
	"""
	Full pipeline should generate a features CSV with the expected schema.
	"""
	input_file = Path("tests/test_data/sample.wav").resolve()
	assert input_file.exists(), "Sample input audio is missing for integration test."

	output_dir = tmp_path / "results"
	output_dir.mkdir()

	main.run_pipeline(input_file=str(input_file), output_dir=str(output_dir))

	output_csv = output_dir / "features.csv"
	assert output_csv.exists(), "Pipeline did not produce the features.csv output file."

	df = pd.read_csv(output_csv)
	expected_columns = {
		"segment_id",
		"length",
		"F0",
		"HNR",
	}

	missing = expected_columns.difference(df.columns)
	assert not missing, f"Missing expected columns in output: {missing}"
