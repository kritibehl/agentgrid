# AgentGrid AI Reliability Invariants

AgentGrid verifies reliability properties under deterministic fault injection rather than assuming successful agent behavior.

## Invariant 1 — Unsupported claims cannot silently ship

Generated output unsupported by retrieved evidence must not terminate with `SHIP`.

## Invariant 2 — Missing grounding is contained

A retrieval miss must terminate in an explicit containment path such as `HOLD`.

## Invariant 3 — Failed tools are not evidence

Malformed, exceptional, repeatedly failed, or partially failed required tool calls cannot be interpreted as successful evidence.

## Invariant 4 — Transient failures may recover safely

A retryable transient tool failure may return to `SHIP` only after a successful retry.

## Invariant 5 — Healthy requests remain releasable

A grounded request with healthy dependencies must not be unnecessarily held or escalated.

## Invariant 6 — Every terminal decision is explainable

Each run records retrieval state, tool execution state, model validation signals, evaluation outcome, terminal route, and decision reason.

## Verification

These invariants are exercised by:

- `reliability_benchmark/corpus/adversarial_v1.json`
- `tests/test_reliability_benchmark.py`
- `reliability_benchmark/reports/traces/`
