import dlt
from dlt.sources.filesystem import filesystem, read_csv
from dlt.sources import incremental
from dlt.pipeline.pipeline import Pipeline

from include.utils import validate_date_format, validate_date_range
import constants as ct


def _create_filesystem_pipeline(
    incremental_column: str, from_date: str, to_date: str
) -> Pipeline:
    """
    Creates and configures a pipeline to extract data from CSV files and perform
    incremental loading based on the provided column.

    Parameters:
        incremental_column (str): The name of the column used for incremental loading.
        from_date (str): The start date for the incremental load.
        to_date (str): The end date for the incremental load.

    Returns:
        dlt.Pipeline: The configured pipeline for data extraction and incremental load.
    """
    try:
        filesystem_pipe = (
            filesystem(bucket_url="data", file_glob="*.csv", extract_content=True)
            | read_csv()
        )

        if ct.CATCHUP:
            validate_date_range(from_date, to_date)
            filesystem_pipe.apply_hints(
                incremental=incremental(
                    incremental_column, initial_value=from_date, end_value=to_date
                )
            )
        else:
            filesystem_pipe.apply_hints(incremental=incremental(incremental_column))

        return filesystem_pipe

    except Exception as e:
        raise RuntimeError(f"Error while creating filesystem pipeline: {str(e)}")


def run_pipeline(
    pipeline_name: str,
    destination: str,
    dataset_name: str,
    table_name: str,
    incremental_column: str,
    **kwargs,
) -> None:
    """
    Defines and runs the data pipeline, loading customer transaction information
    to the specified destination.

    Parameters:
        pipeline_name (str): The name of the pipeline to be created.
        destination (str): The destination where the data will be loaded (e.g., "postgres").
        dataset_name (str): The name of the dataset.
        table_name (str): The name of the table where the data will be stored.
        incremental_column (str): The name of the column used for incremental loading.

    Returns:
        None

    Raises:
        ValueError: If the destination or other parameters are invalid.
        RuntimeError: If an error occurs during pipeline execution.
    """
    from_date = kwargs.get("from_date", None)
    to_date = kwargs.get("to_date", None)

    try:
        filesystem_pipe = _create_filesystem_pipeline(
            incremental_column, from_date, to_date
        )
        pipeline = dlt.pipeline(
            pipeline_name=pipeline_name,
            destination=dlt.destinations.postgres(destination),
            dataset_name=dataset_name,
        )

        load_info = pipeline.run(filesystem_pipe.with_name(table_name))
        print(load_info)

        if "were loaded to destination postgres" in str(load_info):
            print("Success: Data loaded to Postgres destination.")
            print(f"Partition: {from_date} - {to_date} was loaded.")
        else:
            raise RuntimeError(
                "Error: Data was not correctly loaded to Postgres destination."
            )

    except ValueError as e:
        raise ValueError(f"Pipeline parameter error: {e}")
    except Exception as e:
        raise RuntimeError(f"Error running the pipeline: {e}")
