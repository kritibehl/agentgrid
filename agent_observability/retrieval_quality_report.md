# Agent Observability Retrieval Quality Report

## Metrics Tracked

- trace count
- retrieval hit rate
- tool success rate
- p95 latency
- cost per run
- eval-gate outcomes
- trace-level failure reasons

## Example Observability Output

| Metric | Value |
|---|---:|
| retrieval_hit_rate | 0.75 |
| tool_success_rate | 0.75 |
| p95_latency_ms | 940 |
| avg_cost_per_run_usd | 0.0168 |

## Why This Matters

AgentGrid needs observability at the trace level so failures can be tied back to retrieval misses, tool failures, eval-gate outcomes, latency, and cost.

## Scope

This is a deterministic observability proof. It does not claim production Langfuse, Phoenix, or enterprise observability deployment.
