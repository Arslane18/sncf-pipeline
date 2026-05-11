import polars as pl
from dagster import asset, Output, MetadataValue
from datetime import datetime, timezone

from dagster_pipeline.config import SNCF_API_URL

from .utils import get_row_count, insert_or_replace


@asset(
        group_name="ingestion", 
        compute_kind="python", 
        required_resource_keys={"sncf_api"}
)
def fetch_sncf_disruptions(context) -> Output[pl.DataFrame]:
    """Fetching SNCF disruptions data."""
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

@asset(
        group_name="ingestion", 
        compute_kind="python", 
        required_resource_keys={"duckdb"}
)
def save_raw_sncf_disruptions(context, fetch_sncf_disruptions: pl.DataFrame):
    """Persist raw SNCF disruptions into DuckDB."""

    df = fetch_sncf_disruptions.clone()

    df = df.with_columns(pl.lit(datetime.now(tz=timezone.utc)).alias("ingestion_ts"))   # We use UTC bc SNCF uses it aswell.
    
    with context.resources.duckdb.get_connection() as conn:
        insert_or_replace(conn, df, "raw_sncf_disruptions")

        row_count = get_row_count(conn, "raw_sncf_disruptions")

        context.log.info(
            f"{len(df)} rows upserted — total: {row_count}"
        )

        return Output(
            None,
            metadata={
                "rows_inserted": len(df),
                "total_rows": row_count,
            },
        )