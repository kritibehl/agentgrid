WITH first_seen AS (
  SELECT user_id, MIN(created_at) AS cohort_date
  FROM events
  GROUP BY user_id
),
activity AS (
  SELECT DISTINCT user_id, created_at
  FROM events
)
SELECT
  f.cohort_date,
  COUNT(DISTINCT f.user_id) AS cohort_users,
  COUNT(DISTINCT CASE WHEN a.created_at > f.cohort_date THEN a.user_id END) AS retained_users,
  ROUND(
    1.0 * COUNT(DISTINCT CASE WHEN a.created_at > f.cohort_date THEN a.user_id END)
    / COUNT(DISTINCT f.user_id), 3
  ) AS retention_rate
FROM first_seen f
LEFT JOIN activity a ON f.user_id = a.user_id
GROUP BY f.cohort_date
ORDER BY f.cohort_date;
