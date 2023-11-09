WITH selected_table AS (
    SELECT tech
    FROM job_trend.content_detail, UNNEST(tech_list) AS tech
    UNION DISTINCT
    SELECT '(all)' AS tech
)
SELECT DISTINCT tech
FROM selected_table
ORDER BY tech
