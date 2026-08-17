from dagster import Definitions, load_assets_from_package_module
from dagster_dbt import DbtCliResource, dbt_assets, DbtProject

from dagster_pipeline import assets
from dagster_pipeline.config import SNCF_TOKEN, DBT_PROJECT_DIR
from dagster_pipeline.resources import SNCFResource, DuckDBResource
from dagster_pipeline.schedules import sncf_ingestion_job
from dagster_pipeline.sensors import sncf_disruptions_sensor


defs = Definitions(
    assets=[
        *load_assets_from_package_module(assets),
    ],
    jobs=[sncf_ingestion_job],
    sensors=[sncf_disruptions_sensor],
    resources={
        "sncf_api": SNCFResource(sncf_token=SNCF_TOKEN),
        "duckdb":   DuckDBResource(database_path="data/sncf.duckdb"),
        "dbt":      DbtCliResource(project_dir=str(DBT_PROJECT_DIR)),
    },
)