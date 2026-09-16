# Agent Failure Modes

| Failure mode | Detection signal | Response |
|---|---|---|
| Retrieval miss | no grounding context | hold |
| Tool timeout | retry threshold exceeded | retry / escalate |
| Hallucinated claim | unsupported by evidence | block |
| Schema violation | missing required field | fail validation |
| Unsafe action | high-risk operation | human review |
| Eval regression | quality drop | hold release |
