# AgentGrid Walkthrough Video Script

## Title

AgentGrid: Production-Style GenAI Operations Platform

## 0:00–0:15 — Hook

"This is AgentGrid, a production-style GenAI operations platform that detects unsafe AI support answers, blocks unsupported outputs, routes escalations, and turns incidents into RCA and product feedback."

Show:
- dashboard hero
- metrics cards
- latest HOLD decision

## 0:15–0:40 — Trace Viewer

"Here is a real trace from an unsafe deployment-support answer. The user asked why deployment failed, but the generated answer claimed the database was definitely overloaded without enough evidence."

Show:
- trace viewer
- trace_id
- retrieval warning
- tool retry
- eval-gate failure

## 0:40–1:05 — Eval Gate and HOLD Decision

"AgentGrid evaluates retrieval grounding, unsupported-detail risk, tool-call status, and whether human review is required. In this case, the eval gate blocks the answer and returns HOLD."

Show:
- eval-gate panel
- HOLD badge
- unsafe output blocked = yes
- human review required = yes

## 1:05–1:30 — Escalation and Human Review

"Because the answer is unsafe, AgentGrid routes the run into a human-review queue and creates an escalation artifact with trace ID, decision ID, owner, and support action."

Show:
- incident timeline
- escalation step
- human review queue
- support action

## 1:30–1:55 — RCA and Product Feedback

"AutoOps classifies this as a recurring issue family: missing retrieval grounding. It generates RCA, missing diagnostics, and product feedback to improve retrieval coverage."

Show:
- RCA section
- product feedback
- recurring issue family
- repeat count

## 1:55–2:15 — Deployment / Release State

"The release visualization shows that the unsafe response was blocked before reaching users. This is the key operational AI loop: answer generation, evaluation, escalation, RCA, and feedback."

Show:
- deployment/release visualization
- blocked / hold state
- metrics cards

## 2:15–2:30 — Close

"AgentGrid combines multi-agent orchestration, MCP-style tools, eval gates, runtime traces, review queues, and frontend UX into one operational GenAI support system."

End on:
- README architecture image
- GitHub repo
- live dashboard link
