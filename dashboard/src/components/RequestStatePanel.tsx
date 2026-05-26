export function LoadingPanel({ label }: { label: string }) {
  return (
    <section className="card state-panel">
      <div className="spinner" />
      <strong>{label}</strong>
      <p className="muted">Loading dashboard data...</p>
    </section>
  );
}

export function ErrorPanel({
  message,
  retryCount,
  onRetry
}: {
  message: string;
  retryCount: number;
  onRetry: () => void;
}) {
  return (
    <section className="card state-panel error-panel">
      <strong>Dashboard request failed</strong>
      <p>{message}</p>
      <p className="muted">Retry attempts: {retryCount}</p>
      <button className="button" onClick={onRetry}>Retry request</button>
    </section>
  );
}
