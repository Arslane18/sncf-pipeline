-- dbt_project/models/staging/stg_sncf_disruptions.sql
-- Nettoyage SQL minimal, 1 source = 1 modèle staging

WITH source AS (
    SELECT * FROM {{ source('sncf_disruptions', 'raw_sncf_disruptions') }}
),
renamed AS (
    SELECT
        id,
        status,
        "severity.name" AS severity_name,
        updated_at AS updated_at,
        messages
    FROM source
    WHERE id IS NOT NULL
)
SELECT * FROM renamed