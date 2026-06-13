SELECT
  experiment_group,
  workflow_version,
  COUNT(*) AS runs,
  ROUND(AVG(completed), 3) AS completion_rate,
  ROUND(AVG(tool_success), 3) AS tool_success_rate,
  ROUND(AVG(eval_pass), 3) AS eval_pass_rate,
  ROUND(AVG(quality_score), 3) AS avg_quality_score
FROM agent_runs ar
JOIN events e ON ar.user_id = e.user_id
WHERE e.event_name = 'first_agent_run'
GROUP BY experiment_group, workflow_version
ORDER BY experiment_group;
