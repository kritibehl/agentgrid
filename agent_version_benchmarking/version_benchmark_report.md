# Agent Version Benchmark Report

## Summary

| Field | Value |
|---|---|
| Winner | agent_v2 |
| Release decision | ship_agent_v2 |
| Regressions | none |

## Metric Comparison

| Metric | agent_v1 | agent_v2 | Delta | Percent Change | Improved |
|---|---:|---:|---:|---:|---|
| retrieval_hit_rate | 0.76 | 0.89 | 0.13 | 17.11% | True |
| tool_success_rate | 0.88 | 0.94 | 0.06 | 6.82% | True |
| p95_latency_ms | 940 | 820 | -120 | -12.77% | True |
| cost_per_run_usd | 0.018 | 0.014 | -0.004 | -22.22% | True |
| eval_pass_rate | 0.71 | 0.84 | 0.13 | 18.31% | True |

## What This Proves

This benchmark compares RAG/agent workflow versions across retrieval quality, tool success, p95 latency, cost per run, and eval-gate pass rate.

## Scope

This is a deterministic benchmark artifact. It does not claim production traffic or live A/B testing.
