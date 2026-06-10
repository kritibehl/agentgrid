# Agent Version Benchmarking Report

## Purpose

Compare RAG workflow versions across retrieval quality, tool reliability, latency, cost, and eval-gate outcomes.

## Versions

| Version | Retrieval hit rate | Tool success | p95 latency | Cost/run | Eval pass rate | Gate |
|---|---:|---:|---:|---:|---:|---|
| agent_v1 | 0.72 | 0.74 | 1120 ms | $0.0210 | 0.70 | HOLD |
| agent_v2 | 0.84 | 0.89 | 940 ms | $0.0168 | 0.86 | PASS |

## Deltas

- retrieval hit rate: +0.12
- tool success rate: +0.15
- p95 latency: -180 ms
- cost per run: -$0.0042
- eval pass rate: +0.16

## Release decision

`PROMOTE_AGENT_V2`

## Safe claim

This benchmark compares simulated AgentGrid workflow versions using in-repo metrics. It does not claim production traffic or external customer deployment.
