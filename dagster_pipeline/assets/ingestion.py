import requests
import polars as pl
from dagster import asset, Output, MetadataValue

from dagster_pipeline.config import SNCF_API_URL


@asset(group_name="extract", compute_kind="python", required_resource_keys={"sncf_api"})
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

@asset(group_name="extract", compute_kind="python", deps=["fetch_sncf_disruptions"], required_resource_keys={"duckdb"})
def save_raw_sncf_disruptions(context, fetch_sncf_disruptions: pl.DataFrame):
    """Saving raw SNCF disruptions data."""
    df = fetch_sncf_disruptions.clone()

    df = df.select(["id", "status", "severity.name", "updated_at", "messages"])
    df = df.drop_nulls(subset=["id", "status"])
    conn = context.resources.duckdb.get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS raw_sncf_disruptions AS
            SELECT * FROM df WHERE 1=0
        """)
 
        conn.execute("""
            DELETE FROM raw_sncf_disruptions
            WHERE id IN (SELECT id FROM df)
        """)
        conn.execute("INSERT INTO raw_sncf_disruptions SELECT * FROM df")
 
        row_count = conn.execute(
            "SELECT COUNT(*) FROM raw_sncf_disruptions"
        ).fetchone()[0]
 
        context.log.info(
            f"{len(df)} insertions — total lines in DB : {row_count} lines."
        )
    finally:
        conn.close()