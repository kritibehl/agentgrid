export type Decision = "ship" | "hold" | "escalate";

export type IncidentStatus =
  | "detected"
  | "triaged"
  | "escalated"
  | "rca_generated"
  | "product_feedback_created";

export interface TraceStep {
  name: string;
  status: "success" | "warning" | "failed";
  detail: string;
  timestamp: string;
}

export interface AgentRun {
  runId: string;
  traceId: string;
  query: string;
  decision: Decision;
  reason: string;
  retrievalHitRate: number;
  toolCallStatus: "success" | "retrying" | "failed";
  retries: number;
  latencyMs: number;
  costUsd: number;
  unsafeOutputBlocked: boolean;
  humanReviewRequired: boolean;
  trace: TraceStep[];
}

export interface OperationalMetric {
  label: string;
  value: string;
  delta: string;
}

export interface IncidentTimelineItem {
  status: IncidentStatus;
  title: string;
  detail: string;
  timestamp: string;
}
