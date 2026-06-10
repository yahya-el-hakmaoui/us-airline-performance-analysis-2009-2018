{{ config(materialized='table') }}

WITH dates AS (

    SELECT DISTINCT

        CAST(FL_DATE AS DATE) AS full_date

    FROM {{ ref('stg_flights') }}

)

SELECT

    ROW_NUMBER() OVER() AS date_key,

    full_date,

    EXTRACT(YEAR FROM full_date) AS year,

    EXTRACT(MONTH FROM full_date) AS month,

    EXTRACT(QUARTER FROM full_date) AS quarter,

    EXTRACT(DAYOFWEEK FROM full_date) AS day_of_week,

    CASE
        WHEN EXTRACT(DAYOFWEEK FROM full_date) IN (0, 6)
        THEN TRUE
        ELSE FALSE
    END AS is_weekend

FROM dates