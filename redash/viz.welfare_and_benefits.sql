-- for wordcloud
SELECT tag
FROM job_trend.content_detail, UNNEST(tag_name) AS tag, UNNEST(tech_list) AS tech
WHERE ARRAY_LENGTH(tag_name) > 0
    AND (job_name = '{{ JOB }}' OR '{{ JOB }}' = '(all)')
    AND (tech = '{{ TECH STACK }}' OR '{{ TECH STACK }}' = '(all)')
