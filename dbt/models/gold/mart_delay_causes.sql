{{ config(materialized='table') }}

SELECT

    dc.carrier_key,

    dc.carrier_name,

    dd.year,

    SUM(ff.ARR_DELAY) AS total_delay_minutes,

    SUM(ff.CARRIER_DELAY)
    * 100.0
    / NULLIF(SUM(ff.ARR_DELAY), 0)
    AS pct_carrier,

    SUM(ff.WEATHER_DELAY)
    * 100.0
    / NULLIF(SUM(ff.ARR_DELAY), 0)
    AS pct_weather,

    SUM(ff.NAS_DELAY)
    * 100.0
    / NULLIF(SUM(ff.ARR_DELAY), 0)
    AS pct_nas,

    SUM(ff.SECURITY_DELAY)
    * 100.0
    / NULLIF(SUM(ff.ARR_DELAY), 0)
    AS pct_security,

    SUM(ff.LATE_AIRCRAFT_DELAY)
    * 100.0
    / NULLIF(SUM(ff.ARR_DELAY), 0)
    AS pct_late_aircraft

FROM {{ ref('fact_flights') }} ff

LEFT JOIN {{ ref('dim_carrier') }} dc
    ON ff.carrier_key = dc.carrier_key

LEFT JOIN {{ ref('dim_date') }} dd
    ON ff.date_key = dd.date_key

WHERE ff.CANCELLED = 0

GROUP BY
    dc.carrier_key,
    dc.carrier_name,
    dd.year