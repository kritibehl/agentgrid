# C# Support Decision API Contract

## POST /support/decision

Creates an AgentGrid support decision record.

### Request

```json
{
  "traceId": "trace_123",
  "issueType": "low_retrieval_hit_rate",
  "finalDecision": "hold",
  "reason": "insufficient_evidence",
  "supportAction": "Request missing docs context"
}
Response
{
  "decisionId": "decision_abc123",
  "traceId": "trace_123",
  "issueType": "low_retrieval_hit_rate",
  "finalDecision": "hold",
  "reason": "insufficient_evidence",
  "supportAction": "Request missing docs context",
  "createdAtUtc": "2026-05-18T00:00:00Z"
}
GET /support/decisions

Returns all support decisions stored in memory for this proof layer.

GET /support/decisions/{decisionId}

Returns a single support decision or decision_not_found.
