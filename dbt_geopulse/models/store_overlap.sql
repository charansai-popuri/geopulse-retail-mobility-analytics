with visits as (
    select device_id, store
    from {{ source('raw', 'store_visits') }}
),
store_totals as (
    select store, count(*) as devices from visits group by store
),
pairs as (
    select a.store as store_a, b.store as store_b, count(*) as shared_devices
    from visits a
    join visits b on a.device_id = b.device_id and a.store < b.store
    group by a.store, b.store
)
select
    p.store_a, p.store_b, p.shared_devices,
    round(100.0 * p.shared_devices / ta.devices, 1) as pct_of_store_a_devices,
    round(100.0 * p.shared_devices / tb.devices, 1) as pct_of_store_b_devices
from pairs p
join store_totals ta on ta.store = p.store_a
join store_totals tb on tb.store = p.store_b
order by p.store_a, p.store_b