from dagster import define_asset_job, ScheduleDefinition
 
ingestion_job = define_asset_job(
    name="ingestion_job",
    selection=["fetch_sncf_disruptions", "save_raw_sncf_disruptions"],
)
 
daily_10h_schedule = ScheduleDefinition(
    name="daily_10h_schedule",
    job=ingestion_job,
    cron_schedule="0 10 * * *",
    description="Launch data ingestion every day at 10:00 AM.", # Timezone is UTC and I am UTC+2.
)