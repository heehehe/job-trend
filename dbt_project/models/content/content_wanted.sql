{{ config(materialized='view') }}

SELECT url,
       title,
       job_name,
       company_name,
       tech_list,
       CAST(NULL AS DATE) AS deadline,
       CAST(NULL AS STRING) AS location,
       main_work,
       CAST(NULL AS STRING) AS academic_background,
       CAST(NULL AS STRING) AS career,
       preferences,
       welfare,
       qualification,
       description
FROM {{ source('crawling_data', 'wanted') }}
