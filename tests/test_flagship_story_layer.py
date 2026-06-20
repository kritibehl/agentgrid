from pathlib import Path
import json


def test_flagship_docs_and_reports_exist():
    paths = [
        "docs/architecture.md",
        "docs/agent_failure_modes.md",
        "docs/product_requirements_ai_workflows.md",
        "docs/evaluation_methodology.md",
        "reports/sample_agent_run_trace.json",
        "reports/eval_gate_report.md",
        "reports/human_review_decisions.md",
        "examples/ai_authoring_workflow.json",
        "examples/groundedness_eval.json",
        "examples/authoring_report.md",
        "frontend/screenshots/agent_dashboard.png",
    ]

    for path in paths:
        assert Path(path).exists(), path


def test_sample_trace_has_required_stages():
    trace = json.loads(Path("reports/sample_agent_run_trace.json").read_text())
    stages = [step["stage"] for step in trace["steps"]]

    assert "classify" in stages
    assert "retrieve" in stages
    assert "tool_call" in stages
    assert "eval_gate" in stages
    assert "human_review" in stages
    assert trace["steps"][4]["decision"] == "hold"


def test_ai_authoring_workflow_groundedness_gate():
    workflow = json.loads(Path("examples/ai_authoring_workflow.json").read_text())

    assert workflow["workflow"] == "ai_authoring_workflow"
    assert workflow["eval_gate"]["groundedness"] == "pass"
    assert workflow["eval_gate"]["decision"] == "ship"
