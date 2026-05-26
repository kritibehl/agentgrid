import type { Decision } from "../types/agentgrid";

export function StatusBadge({ decision }: { decision: Decision }) {
  const className =
    decision === "ship"
      ? "badge badge-ship"
      : decision === "hold"
        ? "badge badge-hold"
        : "badge badge-escalate";

  return <span className={className}>{decision.toUpperCase()}</span>;
}
