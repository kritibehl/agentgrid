from pathlib import Path

from product_analytics.build_product_analytics import build_product_analytics


def test_product_analytics_reports_generate():
    summary = build_product_analytics()

    assert "DAU" in summary["metrics_tracked"]
    assert "WAU" in summary["metrics_tracked"]
    assert summary["funnel_conversion"]["activation_rate"] >= 0.8
    assert Path("product_analytics/reports/product_analytics_dashboard.md").exists()
    assert Path("product_analytics/reports/product_analytics_summary.json").exists()
    assert Path("product_analytics/reports/experiment_lift.csv").exists()
