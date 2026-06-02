from pathlib import Path

from agent_observability.analyze_traces import analyze_traces
from distributed_eval_processing.pyspark_trace_aggregator import pyspark_aggregate


def test_trace_analytics_outputs_release_risk_metrics():
    report = analyze_traces()

    assert report["total_requests"] == 5
    assert report["retrieval_hit_rate"] == 0.8
    assert report["tool_success_rate"] == 0.8
    assert report["release_decision"] == "hold"
    assert Path("agent_observability/escalation_trend_report.json").exists()


def test_distributed_eval_processing_outputs_model_metrics():
    report = pyspark_aggregate()

    assert report["total_events"] == 5
    assert report["retrieval_hit_rate"] == 0.8
    assert report["tool_success_rate"] == 0.8
    assert "gpt4o-mini-v2" in report["model_metrics"]
    assert Path("distributed_eval_processing/spark_metrics_output.json").exists()
