from pathlib import Path

from mcp_rag_analytics.rag_analytics_agent import run_rag_query
from agentic_retail_workflows.rag_product_answer_agent import generate_product_answer


def test_mcp_rag_analytics_outputs_quality_and_eval_reports():
    result = run_rag_query()

    assert result["retrieval_quality"]["retrieval_hit_rate"] == 0.84
    assert result["eval_gate"]["decision"] == "hold"
    assert Path("mcp_rag_analytics/retrieval_quality_metrics.json").exists()
    assert Path("mcp_rag_analytics/eval_gate_report.json").exists()


def test_agentic_retail_workflow_generates_eval_gated_answer():
    result = generate_product_answer()

    assert result["retrieval_quality"]["retrieval_hit_rate"] >= 0.8
    assert result["eval_gate"]["decision"] in ("ship", "hold")
    assert Path("agentic_retail_workflows/retrieval_quality_report.json").exists()
    assert Path("agentic_retail_workflows/eval_gate_report.json").exists()
