from pathlib import Path

from agent_version_benchmarking.compare_agent_versions import compare_versions


def test_agent_version_benchmark_prefers_v2():
    report = compare_versions()

    assert report["winner"] == "agent_v2"
    assert report["release_decision"] == "ship_agent_v2"
    assert report["comparisons"]["retrieval_hit_rate"]["improved"] is True
    assert report["comparisons"]["tool_success_rate"]["improved"] is True
    assert report["comparisons"]["p95_latency_ms"]["improved"] is True
    assert report["comparisons"]["cost_per_run_usd"]["improved"] is True
    assert report["comparisons"]["eval_pass_rate"]["improved"] is True
    assert Path("agent_version_benchmarking/version_benchmark_report.json").exists()
    assert Path("agent_version_benchmarking/version_benchmark_report.md").exists()
