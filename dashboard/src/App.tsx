import { useMemo, useState } from "react";
import { fetchIncidentTimeline, fetchLatestRun, fetchOperationalMetrics } from "./api/client";
import { BarChart } from "./components/BarChart";
import { EvalGatePanel } from "./components/EvalGatePanel";
import { ErrorPanel, LoadingPanel } from "./components/RequestStatePanel";
import { IncidentTimeline } from "./components/IncidentTimeline";
import { MetricsCards } from "./components/MetricsCards";
import { ReleaseVisualization } from "./components/ReleaseVisualization";
import { StatusBadge } from "./components/StatusBadge";
import { TraceViewer } from "./components/TraceViewer";
import { useAsyncResource } from "./hooks/useAsyncResource";
import "./styles.css";

type View = "overview" | "trace" | "incident" | "release";

export default function App() {
  const [view, setView] = useState<View>("overview");
  const [theme, setTheme] = useState<"dark" | "light">("dark");

  const runState = useAsyncResource(fetchLatestRun);
  const timelineState = useAsyncResource(fetchIncidentTimeline);
  const metricsState = useAsyncResource(fetchOperationalMetrics);

  const run = runState.data;
  const timeline = timelineState.data ?? [];
  const metrics = metricsState.data ?? [];

  const chartValues = useMemo(() => {
    if (!run) return [];
    return [
      { label: "Retrieval", value: Math.round(run.retrievalHitRate * 100), max: 100 },
      { label: "Tool success", value: run.toolCallStatus === "success" ? 100 : 55, max: 100 },
      { label: "Latency score", value: Math.max(10, 100 - Math.round(run.latencyMs / 10)), max: 100 },
      { label: "Human review", value: run.humanReviewRequired ? 100 : 0, max: 100 }
    ];
  }, [run]);

  if (runState.loading || timelineState.loading || metricsState.loading) {
    return (
      <main className={`page theme-${theme}`}>
        <LoadingPanel label="Preparing AgentGrid dashboard" />
      </main>
    );
  }

  if (runState.error || timelineState.error || metricsState.error || !run) {
    return (
      <main className={`page theme-${theme}`}>
        <ErrorPanel
          message={runState.error || timelineState.error || metricsState.error || "Missing run data"}
          retryCount={runState.retryCount + timelineState.retryCount + metricsState.retryCount}
          onRetry={() => {
            runState.reload();
            timelineState.reload();
            metricsState.reload();
          }}
        />
      </main>
    );
  }

  return (
    <main className={`page theme-${theme}`}>
      <nav className="top-nav">
        <strong>AgentGrid</strong>
        <div className="nav-actions">
          {(["overview", "trace", "incident", "release"] as View[]).map((item) => (
            <button
              className={view === item ? "nav-button active" : "nav-button"}
              key={item}
              onClick={() => setView(item)}
            >
              {item}
            </button>
          ))}
          <button
            className="nav-button"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          >
            {theme === "dark" ? "Light" : "Dark"}
          </button>
        </div>
      </nav>

      <section className="hero">
        <div>
          <p className="eyebrow">Operational GenAI Frontend</p>
          <h1>AgentGrid Support Operations</h1>
          <p>
            Trace agent runs, inspect eval-gate decisions, monitor unsafe-output blocking,
            and follow incidents from detection to RCA and product feedback.
          </p>
          <p className="live-link">Live Demo: https://agentgrid-seven.vercel.app</p>
        </div>

        <div className="hero-card">
          <p className="label">Latest decision</p>
          <StatusBadge decision={run.decision} />
          <p className="muted">Trace: {run.traceId}</p>
          <p className="muted">Retries: {run.retries} · Tool: {run.toolCallStatus}</p>
        </div>
      </section>

      {view === "overview" && (
        <>
          <MetricsCards metrics={metrics} />
          <section className="grid two">
            <BarChart title="Operational Health" values={chartValues} />
            <EvalGatePanel run={run} />
          </section>
        </>
      )}

      {view === "trace" && (
        <section className="grid two">
          <TraceViewer trace={run.trace} />
          <BarChart title="Trace Quality Signals" values={chartValues} />
        </section>
      )}

      {view === "incident" && (
        <section className="grid two">
          <IncidentTimeline items={timeline} />
          <EvalGatePanel run={run} />
        </section>
      )}

      {view === "release" && (
        <section className="grid two">
          <ReleaseVisualization run={run} />
          <BarChart title="Release Readiness" values={chartValues} />
        </section>
      )}
    </main>
  );
}
