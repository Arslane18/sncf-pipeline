import requests
import polars as pl
from dagster import asset, Output, MetadataValue

from dagster_pipeline.config import SNCF_API_URL


@asset(group_name="extract", compute_kind="python", required_resource_keys={"sncf_api"})
def raw_sncf_disruptions(context) -> Output[pl.DataFrame]:
    """Ingestion of raw SNCF disruptions data."""
    resp = context.resources.sncf_api.connect(SNCF_API_URL)

    data = resp.get("disruptions", [])
    df = pl.json_normalize(data)

    context.log.info(f"{len(df)} disruptions fetched.")

    return Output(
        df,
        metadata={
            "rows": len(df),
            "preview": MetadataValue.md(df.head(3).to_pandas().to_markdown()),
        }
    )

@asset(group_name="extract", compute_kind="python", deps=["raw_sncf_disruptions"])
def clean_sncf_disruptions(raw_sncf_disruptions: pl.DataFrame) -> pl.DataFrame:
    """Cleaning of raw SNCF disruptions data."""
    df = raw_sncf_disruptions.clone()

    df = df.select(["id", "status", "severity.name", "updated_at", "messages"])
    df = df.drop_nulls(subset=["id", "status"])
    df.write_parquet("data/clean_sncf_disruptions.parquet")

    return df