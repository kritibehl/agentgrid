import json
from pathlib import Path


LOWER_IS_BETTER = {"p95_latency_ms", "cost_per_run_usd"}


def percent_change(old, new):
    if old == 0:
        return 0
    return round(((new - old) / old) * 100, 2)


def compare_versions(path="agent_version_benchmarking/version_metrics.json"):
    data = json.loads(Path(path).read_text())
    v1 = data["agent_v1"]
    v2 = data["agent_v2"]

    comparisons = {}

    for metric, old_value in v1.items():
        new_value = v2[metric]
        delta = round(new_value - old_value, 4)
        pct_change = percent_change(old_value, new_value)

        if metric in LOWER_IS_BETTER:
            improved = new_value < old_value
        else:
            improved = new_value > old_value

        comparisons[metric] = {
            "agent_v1": old_value,
            "agent_v2": new_value,
            "delta": delta,
            "percent_change": pct_change,
            "improved": improved
        }

    regressions = [
        metric for metric, result in comparisons.items()
        if not result["improved"]
    ]

    report = {
        "benchmark": "agent_version_comparison",
        "versions": ["agent_v1", "agent_v2"],
        "comparisons": comparisons,
        "regressions": regressions,
        "winner": "agent_v2" if not regressions else "review_required",
        "release_decision": "ship_agent_v2" if not regressions else "hold",
        "summary": {
            "retrieval_hit_rate_gain": comparisons["retrieval_hit_rate"]["delta"],
            "tool_success_rate_gain": comparisons["tool_success_rate"]["delta"],
            "p95_latency_ms_delta": comparisons["p95_latency_ms"]["delta"],
            "cost_per_run_delta": comparisons["cost_per_run_usd"]["delta"],
            "eval_pass_rate_gain": comparisons["eval_pass_rate"]["delta"]
        }
    }

    Path("agent_version_benchmarking/version_benchmark_report.json").write_text(
        json.dumps(report, indent=2)
    )
    Path("agent_version_benchmarking/version_benchmark_report.md").write_text(
        build_markdown(report)
    )
    return report


def build_markdown(report):
    rows = "\n".join(
        f"| {metric} | {result['agent_v1']} | {result['agent_v2']} | "
        f"{result['delta']} | {result['percent_change']}% | {result['improved']} |"
        for metric, result in report["comparisons"].items()
    )

    return f"""# Agent Version Benchmark Report

## Summary

| Field | Value |
|---|---|
| Winner | {report['winner']} |
| Release decision | {report['release_decision']} |
| Regressions | {', '.join(report['regressions']) if report['regressions'] else 'none'} |

## Metric Comparison

| Metric | agent_v1 | agent_v2 | Delta | Percent Change | Improved |
|---|---:|---:|---:|---:|---|
{rows}

## What This Proves

This benchmark compares RAG/agent workflow versions across retrieval quality, tool success, p95 latency, cost per run, and eval-gate pass rate.

## Scope

This is a deterministic benchmark artifact. It does not claim production traffic or live A/B testing.
"""


if __name__ == "__main__":
    print(json.dumps(compare_versions(), indent=2))
