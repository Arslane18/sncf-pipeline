from dagster import Definitions
from dagster import load_assets_from_package_module

from dagster_pipeline.assets.ingestion import raw_sncf_disruptions
from dagster_pipeline.config import SNCF_TOKEN
from dagster_pipeline.resources import SNCFResource

defs = Definitions(
    assets=[raw_sncf_disruptions],
    resources={
        "sncf_api": SNCFResource(sncf_token=SNCF_TOKEN),
    },
)