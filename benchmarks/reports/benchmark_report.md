# GenAI Workflow Benchmark Report

## Goal

Compare model behavior across controlled GenAI operational-support workflows.

## Models Evaluated

- Gemini Flash
- GPT-4o-mini
- Claude Haiku

## Evaluation Areas

- retrieval grounding
- unsupported-answer risk
- latency
- estimated cost/request
- tool-call quality

## Scenarios

- retrieval grounding
- unsupported-answer handling
- operational support workflows
- escalation recommendation quality

## Controlled Benchmark Summary

| Model | Groundedness | Avg Latency (ms) | Avg Cost | Tool-call Quality | Unsupported Answers |
|---|---|---|---|---|---|
| GPT-4o-mini | 0.93 | 960 | 0.0029 | 0.92 | 0 |
| Gemini Flash | 0.905 | 805 | 0.0020 | 0.89 | 0 |
| Claude Haiku | 0.89 | 745 | 0.0018 | 0.86 | 0 |

## Observations

- GPT-4o-mini produced the strongest grounding and tool-call quality in these controlled scenarios.
- Gemini Flash showed lower latency while maintaining strong grounding.
- Claude Haiku produced the lowest estimated cost and latency.

## Scope and Limitations

This is a controlled evaluation proof for operational GenAI workflow experiments. It is not a large-scale scientific benchmark or production deployment study.

## Why This Matters

Production GenAI systems require evaluation discipline across:
- groundedness
- unsupported-answer risk
- escalation behavior
- latency
- operational cost
- tool orchestration quality
