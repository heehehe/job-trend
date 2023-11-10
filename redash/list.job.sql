SELECT '(all)' AS job_name
UNION DISTINCT
SELECT DISTINCT job_name
FROM job_trend.content_detail
ORDER BY job_name
