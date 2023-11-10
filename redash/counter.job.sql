SELECT count(*) AS count
FROM job_trend.content_detail
WHERE (job_name = '{{ JOB }}' OR '{{ JOB }}' = '(all)')
