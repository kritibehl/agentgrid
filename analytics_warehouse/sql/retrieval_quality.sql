SELECT
  r.workflow_version,
  ROUND(AVG(re.retrieval_hit), 3) AS retrieval_hit_rate,
  ROUND(AVG(re.retrieved_doc_count), 2) AS avg_retrieved_doc_count
FROM retrieval_events re
JOIN runs r ON re.run_id = r.run_id
GROUP BY r.workflow_version
ORDER BY r.workflow_version;
