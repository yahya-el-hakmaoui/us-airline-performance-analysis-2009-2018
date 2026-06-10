{{ config(materialized='table') }}

SELECT

    -- Flight surrogate key
    ROW_NUMBER() OVER() AS flight_key,

    -- Foreign keys
    dc.carrier_key,

    dd.date_key,

    -- Flight identifiers
    sf.OP_CARRIER_FL_NUM,

    -- Airports
    sf.ORIGIN,
    sf.DEST,

    -- Delays
    sf.DEP_DELAY,
    sf.ARR_DELAY,

    -- Cancellation / diversion
    sf.CANCELLED,
    sf.CANCELLATION_CODE,
    sf.DIVERTED,

    -- Delay causes
    sf.CARRIER_DELAY,
    sf.WEATHER_DELAY,
    sf.NAS_DELAY,
    sf.SECURITY_DELAY,
    sf.LATE_AIRCRAFT_DELAY,

    -- Metrics
    sf.DISTANCE,
    sf.CRS_ELAPSED_TIME,
    sf.ACTUAL_ELAPSED_TIME,
    sf.AIR_TIME,

    -- Delay flag
    sf.IS_DELAYED_ARR

FROM {{ ref('stg_flights') }} sf

LEFT JOIN {{ ref('dim_carrier') }} dc
    ON sf.OP_CARRIER = dc.iata_code

LEFT JOIN {{ ref('dim_date') }} dd
    ON CAST(sf.FL_DATE AS DATE) = dd.full_date