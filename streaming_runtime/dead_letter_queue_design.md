
Dead-Letter Queue Design
DLQ Criteria

Events are routed to the dead-letter queue when:

retry count exceeds threshold
payload schema is invalid
required trace_id is missing
downstream tool execution repeatedly fails
event cannot be mapped to a known agent workflow stage
DLQ Payload
{
  "event_id": "evt_006",
  "event_type": "retrieval",
  "reason": "failed_event",
  "trace_id": "trace_stream_001",
  "retry_count": 3,
  "replay_offset": 15
}
Recovery Path
Inspect failed event.
Validate schema.
Patch missing metadata if safe.
Replay from offset.
Confirm eval-gate and escalation outputs.
