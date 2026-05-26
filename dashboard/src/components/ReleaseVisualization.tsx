import type { AgentRun } from "../types/agentgrid";

export function ReleaseVisualization({ run }: { run: AgentRun }) {
  const blocked = run.decision !== "ship";

  return (
    <section className="card release-card">
      <div className="section-header">
        <h2>Deployment / Release Visualization</h2>
        <p>Release gate outcome based on retrieval quality and unsafe-output checks.</p>
      </div>

      <div className="release-flow">
        <span>Generated answer</span>
        <span>→</span>
        <span>Eval gate</span>
        <span>→</span>
        <span className={blocked ? "blocked" : "passed"}>
          {blocked ? "Blocked / Hold" : "Released"}
        </span>
      </div>

      <p className="muted">
        Retrieval hit rate: {run.retrievalHitRate} · retries: {run.retries} · tool status: {run.toolCallStatus}
      </p>
    </section>
  );
}
