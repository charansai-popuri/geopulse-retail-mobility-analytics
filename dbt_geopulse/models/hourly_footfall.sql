select
    store,
    hour,
    unique_visitors,
    case
        when hour in (8, 9) then 'morning rush'
        when hour in (17, 18) then 'evening rush'
        when hour <= 5 then 'night'
        else 'daytime'
    end as period
from {{ ref('hourly_visitors') }}