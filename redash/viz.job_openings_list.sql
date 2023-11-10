-- for table
SELECT company_name, title, url, FORMAT_DATE('%Y/%m/%d', deadline) AS end_date
FROM job_trend.content_detail
WHERE (job_name = '{{ JOB }}' OR '{{ JOB }}' = '(all)')
    AND title != ''
    AND (deadline <= '{{ DEADLINE }}' or deadline IS NULL)
ORDER BY deadline DESC
