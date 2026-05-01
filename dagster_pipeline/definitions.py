from dagster import Definitions
from dagster import load_assets_from_package_module

from dagster_pipeline import assets
from dagster_pipeline.config import SNCF_TOKEN
from dagster_pipeline.resources import SNCFResource

defs = Definitions(
    assets=load_assets_from_package_module(assets),
    resources={
        "sncf_api": SNCFResource(sncf_token=SNCF_TOKEN),
    },
)