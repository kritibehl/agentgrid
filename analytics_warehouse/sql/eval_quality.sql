SELECT
  r.workflow_version,
  ROUND(AVG(e.groundedness_score), 3) AS avg_groundedness_score,
  ROUND(AVG(e.hallucination_risk), 3) AS avg_hallucination_risk,
  SUM(CASE WHEN e.eval_decision = 'ship' THEN 1 ELSE 0 END) AS ship_decisions,
  SUM(CASE WHEN e.eval_decision IN ('hold', 'escalate') THEN 1 ELSE 0 END) AS blocked_decisions
FROM eval_scores e
JOIN runs r ON e.run_id = r.run_id
GROUP BY r.workflow_version
ORDER BY r.workflow_version;
