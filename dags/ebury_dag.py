from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from cosmos import (
    DbtTaskGroup,
    ExecutionConfig,
    ExecutionMode,
    ProfileConfig,
    ProjectConfig,
)

import constants as ct
from dlthub import ingestion

with DAG(
    dag_id="daily_extraction_customer_transactions_data",
    default_args={"owner": ct.OWNER, "start_date": datetime(2025, 1, 9), "retries": 0},
    schedule_interval="@daily",
    description="""
        This DAG extracts and transform customer_transaction data from source filesystem 
        using the `dlt` to ingestion and `dbt` to clean, analytics and data modeling.
    """,
    catchup=ct.CATCHUP,
) as dag:

    run_dlthub = PythonOperator(
        task_id=f"el_{ct.TABLE_NAME}_csv_to_postegres",
        python_callable=ingestion.run_pipeline,
        op_kwargs={
            "pipeline_name": ct.PIPELINE_NAME,
            "destination": ct.DESTINATION,
            "dataset_name": ct.DATABASE_SCHEMA,
            "table_name": ct.TABLE_NAME,
            "incremental_column": ct.INCREMENTAL_COLUMN,
            "from_date": "{{ prev_ds }}",
            "to_date": "{{ ds }}",
        },
    )

    run_dbt = DbtTaskGroup(
        group_id="transformation",
        project_config=ProjectConfig(
            ct.DBT_ROOT_PATH,
            env_vars={
                "PG_HOST": "{{ conn.EBURY_DATABASE_CONN.host }}",
                "PG_DATABASE": "{{ conn.EBURY_DATABASE_CONN.schema }}",
                "DBT_USER": "{{ conn.EBURY_DATABASE_CONN.login }}",
                "DBT_PASSWORD": "{{ conn.EBURY_DATABASE_CONN.password }}",
                "PG_SCHEMA": "{{ conn.EBURY_DATABASE_CONN.schema }}",
            },
        ),
        profile_config=ProfileConfig(
            profile_name=ct.DBT_PROFILE_NAME,
            target_name=ct.DBT_TARGET_NAME,
            profiles_yml_filepath=ct.DBT_PROFILES_DIR,
        ),
        execution_config=ExecutionConfig(
            execution_mode=ExecutionMode.LOCAL,
        ),
        operator_args={
            "install_deps": True,
        },
    )

    run_dlthub >> run_dbt
