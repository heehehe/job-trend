{{ config(materialized='table') }}

SELECT *
FROM {{ ref('content_jumpit') }}

UNION ALL

SELECT *
FROM {{ ref('content_wanted') }}

UNION ALL

SELECT *
FROM {{ ref('content_jobplanet') }}
