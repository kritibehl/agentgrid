-- DAU-style workflow usage
SELECT
  created_at AS activity_date,
  COUNT(DISTINCT user_id) AS active_users,
  COUNT(*) AS workflow_runs
FROM runs
GROUP BY created_at
ORDER BY activity_date;

-- WAU-style workflow usage over sample period
SELECT
  COUNT(DISTINCT user_id) AS weekly_active_users,
  COUNT(*) AS weekly_workflow_runs
FROM runs
WHERE created_at >= '2026-05-20';
