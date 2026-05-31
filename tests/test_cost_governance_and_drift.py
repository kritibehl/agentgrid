from pathlib import Path

from cost_governance.spend_tracker import calculate_spend
from cost_governance.release_budget_gate import run_budget_gate
from evaluation_drift.drift_detector import detect_drift


def test_cost_governance_flags_budget_risk():
    report = calculate_spend()

    assert report["monthly_budget"] == 500
    assert report["projected_spend"] > 500
    assert report["status"] == "budget_risk"
    assert Path("cost_governance/projected_cost_report.json").exists()


def test_budget_gate_holds_on_budget_risk():
    result = run_budget_gate()

    assert result["decision"] == "hold"
    assert result["status"] == "budget_risk"


def test_evaluation_drift_detects_retrieval_regression():
    report = detect_drift()

    assert report["metrics"]["retrieval_hit_rate"]["baseline"] == 0.91
    assert report["metrics"]["retrieval_hit_rate"]["current"] == 0.76
    assert "retrieval_hit_rate" in report["regressions"]
    assert report["decision"] == "hold"
    assert Path("evaluation_drift/drift_report.json").exists()
