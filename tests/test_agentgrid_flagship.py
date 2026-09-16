from pathlib import Path
from claude_workflows.claude_tool_runner import run_all
from evals.ragas.ragas_eval import run_ragas_eval
from runtime_telemetry.collect_runtime_metrics import collect_metrics
from handoff.review_queue import build_review_queue

def test_claude_style_workflow_runs():
    report = run_all()
    assert report["runs"] == 2
    assert Path("claude_workflows/claude_run_report.json").exists()

def test_ragas_eval_runs():
    report = run_ragas_eval()
    assert report["decision"] == "pass"
    assert report["faithfulness"] >= 0.9

def test_runtime_telemetry_runs():
    report = collect_metrics()
    assert "avg_cost" in report
    assert report["p95_latency_ms"] > 0

def test_handoff_queue_runs():
    report = build_review_queue()
    assert report["queue_size"] == 1
    assert report["decision"] == "route_to_human_review"
