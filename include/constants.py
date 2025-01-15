import os
from pathlib import Path
from airflow.hooks.base_hook import BaseHook

CATCHUP = False
OWNER = "data_plataform_team"

DBT_ROOT_PATH = Path(__file__).parent / "dbt"
DBT_PROFILES_DIR = os.path.join(DBT_ROOT_PATH, "profiles.yml")
DBT_PROFILE_NAME = "ebury_challenge"
DBT_TARGET_NAME = "prod"

DESTINATION = BaseHook.get_connection("EBURY_DATABASE_CONN").get_uri()
DATABASE_SCHEMA = "raw"
TABLE_NAME = "customer_transactions"
PIPELINE_NAME = "extract_" + TABLE_NAME
INCREMENTAL_COLUMN = "transaction_date"
