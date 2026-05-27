# Retrieval Cache Behavior

## Goal

Reduce retrieval latency while preventing stale operational context.

## Cache Workflow

```text
retrieval request
→ cache lookup
→ cache hit or miss
→ retrieval execution
→ cache update
→ cache invalidation on refresh
Cached Artifacts
retrieval chunks
support summaries
incident embeddings
runbook search results
Cache Invalidation Triggers
runbook update
embedding refresh
retrieval drift detection
repeated unsupported-answer incidents
Operational Metrics
cache hit rate
cache miss rate
retrieval latency
stale cache incidents
