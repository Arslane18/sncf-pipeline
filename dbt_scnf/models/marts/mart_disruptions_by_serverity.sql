with staging as (
    select * from {{ ref('stg_sncf_disruptions') }}
)

select
    severity,
    status,
    count(*)                          as nb_disruptions
from staging
group by severity, status
order by nb_disruptions desc
