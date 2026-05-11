from dagster import Definitions, load_assets_from_package_module
from dagster_dbt import DbtCliResource, dbt_assets, DbtProject

from dagster_pipeline import assets
from dagster_pipeline.config import SNCF_TOKEN, DBT_PROJECT_DIR
from dagster_pipeline.resources import SNCFResource, DuckDBResource
from dagster_pipeline.schedules import ingestion_job, daily_10h_schedule


dbt_project = DbtProject(
    project_dir=DBT_PROJECT_DIR,
    profiles_dir=DBT_PROJECT_DIR,
)

@dbt_assets(manifest=dbt_project.manifest_path)
def sncf_dbt_assets(context, dbt: DbtCliResource):
    yield from dbt.cli(["run"], context=context).stream()


defs = Definitions(
    assets=[
        *load_assets_from_package_module(assets),
        sncf_dbt_assets,          
    ],
    jobs=[ingestion_job],
    schedules=[daily_10h_schedule],
    resources={
        "sncf_api": SNCFResource(sncf_token=SNCF_TOKEN),
        "duckdb":   DuckDBResource(database_path="data/sncf.duckdb"),
        "dbt":      DbtCliResource(project_dir=str(DBT_PROJECT_DIR)),
    },
)