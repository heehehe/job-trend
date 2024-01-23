{{ config(materialized = 'table') }}

WITH
    job_jumpit AS (
        SELECT DISTINCT job_category, job_name
        FROM {{ ref('job_jumpit') }}
    ),
    job_wanted AS (
        SELECT DISTINCT job_category, job_name
        FROM {{ ref('job_wanted') }}
    )

SELECT job_jumpit.job_category as jumpit_category,
       job_wanted.job_category as wanted_category,
       job_jumpit.job_name as name
FROM job_jumpit, job_wanted
GROUP BY name
