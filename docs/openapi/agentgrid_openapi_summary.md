# AgentGrid OpenAPI Summary

## Core APIs

| Endpoint | Purpose |
|---|---|
| POST /agent/run | Run GenAI support workflow |
| GET /metrics | Prometheus-style metrics |
| POST /jobs/validation | Create async validation job |
| GET /jobs/{job_id} | Inspect job status |
| POST /redis/jobs/validation | Create Redis-backed validation job |
| GET /redis/dead-letter | Inspect Redis dead-letter queue |
| GET /auth/demo-token/{role} | Generate demo role token |
| POST /review/action | Run RBAC-protected reviewer action |
| GET /audit/events | Inspect support-decision audit log |

## Dashboard Flow

```text
User query
→ RAG context retrieval
→ tool-call validation
→ eval gate
→ ship / hold / escalate
→ AutoOps event
→ audit trail / metrics
Scope

This is a documented API-contract layer for demo and portfolio review, not a production API gateway.
