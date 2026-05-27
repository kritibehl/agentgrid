# Component Contracts

## MetricsCards

Input:
- `OperationalMetric[]`

Contract:
- renders label
- renders value
- renders delta

## TraceViewer

Input:
- `TraceStep[]`

Contract:
- renders agent/tool step
- renders success/warning/failed state
- renders timestamp and detail

## EvalGatePanel

Input:
- `AgentRun`

Contract:
- renders decision badge
- renders reason
- renders unsafe-output block state
- renders human-review requirement

## IncidentTimeline

Input:
- `IncidentTimelineItem[]`

Contract:
- renders incident status sequence
- shows RCA/product-feedback progression

## ReleaseVisualization

Input:
- `AgentRun`

Contract:
- shows generated answer → eval gate → blocked/released state
- surfaces retrieval hit rate, retry count, and tool status
