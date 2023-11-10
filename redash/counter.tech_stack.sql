SELECT count(*) AS count
FROM job_trend.content_detail, UNNEST(tech_list) AS tech
WHERE (tech = '{{ TECH STACK }}' OR '{{ TECH STACK }}' = '(all)')
