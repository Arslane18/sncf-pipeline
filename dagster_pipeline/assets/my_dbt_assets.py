from dagster_pipeline.config import DBT_PROJECT_DIR
from dagster_dbt import DbtCliResource, dbt_assets, DbtProject


dbt_project = DbtProject(
    project_dir=DBT_PROJECT_DIR,
    profiles_dir=DBT_PROJECT_DIR,
)

@dbt_assets(manifest=dbt_project.manifest_path)
def sncf_dbt_assets(context, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()