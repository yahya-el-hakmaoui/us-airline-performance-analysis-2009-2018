{{ config(materialized='table') }}

WITH cancellations AS (

    SELECT

        dc.carrier_key,

        dc.carrier_name,

        dd.year,

        ff.CANCELLATION_CODE,

        COUNT(*) AS cancellation_count

    FROM {{ ref('fact_flights') }} ff

    LEFT JOIN {{ ref('dim_carrier') }} dc
        ON ff.carrier_key = dc.carrier_key

    LEFT JOIN {{ ref('dim_date') }} dd
        ON ff.date_key = dd.date_key

    WHERE ff.CANCELLED = 1

    GROUP BY
        dc.carrier_key,
        dc.carrier_name,
        dd.year,
        ff.CANCELLATION_CODE
)

SELECT

    *,

    cancellation_count
    * 100.0
    / SUM(cancellation_count)
        OVER(PARTITION BY carrier_key, year)
    AS pct

FROM cancellations