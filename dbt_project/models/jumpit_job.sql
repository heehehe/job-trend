{{ config(materialized = 'view') }}

SELECT DISTINCT job_category, job_name
FROM {{ source('crawling_data', 'jumpit') }}
