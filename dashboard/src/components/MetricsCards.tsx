import type { OperationalMetric } from "../types/agentgrid";

export function MetricsCards({ metrics }: { metrics: OperationalMetric[] }) {
  return (
    <section className="grid cards">
      {metrics.map((metric) => (
        <article className="card metric-card" key={metric.label}>
          <p className="label">{metric.label}</p>
          <h2>{metric.value}</h2>
          <p className="muted">{metric.delta}</p>
        </article>
      ))}
    </section>
  );
}
