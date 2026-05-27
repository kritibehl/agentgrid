
Stream Replay Workflow
Goal

Replay failed AgentGrid operational events from a known offset.

Replay Flow
identify failed event
→ locate partition + offset
→ inspect payload and trace_id
→ replay retrieval/eval/escalation event
→ regenerate telemetry report
→ confirm no repeated DLQ entry
Example

Failed event:

event_id: evt_006
type: retrieval
offset: 15

Replay action:

replay from offset 15
regenerate retrieval result
rerun eval gate
update consumer lag report
Why This Matters

Replay workflows make AI-agent event processing auditable and recoverable after tool failures, retrieval failures, or telemetry gaps.
