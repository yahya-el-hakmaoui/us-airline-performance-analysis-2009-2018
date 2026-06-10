{{ config(materialized='table') }}

WITH base AS (

    SELECT

        dc.carrier_key,

        dc.carrier_name,

        dc.carrier_type,

        dd.year,

        COUNT(*) AS total_flights,

        AVG(ff.ARR_DELAY) AS avg_arr_delay,

        SUM(
            CASE
                WHEN ff.CANCELLED = 1
                THEN 1
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
        ) * 100.0 / COUNT(*) AS otp_pct

    FROM {{ ref('fact_flights') }} ff

    LEFT JOIN {{ ref('dim_carrier') }} dc
        ON ff.carrier_key = dc.carrier_key

    LEFT JOIN {{ ref('dim_date') }} dd
        ON ff.date_key = dd.date_key

    GROUP BY
        dc.carrier_key,
        dc.carrier_name,
        dc.carrier_type,
        dd.year
)

SELECT

    *,

    RANK() OVER(
        PARTITION BY year
        ORDER BY otp_pct DESC
    ) AS rank_otp,

    RANK() OVER(
        PARTITION BY year
        ORDER BY cancellation_rate ASC
    ) AS rank_cancellation,

    RANK() OVER(
        PARTITION BY year
        ORDER BY avg_arr_delay ASC
    ) AS rank_delay,

    (
        RANK() OVER(
            PARTITION BY year
            ORDER BY otp_pct DESC
        ) * 0.5

        +

        RANK() OVER(
            PARTITION BY year
            ORDER BY cancellation_rate ASC
        ) * 0.3

        +

        RANK() OVER(
            PARTITION BY year
            ORDER BY avg_arr_delay ASC
        ) * 0.2
    ) AS score_composite,

    carrier_type AS peer_group

FROM base