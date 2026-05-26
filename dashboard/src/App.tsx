import { useEffect, useState } from "react";
import { fetchIncidentTimeline, fetchLatestRun, fetchOperationalMetrics } from "./api/client";
import { EvalGatePanel } from "./components/EvalGatePanel";
import { IncidentTimeline } from "./components/IncidentTimeline";
import { MetricsCards } from "./components/MetricsCards";
import { ReleaseVisualization } from "./components/ReleaseVisualization";
import { StatusBadge } from "./components/StatusBadge";
import { TraceViewer } from "./components/TraceViewer";
import type { AgentRun, IncidentTimelineItem, OperationalMetric } from "./types/agentgrid";
import "./styles.css";

export default function App() {
  const [run, setRun] = useState<AgentRun | null>(null);
  const [timeline, setTimeline] = useState<IncidentTimelineItem[]>([]);
  const [metrics, setMetrics] = useState<OperationalMetric[]>([]);

  useEffect(() => {
    fetchLatestRun().then(setRun);
    fetchIncidentTimeline().then(setTimeline);
    fetchOperationalMetrics().then(setMetrics);
  }, []);

  if (!run) {
    return <main className="page">Loading AgentGrid dashboard...</main>;
  }

  return (
    <main className="page">
      <section className="hero">
        <div>
          <p className="eyebrow">AgentGrid Frontend</p>
          <h1>Operational GenAI Support Dashboard</h1>
          <p>
            Trace agent runs, inspect eval-gate decisions, monitor unsafe-output blocking,
            and follow incidents from detection to RCA and product feedback.
          </p>
        </div>

        <div className="hero-card">
          <p className="label">Latest decision</p>
          <StatusBadge decision={run.decision} />
          <p className="muted">Trace: {run.traceId}</p>
        </div>
      </section>

      <MetricsCards metrics={metrics} />

      <section className="grid two">
        <EvalGatePanel run={run} />
        <ReleaseVisualization run={run} />
      </section>

      <section className="grid two">
        <TraceViewer trace={run.trace} />
        <IncidentTimeline items={timeline} />
      </section>
    </main>
  );
}
