from dagster import sensor, RunRequest
import duckdb
from datetime import datetime
from dagster_pipeline.config import SNCF_API_URL
from dagster_pipeline.schedules import sncf_ingestion_job


@sensor(
        job=sncf_ingestion_job,
        required_resource_keys={"sncf_api"},
        minimum_interval_seconds=3600,
)
def sncf_disruptions_sensor(context):

    resp = context.resources.sncf_api.connect(
                SNCF_API_URL,
                count=1,
    )   
    disruptions = resp.get("disruptions", [])
    api_latest_updated_at = datetime.strptime(disruptions[0]["updated_at"], "%Y%m%dT%H%M%S")

    with duckdb.connect("data/sncf.duckdb") as conn:

        result = conn.execute("""
            SELECT MAX(updated_at)
            FROM stg_sncf_disruptions
        """).fetchone()

        local_latest_updated_at = result[0] if result else None  # Handle case where table is empty.


    if api_latest_updated_at != local_latest_updated_at:

        yield RunRequest(
            run_key=str(api_latest_updated_at),
        )

    else:

        context.log.info(
            "No new SNCF disruptions detected."
        )