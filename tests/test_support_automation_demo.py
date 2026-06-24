import json
from pathlib import Path


def test_support_automation_artifacts_exist():
    paths = [
        "examples/support_automation_workflow.json",
        "examples/customer_issue_triage.json",
        "examples/knowledge_retrieval_trace.json",
        "reports/support_automation_eval_report.md",
        "reports/feedback_loop_quality_report.md",
        "docs/cooperative_ai_use_case.md",
        "docs/support_automation_architecture.md",
    ]

    for path in paths:
        assert Path(path).exists(), path


def test_support_automation_routes_unsupported_answer_to_review():
    workflow = json.loads(Path("examples/support_automation_workflow.json").read_text())

    assert workflow["workflow"] == "support_automation"
    assert workflow["steps"][1]["retrieval_hit"] is True
    assert workflow["steps"][3]["decision"] == "escalate_to_human_review"
    assert workflow["release_decision"] == "hold_for_review"


def test_customer_issue_triage_detects_missing_evidence():
    triage = json.loads(Path("examples/customer_issue_triage.json").read_text())

    assert triage["classification"]["requires_human_review"] is True
    assert triage["structured_fields"]["missing_evidence"] is True
    assert triage["structured_fields"]["unsafe_action_risk"] is True
