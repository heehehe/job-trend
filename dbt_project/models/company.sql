{{ config(materialized = 'table') }}

WITH
    company_jumpit AS (
        SELECT DISTINCT company_url, company_name
        FROM {{ ref('company_jumpit') }}
    ),
    company_wanted AS (
        SELECT DISTINCT company_url, company_name
        FROM {{ ref('company_wanted') }}
    )

SELECT company_jumpit.company_url as jumpit_url,
       company_wanted.company_url as wanted_url,
       company_jumpit.job_name as name
FROM company_jumpit, company_wanted
GROUP BY name
