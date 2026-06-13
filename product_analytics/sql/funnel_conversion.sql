WITH funnel AS (
  SELECT
    user_id,
    MAX(CASE WHEN event_name = 'signup' THEN 1 ELSE 0 END) AS signed_up,
    MAX(CASE WHEN event_name = 'first_agent_run' THEN 1 ELSE 0 END) AS activated,
    MAX(CASE WHEN event_name = 'completed_workflow' THEN 1 ELSE 0 END) AS completed
  FROM events
  GROUP BY user_id
)
SELECT
  SUM(signed_up) AS signed_up,
  SUM(activated) AS activated,
  SUM(completed) AS completed,
  ROUND(1.0 * SUM(activated) / SUM(signed_up), 3) AS activation_rate,
  ROUND(1.0 * SUM(completed) / SUM(signed_up), 3) AS completion_rate
FROM funnel;
