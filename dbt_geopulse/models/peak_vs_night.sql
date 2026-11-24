select
    store,
    period,
    count(*) as hours,
    round(avg(unique_visitors), 1) as avg_unique_visitors
from {{ ref('hourly_footfall') }}
group by store, period