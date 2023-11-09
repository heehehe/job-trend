-- for pie chart
WITH selected_table AS (
    SELECT tech, job_name
    FROM job_trend.content_detail, UNNEST(tech_list) AS tech
)
SELECT job_name, count(*) AS cnt
FROM selected_table
WHERE (tech = '{{ TECH STACK }}' OR '{{ TECH STACK }}' = '(all)')
GROUP BY job_name, tech
ORDER BY cnt DESC
