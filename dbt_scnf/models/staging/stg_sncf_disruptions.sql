WITH source AS (
    SELECT * FROM {{ source('sncf_disruptions', 'raw_sncf_disruptions') }}
),
renamed AS (
    SELECT
        id,
        status,
        "severity.name" AS severity,
        updated_at AS updated_at,
        messages
    FROM source
    WHERE id IS NOT NULL
)
SELECT * FROM renamed