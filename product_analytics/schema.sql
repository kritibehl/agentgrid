CREATE TABLE users (
  user_id TEXT PRIMARY KEY,
  segment TEXT NOT NULL,
  signup_date TEXT NOT NULL
);

CREATE TABLE events (
  event_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  event_name TEXT NOT NULL,
  workflow_version TEXT NOT NULL,
  experiment_group TEXT NOT NULL,
  success INTEGER NOT NULL,
  latency_ms INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE agent_runs (
  run_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  workflow_version TEXT NOT NULL,
  completed INTEGER NOT NULL,
  tool_success INTEGER NOT NULL,
  eval_pass INTEGER NOT NULL,
  quality_score REAL NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(user_id)
);
