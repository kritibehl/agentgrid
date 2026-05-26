import { demoRun, incidentTimeline, metrics } from "../data/demoData";
import type { AgentRun, IncidentTimelineItem, OperationalMetric } from "../types/agentgrid";

const API_BASE = import.meta.env.VITE_AGENTGRID_API_URL || "";

async function safeFetch<T>(path: string, fallback: T): Promise<T> {
  if (!API_BASE) return fallback;

  try {
    const response = await fetch(`${API_BASE}${path}`);
    if (!response.ok) return fallback;
    return (await response.json()) as T;
  } catch {
    return fallback;
  }
}

export async function fetchLatestRun(): Promise<AgentRun> {
  return safeFetch<AgentRun>("/agent/runs/latest", demoRun);
}

export async function fetchIncidentTimeline(): Promise<IncidentTimelineItem[]> {
  return safeFetch<IncidentTimelineItem[]>("/incidents/timeline", incidentTimeline);
}

export async function fetchOperationalMetrics(): Promise<OperationalMetric[]> {
  return safeFetch<OperationalMetric[]>("/metrics/summary", metrics);
}
