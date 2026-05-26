export function BarChart({
  title,
  values
}: {
  title: string;
  values: Array<{ label: string; value: number; max?: number }>;
}) {
  return (
    <section className="card">
      <div className="section-header">
        <h2>{title}</h2>
        <p>Operational trend view for dashboard scanning.</p>
      </div>

      <div className="bar-list">
        {values.map((item) => {
          const max = item.max ?? 1;
          const width = `${Math.min(100, Math.round((item.value / max) * 100))}%`;

          return (
            <div className="bar-row" key={item.label}>
              <div className="bar-label">
                <span>{item.label}</span>
                <strong>{item.value}</strong>
              </div>
              <div className="bar-track">
                <div className="bar-fill" style={{ width }} />
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
