from dagster import ScheduleDefinition
from .assets.ingestion import raw_sncf_disruptions


daily_schedule = ScheduleDefinition(
    name="daily_refresh",
    cron_schedule="0 10 * * *",  # Runs at 10 AM daily (UTC and I am at UTC+2)
    target=[raw_sncf_disruptions],
)