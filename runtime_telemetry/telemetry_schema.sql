CREATE TABLE runtime_metrics (
  run_id TEXT PRIMARY KEY,
  workflow_name TEXT,
  model_name TEXT,
  prompt_tokens INTEGER,
  completion_tokens INTEGER,
  estimated_cost REAL,
  latency_ms INTEGER,
  tool_calls INTEGER,
  retry_count INTEGER,
  failure_reason TEXT,
  eval_status TEXT,
  release_decision TEXT
);
