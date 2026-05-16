WITH transitions AS (

    SELECT
        id,

        status AS new_status,

        LAG(status) OVER (
            PARTITION BY id
            ORDER BY ingestion_ts
        ) AS old_status,

        ingestion_ts

    FROM {{ ref('stg_sncf_disruptions') }}

)

SELECT
    id,
    old_status,
    new_status,
    ingestion_ts AS transition_at

FROM transitions

WHERE old_status IS NOT NULL
  AND old_status != new_status