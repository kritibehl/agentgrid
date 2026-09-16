SELECT
  workflow_version,
  COUNT(*) AS total_runs,
  SUM(CASE WHEN status IN ('hold', 'escalate') THEN 1 ELSE 0 END) AS failed_or_blocked_runs,
  ROUND(1.0 * SUM(CASE WHEN status IN ('hold', 'escalate') THEN 1 ELSE 0 END) / COUNT(*), 3) AS failure_rate
FROM runs
GROUP BY workflow_version
ORDER BY workflow_version;
