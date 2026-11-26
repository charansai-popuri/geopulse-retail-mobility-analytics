with devices as (
    select device_id, count(*) as stores_visited
    from {{ source('raw', 'store_visits') }}
    group by device_id
)
select
    stores_visited,
    count(*) as devices,
    round(100.0 * count(*) / sum(count(*)) over (), 1) as pct_of_devices
from devices
group by stores_visited
order by stores_visited