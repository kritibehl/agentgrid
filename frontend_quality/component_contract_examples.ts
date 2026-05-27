import type { AgentRun, IncidentTimelineItem, OperationalMetric } from "../dashboard/src/types/agentgrid";

export const metricContractExample: OperationalMetric = {
  label: "Unsafe outputs blocked",
  value: "1",
  delta: "+1 today"
};

export const runContractExample: AgentRun = {
  runId: "run_contract_001",
  traceId: "trace_contract_001",
  query: "Why did deployment fail?",
  decision: "hold",
  reason: "missing_retrieval_grounding",
  retrievalHitRate: 0.32,
  toolCallStatus: "retrying",
  retries: 2,
  latencyMs: 258,
  costUsd: 0.002,
  unsafeOutputBlocked: true,
  humanReviewRequired: true,
  trace: []
};

export const timelineContractExample: IncidentTimelineItem = {
  status: "detected",
  title: "Unsafe answer detected",
  detail: "Unsupported deployment explanation blocked by eval gate.",
  timestamp: "10:00:06"
};
