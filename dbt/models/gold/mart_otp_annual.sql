{{ config(materialized='table') }}

SELECT

    dc.carrier_name,

    dd.year,

    COUNT(*) AS total_flights,

    AVG(ff.ARR_DELAY) AS avg_arr_delay,

    SUM(
        CASE
            WHEN ff.CANCELLED = 1 THEN 1
            ELSE 0
        END
    ) * 100.0 / COUNT(*) AS cancellation_rate,

    SUM(
        CASE
            WHEN ff.ARR_DELAY <= 15
                 AND ff.CANCELLED = 0
            THEN 1
            ELSE 0
        END
    ) * 100.0 / COUNT(*) AS otp_percentage,

    RANK() OVER(
        PARTITION BY dd.year
        ORDER BY
            SUM(
                CASE
                    WHEN ff.ARR_DELAY <= 15
                         AND ff.CANCELLED = 0
                    THEN 1
                    ELSE 0
                END
            ) * 100.0 / COUNT(*) DESC
    ) AS otp_rank

FROM {{ ref('fact_flights') }} ff

LEFT JOIN {{ ref('dim_carrier') }} dc
    ON ff.carrier_key = dc.carrier_key

LEFT JOIN {{ ref('dim_date') }} dd
    ON ff.date_key = dd.date_key

GROUP BY
    dc.carrier_name,
    dd.year