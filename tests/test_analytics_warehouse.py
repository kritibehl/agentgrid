from pathlib import Path

from analytics_warehouse.build_warehouse_reports import build_reports
from analytics_warehouse.data_quality_checks import run_quality_checks


def test_analytics_warehouse_reports_generate():
    summary = build_reports()

    assert "runs" in summary["tables"]
    assert "users" in summary["tables"]
    assert "tools" in summary["tables"]
    assert "retrieval_events" in summary["tables"]
    assert "eval_scores" in summary["tables"]
    assert Path("analytics_warehouse/reports/warehouse_dashboard.html").exists()
    assert Path("analytics_warehouse/reports/failure_rate.csv").exists()


def test_data_quality_checks_pass():
    build_reports()
    result = run_quality_checks()

    assert result["status"] == "pass"
    assert result["null_violations"] == []
    assert result["schema_violations"] == []
    assert result["freshness_violations"] == []
