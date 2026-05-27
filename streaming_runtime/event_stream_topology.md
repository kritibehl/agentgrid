# AgentGrid Event Stream Topology

## Purpose

This artifact models a Kafka/Redis-Streams-style runtime topology for AgentGrid operational events.

## Event Flow

```text
user query event
→ retrieval event
→ eval-gate event
→ escalation event
→ latency telemetry event
→ window processor
→ consumer lag report / DLQ / replay workflow
Event Types
user_query
retrieval
eval_gate
escalation
latency_telemetry
Runtime Metrics
consumer lag
average processing latency
failed event count
retry count
dead-letter candidates
replay offset
backpressure risk
Scope

This is a deterministic streaming-runtime proof. It does not claim a deployed Kafka cluster.
