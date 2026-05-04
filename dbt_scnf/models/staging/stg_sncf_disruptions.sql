-- dbt_project/models/staging/stg_sncf_disruptions.sql
-- Nettoyage SQL minimal, 1 source = 1 modèle staging

WITH source AS (
    SELECT * FROM data.raw_sncf_disruptions
),
cleaned AS (
    SELECT
        id,
        status,
        severity,
        updated_at::timestamp AS updated_at,
        updated_at::date      AS disruption_date
    FROM source
    WHERE id IS NOT NULL
)
SELECT * FROM cleaned