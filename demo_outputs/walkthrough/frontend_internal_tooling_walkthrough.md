# AgentGrid Frontend Walkthrough Script

## Title

AgentGrid: React/TypeScript Operational GenAI Dashboard

## 0:00–0:15 — Hook

"This is AgentGrid, a React/TypeScript operational dashboard for GenAI support workflows. It shows unsafe answer detection, eval-gate decisions, retry/error states, and incident escalation in one internal-tooling UI."

Show:
- dashboard dark mode
- Live Demo URL
- metrics cards

## 0:15–0:35 — Frontend Architecture

"The frontend uses reusable React components, typed API models, a typed API client, and request-state handling for loading, error, and retry states."

Show:
- dashboard/src/components
- dashboard/src/api/client.ts
- dashboard/src/hooks/useAsyncResource.ts

## 0:35–0:55 — Trace Viewer

"This trace viewer shows the actual agent workflow: triage, retrieval, MCP tool execution, eval gate, and AutoOps escalation."

Show:
- Trace tab
- retry warning
- eval-gate failure

## 0:55–1:15 — Eval Gate + Release State

"The eval gate blocks unsafe outputs. In this run, the answer is held because retrieval grounding is missing, and the release visualization shows the response blocked before reaching users."

Show:
- Eval Gate panel
- Release tab
- HOLD decision

## 1:15–1:35 — Incident Timeline

"The incident timeline turns the AI failure into an operational workflow: unsafe answer detected, hold decision, escalation artifact, RCA, and product feedback."

Show:
- Incident tab
- timeline stages

## 1:35–1:55 — Responsive / Product Polish

"The UI supports dark/light mode and responsive layouts, so it feels like a real internal dashboard rather than a backend-only demo."

Show:
- light mode
- mobile responsive screenshot

## 1:55–2:10 — Close

"AgentGrid combines backend GenAI orchestration with usable frontend UX: typed API integration, retry/error visualization, metrics cards, trace views, and escalation workflows."

End:
- GitHub repo
- live demo URL
