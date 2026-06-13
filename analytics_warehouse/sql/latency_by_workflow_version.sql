SELECT
  workflow_version,
  workflow_name,
  COUNT(*) AS run_count,
  ROUND(AVG(latency_ms), 2) AS avg_latency_ms,
  MAX(latency_ms) AS max_latency_ms
FROM runs
GROUP BY workflow_version, workflow_name
ORDER BY workflow_version, workflow_name;
