import requests
import polars as pl
from dagster import asset, Output, MetadataValue

from dagster_pipeline.config import SNCF_API_URL


@asset(group_name="raw", compute_kind="python", defs="sncf_api")
def raw_sncf_disruptions(context) -> Output[pl.DataFrame]:
    """Ingestion of raw SNCF disruptions data."""
    resp = context.resources.sncf_api.connect(SNCF_API_URL)

    data = resp.json().get("disruptions", [])
    df = pl.json_normalize(data)

    context.log.info(f"{len(df)} disruptions fetched.")

    return Output(
        df,
        metadata={
            "rows": len(df),
            "preview": MetadataValue.md(df.head(3).to_pandas().to_markdown()),
        }
    )