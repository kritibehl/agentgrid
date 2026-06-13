import csv
import json
import sqlite3
from pathlib import Path


ROOT = Path("analytics_warehouse")
DB_PATH = ROOT / "agentgrid_warehouse.sqlite"
REPORTS = ROOT / "reports"


TABLES = {
    "users": ["user_id", "account_type", "created_at"],
    "tools": ["tool_id", "tool_name", "tool_type", "enabled"],
    "runs": ["run_id", "user_id", "workflow_version", "workflow_name", "status", "latency_ms", "created_at"],
    "retrieval_events": ["event_id", "run_id", "query", "retrieval_hit", "retrieved_doc_count", "created_at"],
    "eval_scores": ["eval_id", "run_id", "groundedness_score", "hallucination_risk", "eval_decision", "created_at"],
    "tool_calls": ["call_id", "run_id", "tool_id", "tool_success", "latency_ms", "created_at"],
}


def load_data():
    return json.loads((ROOT / "sample_data.json").read_text())


def reset_db(conn):
    schema = (ROOT / "schema.sql").read_text()
    conn.executescript(schema)


def insert_rows(conn, table, rows):
    if not rows:
        return
    cols = TABLES[table]
    placeholders = ",".join("?" for _ in cols)
    query = f"INSERT INTO {table} ({','.join(cols)}) VALUES ({placeholders})"
    conn.executemany(query, [[row[col] for col in cols] for row in rows])


def run_query(conn, sql):
    cur = conn.execute(sql)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def write_csv(path, rows):
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_reports():
    REPORTS.mkdir(parents=True, exist_ok=True)

    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    reset_db(conn)

    data = load_data()
    for table, rows in data.items():
        insert_rows(conn, table, rows)

    conn.commit()

    query_files = {
        "workflow_usage": ROOT / "sql/workflow_usage.sql",
        "failure_rate": ROOT / "sql/failure_rate.sql",
        "latency_by_workflow_version": ROOT / "sql/latency_by_workflow_version.sql",
        "retrieval_quality": ROOT / "sql/retrieval_quality.sql",
        "eval_quality": ROOT / "sql/eval_quality.sql",
    }

    outputs = {}
    for name, path in query_files.items():
        statements = [s.strip() for s in path.read_text().split(";") if s.strip()]
        query_results = []
        for statement in statements:
            query_results.append(run_query(conn, statement))
        outputs[name] = query_results[-1]
        write_csv(REPORTS / f"{name}.csv", query_results[-1])

    summary = {
        "tables": list(TABLES.keys()),
        "runs": len(data["runs"]),
        "users": len(data["users"]),
        "tools": len(data["tools"]),
        "reports_generated": sorted(outputs.keys()),
        "failure_rate_by_version": outputs["failure_rate"],
        "latency_by_workflow_version": outputs["latency_by_workflow_version"],
        "retrieval_quality": outputs["retrieval_quality"],
        "eval_quality": outputs["eval_quality"],
    }

    (REPORTS / "warehouse_summary.json").write_text(json.dumps(summary, indent=2))
    (REPORTS / "warehouse_dashboard.html").write_text(build_html(summary))
    conn.close()
    return summary


def build_html(summary):
    def table(rows):
        if not rows:
            return "<p>No data</p>"
        headers = rows[0].keys()
        head = "".join(f"<th>{h}</th>" for h in headers)
        body = "".join(
            "<tr>" + "".join(f"<td>{row[h]}</td>" for h in headers) + "</tr>"
            for row in rows
        )
        return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"

    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>AgentGrid Analytics Warehouse</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; background: #0f172a; color: #e5e7eb; }}
    h1, h2 {{ color: #93c5fd; }}
    table {{ border-collapse: collapse; width: 100%; margin-bottom: 28px; background: #111827; }}
    th, td {{ border: 1px solid #374151; padding: 10px; text-align: left; }}
    th {{ background: #1f2937; }}
    .card {{ padding: 16px; border: 1px solid #334155; border-radius: 12px; margin-bottom: 20px; }}
  </style>
</head>
<body>
  <h1>AgentGrid Analytics Warehouse</h1>
  <div class="card">
    <p><b>Tables:</b> {", ".join(summary["tables"])}</p>
    <p><b>Runs:</b> {summary["runs"]}</p>
    <p><b>Users:</b> {summary["users"]}</p>
    <p><b>Tools:</b> {summary["tools"]}</p>
  </div>

  <h2>Failure Rate by Workflow Version</h2>
  {table(summary["failure_rate_by_version"])}

  <h2>Latency by Workflow Version</h2>
  {table(summary["latency_by_workflow_version"])}

  <h2>Retrieval Quality</h2>
  {table(summary["retrieval_quality"])}

  <h2>Eval Quality</h2>
  {table(summary["eval_quality"])}
</body>
</html>
"""


if __name__ == "__main__":
    print(json.dumps(build_reports(), indent=2))
