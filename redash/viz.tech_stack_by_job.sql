-- for sanky & sunburst
WITH job_name_rank AS (
  SELECT job_name
  FROM job_trend.content_detail
  GROUP BY job_name
  ORDER BY COUNT(*) DESC
  LIMIT 15
),
tech_rank AS (
  SELECT tech
  FROM job_trend.content_detail,
  UNNEST(tech_list) as tech
  GROUP BY tech
  ORDER BY COUNT(*) DESC
  LIMIT 15
),
filtered_content AS (
  SELECT
    job_name,
    tech,
    COUNT(*) AS value
  FROM
    job_trend.content_detail,
    UNNEST(tech_list) as tech
  WHERE
    job_name IN (SELECT job_name FROM job_name_rank)
    AND tech IN (SELECT tech FROM tech_rank)
  GROUP BY
    job_name,
    tech
)
SELECT
  job_name AS stage1,
  tech AS stage2,
  SUM(value) AS value
FROM
  filtered_content
GROUP BY
  stage1,
  stage2
ORDER BY
  value DESC
