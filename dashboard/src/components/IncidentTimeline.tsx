import type { IncidentTimelineItem } from "../types/agentgrid";

export function IncidentTimeline({ items }: { items: IncidentTimelineItem[] }) {
  return (
    <section className="card">
      <div className="section-header">
        <h2>Incident Timeline</h2>
        <p>Unsafe answer → escalation → RCA → product feedback.</p>
      </div>

      <div className="timeline">
        {items.map((item) => (
          <div className="timeline-item" key={`${item.status}-${item.timestamp}`}>
            <div className="dot" />
            <div>
              <p className="label">{item.timestamp} · {item.status}</p>
              <h3>{item.title}</h3>
              <p>{item.detail}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
