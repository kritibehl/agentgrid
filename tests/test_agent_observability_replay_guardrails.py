import json
from pathlib import Path

from agent_observability.cost_latency_tracker import build_observability_report
from agent_replay.replay_agent_run import replay_run
from agent_replay.human_review_resume import resume_after_review


def test_agent_observability_report_tracks_core_metrics():
    report = build_observability_report()

    assert report["trace_count"] == 4
    assert "retrieval_hit_rate" in report
    assert "tool_success_rate" in report
    assert "p95_latency_ms" in report
    assert "avg_cost_per_run_usd" in report
    assert Path("agent_observability/tool_success_dashboard.json").exists()


def test_agent_replay_and_resume():
    replay = replay_run()
    resumed = resume_after_review()

    assert replay["replay_status"] == "ready_for_resume"
    assert resumed["resumed_from_checkpoint"] is True
    assert resumed["final_status"] == "released"


def test_guardrail_taxonomy_files_exist_and_have_actions():
    for name in ["unsupported_claim", "missing_retrieval", "unsafe_action", "tool_timeout"]:
        data = json.loads(Path(f"guardrail_taxonomy/{name}.json").read_text())
        assert "failure_type" in data
        assert "default_action" in data
        assert "escalation_path" in data
