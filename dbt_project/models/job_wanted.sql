{{ config(materialized = 'view') }}

WITH job_table AS (
    SELECT DISTINCT job_category, job_name
    FROM {{ source('crawling_data', 'wanted') }}
)
SELECT job_category, --CONCAT('wanted_', job_category) AS job_category,
       job_name
FROM job_table
