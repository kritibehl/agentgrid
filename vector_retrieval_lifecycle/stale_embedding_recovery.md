# Stale Embedding Recovery

## Scenario

Operational documentation changed, but the vector index still referenced outdated embeddings.

## Risk

The agent retrieved old escalation guidance and generated unsupported operational suggestions.

## Recovery Flow

```text
detect retrieval drift
→ identify stale embeddings
→ regenerate embeddings
→ refresh vector index
→ invalidate retrieval cache
→ rerun retrieval benchmark
→ confirm improved retrieval grounding
Example Indicators
reduced retrieval hit rate
repeated retrieval misses
increased HOLD decisions
recurring unsupported-detail detections
Result

Embedding refresh and cache invalidation restored retrieval grounding behavior.
