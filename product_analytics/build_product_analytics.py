import csv
import json
import sqlite3
from pathlib import Path


ROOT = Path("product_analytics")
REPORTS = ROOT / "reports"
DB = ROOT / "product_analytics.sqlite"


QUERY_FILES = {
    "dau_wau": ROOT / "sql/dau_wau.sql",
    "funnel_conversion": ROOT / "sql/funnel_conversion.sql",
    "cohort_retention": ROOT / "sql/cohort_retention.sql",
    "agent_adoption_by_segment": ROOT / "sql/agent_adoption_by_segment.sql",
    "experiment_lift": ROOT / "sql/experiment_lift.sql",
}


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


def build_product_analytics():
    REPORTS.mkdir(parents=True, exist_ok=True)

    if DB.exists():
        DB.unlink()

    conn = sqlite3.connect(DB)
    conn.executescript((ROOT / "schema.sql").read_text())
    conn.executescript((ROOT / "sample_events.sql").read_text())
    conn.commit()

    outputs = {}

    for name, path in QUERY_FILES.items():
        statements = [s.strip() for s in path.read_text().split(";") if s.strip()]
        result = None
        for statement in statements:
            result = run_query(conn, statement)
        outputs[name] = result
        write_csv(REPORTS / f"{name}.csv", result)

    summary = {
        "dau_wau": outputs["dau_wau"],
        "funnel_conversion": outputs["funnel_conversion"][0],
        "cohort_retention": outputs["cohort_retention"],
        "agent_adoption_by_segment": outputs["agent_adoption_by_segment"],
        "experiment_lift": outputs["experiment_lift"],
        "metrics_tracked": [
            "DAU",
            "WAU",
            "activation funnel",
            "workflow completion rate",
            "tool success rate",
            "retention by user segment",
            "experiment lift",
            "quality improvement after workflow change"
        ]
    }

    (REPORTS / "product_analytics_summary.json").write_text(json.dumps(summary, indent=2))
    (REPORTS / "product_analytics_dashboard.md").write_text(build_markdown(summary))
    conn.close()
    return summary


def build_markdown(summary):
    funnel = summary["funnel_conversion"]

    return f"""# Product Analytics Dashboard

## Metrics Covered

- DAU / WAU-style usage
- activation funnel
- agent workflow completion rate
- tool success rate
- retention by cohort
- agent adoption by segment
- experiment A/B lift
- quality improvement after workflow change

## Funnel Summary

| Metric | Value |
|---|---:|
| signed_up | {funnel['signed_up']} |
| activated | {funnel['activated']} |
| completed | {funnel['completed']} |
| activation_rate | {funnel['activation_rate']} |
| completion_rate | {funnel['completion_rate']} |

## Segment Adoption

See `agent_adoption_by_segment.csv`.

## Experiment Lift

See `experiment_lift.csv`.

## Scope

This is a deterministic product-analytics proof for AgentGrid AI-agent workflow telemetry.
"""


if __name__ == "__main__":
    print(json.dumps(build_product_analytics(), indent=2))
