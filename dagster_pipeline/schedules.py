from dagster import define_asset_job, AssetSelection

sncf_ingestion_job = define_asset_job(
    name="sncf_ingestion_job",
    selection=AssetSelection.keys(
        "fetch_sncf_disruptions"
    ).downstream(),
)
