from dagster_pipeline.config import DBT_PROJECT_DIR
from dagster_dbt import DbtCliResource, dbt_assets, DbtProject, DagsterDbtTranslator
from dagster import AssetKey

class CustomDagsterDbtTranslator(DagsterDbtTranslator):
    def get_asset_key(self, dbt_resource_props):
        if dbt_resource_props["resource_type"] == "source":
            if dbt_resource_props["name"] == "raw_sncf_disruptions":
                return AssetKey("save_raw_sncf_disruptions")
        return super().get_asset_key(dbt_resource_props)


dbt_project = DbtProject(
    project_dir=DBT_PROJECT_DIR,
    profiles_dir=DBT_PROJECT_DIR,
)

@dbt_assets(manifest=dbt_project.manifest_path, dagster_dbt_translator=CustomDagsterDbtTranslator())
def sncf_dbt_assets(context, dbt: DbtCliResource):
    yield from dbt.cli(["run"], context=context).stream()