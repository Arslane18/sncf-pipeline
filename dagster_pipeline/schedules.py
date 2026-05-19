from dagster import define_asset_job, ScheduleDefinition
 

sncf_ingestion_job = define_asset_job(
    name="sncf_ingestion_job",
    selection=[
        "fetch_sncf_disruptions",
        "save_raw_sncf_disruptions",
    ],
)