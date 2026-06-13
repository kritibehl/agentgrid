CREATE TABLE users (
  user_id TEXT PRIMARY KEY,
  account_type TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE tools (
  tool_id TEXT PRIMARY KEY,
  tool_name TEXT NOT NULL,
  tool_type TEXT NOT NULL,
  enabled INTEGER NOT NULL
);

CREATE TABLE runs (
  run_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  workflow_version TEXT NOT NULL,
  workflow_name TEXT NOT NULL,
  status TEXT NOT NULL,
  latency_ms INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE retrieval_events (
  event_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  query TEXT NOT NULL,
  retrieval_hit INTEGER NOT NULL,
  retrieved_doc_count INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY(run_id) REFERENCES runs(run_id)
);

CREATE TABLE eval_scores (
  eval_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  groundedness_score REAL NOT NULL,
  hallucination_risk REAL NOT NULL,
  eval_decision TEXT NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY(run_id) REFERENCES runs(run_id)
);

CREATE TABLE tool_calls (
  call_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  tool_id TEXT NOT NULL,
  tool_success INTEGER NOT NULL,
  latency_ms INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY(run_id) REFERENCES runs(run_id),
  FOREIGN KEY(tool_id) REFERENCES tools(tool_id)
);
