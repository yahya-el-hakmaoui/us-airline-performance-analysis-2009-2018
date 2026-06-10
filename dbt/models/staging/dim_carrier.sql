{{ config(materialized='table') }}

WITH carriers AS (

    SELECT DISTINCT
        OP_CARRIER

    FROM {{ ref('stg_flights') }}

)

SELECT

    ROW_NUMBER() OVER() AS carrier_key,

    OP_CARRIER AS iata_code,

    CASE
        WHEN OP_CARRIER = 'AA' THEN 'American Airlines'
        WHEN OP_CARRIER = 'DL' THEN 'Delta Air Lines'
        WHEN OP_CARRIER = 'UA' THEN 'United Airlines'
        WHEN OP_CARRIER = 'WN' THEN 'Southwest Airlines'
        WHEN OP_CARRIER = 'B6' THEN 'JetBlue Airways'
        WHEN OP_CARRIER = 'AS' THEN 'Alaska Airlines'
        WHEN OP_CARRIER = 'NK' THEN 'Spirit Airlines'
        WHEN OP_CARRIER = 'F9' THEN 'Frontier Airlines'
        WHEN OP_CARRIER = 'US' THEN 'US Airways'
        WHEN OP_CARRIER = 'CO' THEN 'Continental Airlines'
        WHEN OP_CARRIER = 'FL' THEN 'AirTran Airways'
        ELSE 'Unknown Carrier'
    END AS carrier_name,

    CASE
        WHEN OP_CARRIER IN ('AA', 'DL', 'UA') THEN 'Legacy'
        WHEN OP_CARRIER IN ('WN', 'B6') THEN 'Low Cost'
        WHEN OP_CARRIER IN ('NK', 'F9') THEN 'Ultra Low Cost'
        ELSE 'Other'
    END AS carrier_type,

    CASE
        WHEN OP_CARRIER = 'CO' THEN 'UA'
        WHEN OP_CARRIER = 'US' THEN 'AA'
        WHEN OP_CARRIER = 'FL' THEN 'WN'
        ELSE NULL
    END AS merged_into

FROM carriers