from mcp_rag_workflows.rag_analytics_agent import run_analytics

def test_retrieval_quality_metrics():
    report = run_analytics()

    assert report["retrieval_hit_rate"] > 0.5
    assert report["avg_retrieval_latency_ms"] > 0
    assert report["status"] == "healthy"
