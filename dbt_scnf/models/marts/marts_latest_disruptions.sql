WITH ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY id
            ORDER BY ingestion_ts DESC
        ) AS rn
    FROM {{ ref('stg_sncf_disruptions') }}

)
SELECT *
FROM ranked
WHERE rn = 1