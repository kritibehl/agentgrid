# 2-Minute Walkthrough Script: Unsafe Answer → RCA

## Title

AgentGrid + AutoOps: Turning Unsafe GenAI Support Answers into RCA and Product Feedback

## 0:00–0:15 — Problem

"Production GenAI support systems cannot just answer confidently. They need to know when not to answer. This demo shows what happens when an AI support workflow produces an unsupported deployment explanation."

Show:
- README hero
- architecture screenshot

## 0:15–0:35 — Unsafe Answer

"Here the answer claims the database cluster was definitely overloaded and recovered. But the available context only says there were DB timeout logs, missing runbook evidence, and no DB health snapshot."

Show:
- `demo_outputs/end_to_end_ai_support_incident.md`

## 0:35–0:55 — AgentGrid Detection

"AgentGrid detects unsupported root-cause claims and missing retrieval grounding. The eval gate blocks the response with a HOLD decision."

Show:
- `agentgrid_detection`
- unsupported claims
- eval gate safe_to_ship=false

## 0:55–1:15 — Escalation Artifact

"The system creates an escalation artifact with trace ID, decision ID, severity, owner, support action, and engineering summary."

Show:
- escalation artifact
- Jira-style payload

## 1:15–1:35 — AutoOps Classification

"AutoOps classifies this as a recurring issue family: missing retrieval grounding. It detects repeated patterns and routes it to the support reviewer queue."

Show:
- recurring issue family
- repeat_count
- customer analytics report

## 1:35–1:55 — RCA + Product Feedback

"The workflow generates an RCA summary, missing diagnostics, product feedback, and a safe support-response draft."

Show:
- RCA summary
- product feedback
- missing diagnostics

## 1:55–2:10 — Close

"This is the operational loop: unsafe answer detection, eval-gate blocking, escalation, recurring issue analytics, RCA, and product feedback. That is the core of production-style GenAI support operations."
