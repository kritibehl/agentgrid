from __future__ import annotations

import json
from pathlib import Path


AGENT_RESULTS = [
    {
        "agent_version": "agent_v1",
        "retrieval_hit_rate": 0.72,
        "tool_success_rate": 0.74,
        "p95_latency_ms": 1120,
        "cost_per_run_usd": 0.021,
        "eval_pass_rate": 0.70,
        "eval_gate": "HOLD"
    },
    {
        "agent_version": "agent_v2",
        "retrieval_hit_rate": 0.84,
        "tool_success_rate": 0.89,
        "p95_latency_ms": 940,
        "cost_per_run_usd": 0.0168,
        "eval_pass_rate": 0.86,
        "eval_gate": "PASS"
    }
]


def compare_agents() -> dict[str, object]:
    baseline, candidate = AGENT_RESULTS

    report = {
        "benchmark": "agent_version_benchmark",
        "baseline": baseline,
        "candidate": candidate,
        "improvements": {
            "retrieval_hit_rate_delta": round(candidate["retrieval_hit_rate"] - baseline["retrieval_hit_rate"], 3),
            "tool_success_rate_delta": round(candidate["tool_success_rate"] - baseline["tool_success_rate"], 3),
            "p95_latency_ms_delta": candidate["p95_latency_ms"] - baseline["p95_latency_ms"],
            "cost_per_run_usd_delta": round(candidate["cost_per_run_usd"] - baseline["cost_per_run_usd"], 4),
            "eval_pass_rate_delta": round(candidate["eval_pass_rate"] - baseline["eval_pass_rate"], 3)
        },
        "release_decision": "PROMOTE_AGENT_V2"
    }

    out = Path("agent_version_benchmark")
    out.mkdir(parents=True, exist_ok=True)
    (out / "agent_version_benchmark_report.json").write_text(json.dumps(report, indent=2))

    return report


if __name__ == "__main__":
    print(json.dumps(compare_agents(), indent=2))
