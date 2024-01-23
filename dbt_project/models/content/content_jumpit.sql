{{ config(materialized='view') }}

SELECT url,
       title,
       job_name,
       company_name,
       tech_list,
       deadline,
       location,
       CAST(NULL AS ARRAY<STRING>) AS main_work,
       academic_background,
       career,
       CAST(NULL AS ARRAY<STRING>) AS preferences,
       CAST(NULL AS ARRAY<STRING>) AS welfare,
       CAST(NULL AS ARRAY<STRING>) AS qualification,
       CAST(NULL AS ARRAY<STRING>) AS description
FROM {{ source('crawling_data', 'jumpit') }}
