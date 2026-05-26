import type { AgentRun } from "../types/agentgrid";
import { StatusBadge } from "./StatusBadge";

export function EvalGatePanel({ run }: { run: AgentRun }) {
  return (
    <section className="card">
      <div className="section-header">
        <h2>Evaluation Gate</h2>
        <p>Blocks unsafe or weakly grounded GenAI support outputs.</p>
      </div>

      <div className="eval-grid">
        <div>
          <p className="label">Decision</p>
          <StatusBadge decision={run.decision} />
        </div>
        <div>
          <p className="label">Reason</p>
          <strong>{run.reason}</strong>
        </div>
        <div>
          <p className="label">Unsafe output blocked</p>
          <strong>{run.unsafeOutputBlocked ? "Yes" : "No"}</strong>
        </div>
        <div>
          <p className="label">Human review</p>
          <strong>{run.humanReviewRequired ? "Required" : "Not required"}</strong>
        </div>
      </div>
    </section>
  );
}
