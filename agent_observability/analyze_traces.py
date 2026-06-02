import json
from collections import Counter, defaultdict
from pathlib import Path


def percentile(values, p):
    values = sorted(values)
    if not values:
        return 0
    idx = min(len(values) - 1, int(round((p / 100) * (len(values) - 1))))
    return values[idx]


def load_traces(path="agent_observability/sample_traces.jsonl"):
    return [
        json.loads(line)
        for line in Path(path).read_text().splitlines()
        if line.strip()
    ]


def analyze_traces():
    traces = load_traces()
    total = len(traces)

    decisions = Counter(trace["decision"] for trace in traces)
    failures = Counter(
        trace["failure_reason"]
        for trace in traces
        if trace.get("failure_reason")
    )
    model_counts = Counter(trace["model_version"] for trace in traces)

    latency_values = [trace["latency_ms"] for trace in traces]
    costs = [trace["cost_usd"] for trace in traces]

    summary = {
        "total_requests": total,
        "retrieval_hit_rate": round(sum(trace["retrieval_hit"] for trace in traces) / total, 2),
        "tool_success_rate": round(sum(trace["tool_success"] for trace in traces) / total, 2),
        "avg_latency_ms": round(sum(latency_values) / total, 2),
        "p95_latency_ms": percentile(latency_values, 95),
        "avg_cost_usd": round(sum(costs) / total, 4),
        "escalation_rate": round(decisions["escalate"] / total, 2),
        "hold_rate": round(decisions["hold"] / total, 2),
        "release_decision": "hold" if decisions["hold"] or decisions["escalate"] else "ship",
        "decision_counts": dict(decisions),
        "failure_breakdown": dict(failures),
        "model_version_counts": dict(model_counts),
    }

    by_model = defaultdict(list)
    for trace in traces:
        by_model[trace["model_version"]].append(trace)

    model_report = {}
    for model, rows in by_model.items():
        model_report[model] = {
            "request_count": len(rows),
            "retrieval_hit_rate": round(sum(row["retrieval_hit"] for row in rows) / len(rows), 2),
            "tool_success_rate": round(sum(row["tool_success"] for row in rows) / len(rows), 2),
            "avg_eval_score": round(sum(row["eval_score"] for row in rows) / len(rows), 2),
            "avg_latency_ms": round(sum(row["latency_ms"] for row in rows) / len(rows), 2),
            "avg_cost_usd": round(sum(row["cost_usd"] for row in rows) / len(rows), 4),
        }

    Path("agent_observability/trace_failure_breakdown.json").write_text(
        json.dumps(summary["failure_breakdown"], indent=2)
    )
    Path("agent_observability/model_version_comparison.json").write_text(
        json.dumps(model_report, indent=2)
    )
    Path("agent_observability/escalation_trend_report.json").write_text(
        json.dumps(summary, indent=2)
    )

    return summary


if __name__ == "__main__":
    print(json.dumps(analyze_traces(), indent=2))
