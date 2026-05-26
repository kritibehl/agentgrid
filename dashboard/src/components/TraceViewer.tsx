import type { TraceStep } from "../types/agentgrid";

export function TraceViewer({ trace }: { trace: TraceStep[] }) {
  return (
    <section className="card">
      <div className="section-header">
        <h2>Trace Viewer</h2>
        <p>Agent execution path with retries, warnings, and eval-gate outcome.</p>
      </div>

      <div className="trace-list">
        {trace.map((step) => (
          <div className={`trace-step ${step.status}`} key={`${step.name}-${step.timestamp}`}>
            <div>
              <strong>{step.name}</strong>
              <p>{step.detail}</p>
            </div>
            <span>{step.timestamp}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
