WITH source AS (
    SELECT * FROM {{ source('sncf_disruptions', 'raw_sncf_disruptions') }}
),
renamed AS (
    SELECT
        id,
        status,
        "severity.name" AS severity,
        strptime(updated_at, '%Y%m%dT%H%M%S') AS updated_at,
        strptime(updated_at, '%Y%m%dT%H%M%S')::DATE AS updated_date,
        ingestion_ts,
        messages
    FROM source
)
SELECT * FROM renamed