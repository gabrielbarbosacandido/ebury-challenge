import pytest
from unittest.mock import patch, MagicMock

from dlthub.ingestion import _create_filesystem_pipeline, run_pipeline
import dlt

from include import constants as ct


@pytest.mark.parametrize(
    "incremental_column, from_date, to_date",
    [("transaction_date", "2025-01-01", "2025-01-10")],
)
@patch("dlthub.ingestion.filesystem")
@patch("dlthub.ingestion.read_csv")
@patch("dlthub.ingestion.incremental")
@patch("dlt.pipeline")
def test_create_filesystem_pipeline(
    mock_pipeline,
    mock_incremental,
    mock_read_csv,
    mock_filesystem,
    incremental_column: str,
    from_date: str,
    to_date: str,
) -> None:
    """
    Test the creation of a filesystem pipeline.

    This test mocks the filesystem, read_csv, incremental, and pipeline
    functions to verify that the pipeline is created correctly with the
    expected parameters.

    Args:
        mock_pipeline (MagicMock): Mocked pipeline function.
        mock_incremental (MagicMock): Mocked incremental function.
        mock_read_csv (MagicMock): Mocked read_csv function.
        mock_filesystem (MagicMock): Mocked filesystem function.
        incremental_column (str): The column used for incremental loading.
        from_date (str): The start date for the incremental loading.
        to_date (str): The end date for the incremental loading.

    Returns:
        None
    """
    mock_filesystem.return_value = MagicMock()
    mock_read_csv.return_value = MagicMock()
    mock_incremental.return_value = MagicMock()

    ct.CATCHUP = True

    result = _create_filesystem_pipeline(incremental_column, from_date, to_date)

    mock_filesystem.assert_called_once_with(
        bucket_url="data", file_glob="*.csv", extract_content=True
    )
    mock_read_csv.assert_called_once()

    mock_incremental.assert_called_once_with(
        incremental_column, initial_value=from_date, end_value=to_date
    )
    assert result is not None


@pytest.mark.parametrize(
    "pipeline_name, destination, dataset_name, table_name, incremental_column, from_date, to_date",
    [
        (
            "test_pipeline",
            "postgres",
            "test_dataset",
            "test_table",
            "transaction_date",
            "2025-01-01",
            "2025-01-10",
        )
    ],
)
@patch("dlthub.ingestion._create_filesystem_pipeline")
@patch("dlt.pipeline")
def test_run_pipeline_with_invalid_destination(
    mock_pipeline,
    mock_create_filesystem_pipeline,
    pipeline_name: str,
    destination: str,
    dataset_name: str,
    table_name: str,
    incremental_column: str,
    from_date: str,
    to_date: str,
) -> None:
    """
    Test the run_pipeline function when data is not correctly loaded to the destination.

    This test mocks the _create_filesystem_pipeline and pipeline functions and
    verifies that the appropriate exception is raised when the pipeline run fails.

    Args:
        mock_pipeline (MagicMock): Mocked pipeline function.
        mock_create_filesystem_pipeline (MagicMock): Mocked _create_filesystem_pipeline function.
        pipeline_name (str): The name of the pipeline.
        destination (str): The destination where the data will be loaded.
        dataset_name (str): The name of the dataset.
        table_name (str): The name of the table.
        incremental_column (str): The column used for incremental loading.
        from_date (str): The start date for incremental loading.
        to_date (str): The end date for incremental loading.

    Returns:
        None
    """
    mock_create_filesystem_pipeline.return_value = MagicMock()
    mock_pipeline.return_value = MagicMock()
    mock_pipeline.return_value.run.return_value = (
        "Error: Data was not correctly loaded to Postgres destination."
    )

    with pytest.raises(RuntimeError):
        run_pipeline(
            pipeline_name,
            destination,
            dataset_name,
            table_name,
            incremental_column,
            from_date=from_date,
            to_date=to_date,
        )

    mock_create_filesystem_pipeline.assert_called_once_with(
        incremental_column, from_date, to_date
    )
    mock_pipeline.return_value.run.assert_called_once()
