SELECT
  created_at AS activity_date,
  COUNT(DISTINCT user_id) AS dau
FROM events
GROUP BY created_at
ORDER BY activity_date;

SELECT
  COUNT(DISTINCT user_id) AS wau,
  COUNT(*) AS weekly_events
FROM events
WHERE created_at >= '2026-05-20';
