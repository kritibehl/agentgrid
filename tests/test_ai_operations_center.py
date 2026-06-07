from pathlib import Path

from ai_operations_center.agent_reliability_scorecard import build_scorecard
from ai_operations_center.cost_governance_center import build_cost_governance_center
from ai_operations_center.human_review_analytics import build_human_review_analytics
from ai_operations_center.build_ai_ops_report import build_ai_ops_report


def test_agent_reliability_scorecard():
    scorecard = build_scorecard()

    assert scorecard["retrieval"] == 0.82
    assert scorecard["tool_success"] == 0.91
    assert scorecard["hallucination_risk"] == 0.07
    assert Path("ai_operations_center/agent_reliability_scorecard.json").exists()


def test_cost_governance_center():
    report = build_cost_governance_center()

    assert report["monthly_cost"] == 700.0
    assert report["status"] == "budget_risk"
    assert report["waste"]["total_estimated_waste_usd"] == 164.0


def test_human_review_analytics():
    report = build_human_review_analytics()

    assert report["approval_rate"] == 0.68
    assert report["override_rate"] == 0.24
    assert report["rejection_rate"] == 0.08


def test_combined_ai_ops_report():
    report = build_ai_ops_report()

    assert report["platform_status"] == "watch"
    assert report["release_recommendation"] == "hold_noncritical_ai_changes"
    assert Path("ai_operations_center/ai_operations_report.json").exists()
