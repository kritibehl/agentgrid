SELECT
  u.segment,
  COUNT(DISTINCT u.user_id) AS users,
  COUNT(ar.run_id) AS agent_runs,
  ROUND(AVG(ar.completed), 3) AS workflow_completion_rate,
  ROUND(AVG(ar.tool_success), 3) AS tool_success_rate,
  ROUND(AVG(ar.quality_score), 3) AS avg_quality_score
FROM users u
LEFT JOIN agent_runs ar ON u.user_id = ar.user_id
GROUP BY u.segment
ORDER BY u.segment;
