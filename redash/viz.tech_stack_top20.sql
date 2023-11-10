-- for bar chart
WITH selected_table AS (
    SELECT tech, job_name
    FROM job_trend.content_detail, UNNEST(tech_list) AS tech
)
SELECT tech, count(*) AS cnt
FROM selected_table
WHERE (job_name = '{{ JOB }}' OR '{{ JOB }}' = '(all)')
GROUP BY job_name, tech
ORDER BY job_name, cnt DESC
LIMIT 20
