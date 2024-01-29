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
       COALESCE(job_jumpit.job_name, job_wanted.job_name) AS name
FROM job_jumpit
FULL OUTER JOIN job_wanted
ON job_jumpit.job_name = job_wanted.job_name
