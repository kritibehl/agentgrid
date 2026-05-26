import type { AgentRun, IncidentTimelineItem, OperationalMetric } from "../types/agentgrid";

export const demoRun: AgentRun = {
  runId: "run_e2e_001",
  traceId: "trace_e2e_001",
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
  trace: [
    {
      name: "Triage Agent",
      status: "success",
      detail: "Classified issue as deployment-support incident",
      timestamp: "10:00:01"
    },
    {
      name: "Retrieval Agent",
      status: "warning",
      detail: "DB timeout logs found, but saturation runbook missing",
      timestamp: "10:00:03"
    },
    {
      name: "MCP Tool Server",
      status: "warning",
      detail: "query_metrics retried twice before partial result",
      timestamp: "10:00:05"
    },
    {
      name: "Eval Gate",
      status: "failed",
      detail: "Blocked unsupported root-cause claim",
      timestamp: "10:00:06"
    },
    {
      name: "AutoOps Escalation",
      status: "success",
      detail: "Routed to support_reviewer_queue",
      timestamp: "10:00:08"
    }
  ]
};

export const metrics: OperationalMetric[] = [
  { label: "Unsafe outputs blocked", value: "1", delta: "+1 today" },
  { label: "Retrieval hit rate", value: "0.32", delta: "below threshold" },
  { label: "p95 latency", value: "258 ms", delta: "local eval" },
  { label: "Cost / request", value: "$0.002", delta: "benchmark estimate" }
];

export const incidentTimeline: IncidentTimelineItem[] = [
  {
    status: "detected",
    title: "Unsafe answer detected",
    detail: "Answer claimed DB overload without supporting evidence.",
    timestamp: "10:00:06"
  },
  {
    status: "triaged",
    title: "Eval gate blocked response",
    detail: "Decision changed to HOLD due to missing retrieval grounding.",
    timestamp: "10:00:07"
  },
  {
    status: "escalated",
    title: "Escalation artifact created",
    detail: "Jira-style issue routed to ai_support_engineering.",
    timestamp: "10:00:09"
  },
  {
    status: "rca_generated",
    title: "RCA summary generated",
    detail: "Probable cause framed as missing retrieval grounding.",
    timestamp: "10:00:12"
  },
  {
    status: "product_feedback_created",
    title: "Product feedback created",
    detail: "Improve deployment-failure runbook retrieval coverage.",
    timestamp: "10:00:14"
  }
];
