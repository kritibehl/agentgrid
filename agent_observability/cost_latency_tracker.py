import json
from pathlib import Path


RUNS = [
    {"trace_id": "ag-1021", "latency_ms": 760, "cost_usd": 0.016, "tool_success": True, "retrieval_hit": True, "eval_gate": "pass"},
    {"trace_id": "ag-1022", "latency_ms": 820, "cost_usd": 0.018, "tool_success": True, "retrieval_hit": True, "eval_gate": "pass"},
    {"trace_id": "ag-1023", "latency_ms": 940, "cost_usd": 0.021, "tool_success": False, "retrieval_hit": True, "eval_gate": "hold"},
    {"trace_id": "ag-1024", "latency_ms": 610, "cost_usd": 0.012, "tool_success": True, "retrieval_hit": False, "eval_gate": "hold"}
]


def percentile(values, p):
    ordered = sorted(values)
    idx = min(len(ordered) - 1, int(round((p / 100) * (len(ordered) - 1))))
    return ordered[idx]


def build_observability_report():
    latencies = [run["latency_ms"] for run in RUNS]
    report = {
        "trace_count": len(RUNS),
        "retrieval_hit_rate": round(sum(run["retrieval_hit"] for run in RUNS) / len(RUNS), 2),
        "tool_success_rate": round(sum(run["tool_success"] for run in RUNS) / len(RUNS), 2),
        "p95_latency_ms": percentile(latencies, 95),
        "avg_cost_per_run_usd": round(sum(run["cost_usd"] for run in RUNS) / len(RUNS), 4),
        "eval_gate_outcomes": {
            "pass": sum(1 for run in RUNS if run["eval_gate"] == "pass"),
            "hold": sum(1 for run in RUNS if run["eval_gate"] == "hold"),
            "escalate": sum(1 for run in RUNS if run["eval_gate"] == "escalate")
        },
        "trace_level_failure_reasons": [
            {"trace_id": run["trace_id"], "reason": "tool_failure" if not run["tool_success"] else "missing_retrieval" if not run["retrieval_hit"] else None}
            for run in RUNS
            if not run["tool_success"] or not run["retrieval_hit"]
        ]
    }

    Path("agent_observability/tool_success_dashboard.json").write_text(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    print(json.dumps(build_observability_report(), indent=2))
