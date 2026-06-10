from pathlib import Path

from agent_version_benchmark.benchmark_agents import compare_agents


def test_agent_version_benchmark_promotes_v2():
    report = compare_agents()

    assert report["candidate"]["agent_version"] == "agent_v2"
    assert report["candidate"]["eval_gate"] == "PASS"
    assert report["release_decision"] == "PROMOTE_AGENT_V2"


def test_agent_v2_improves_quality_latency_and_cost():
    report = compare_agents()
    improvements = report["improvements"]

    assert improvements["retrieval_hit_rate_delta"] == 0.12
    assert improvements["tool_success_rate_delta"] == 0.15
    assert improvements["p95_latency_ms_delta"] == -180
    assert improvements["cost_per_run_usd_delta"] == -0.0042
    assert improvements["eval_pass_rate_delta"] == 0.16


def test_agent_version_benchmark_report_written():
    compare_agents()

    assert Path("agent_version_benchmark/agent_version_benchmark_report.json").exists()
