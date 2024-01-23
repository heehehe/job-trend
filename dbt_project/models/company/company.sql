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
       COALESCE(company_jumpit.company_name, company_wanted.company_name) AS name
FROM company_jumpit
FULL OUTER JOIN company_wanted
ON company_jumpit.company_name = company_wanted.company_name
