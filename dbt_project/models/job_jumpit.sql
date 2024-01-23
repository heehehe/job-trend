{{ config(materialized = 'view') }}

WITH job_table AS (
    SELECT DISTINCT job_category, job_name
    FROM {{ source('crawling_data', 'jumpit') }}
)
SELECT CONCAT('jumpit_', job_category) AS job_category, job_name
FROM job_table
