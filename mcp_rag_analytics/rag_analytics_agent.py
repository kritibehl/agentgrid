import json
from pathlib import Path


def run_rag_query(query: str = "Why did retrieval quality drop?") -> dict:
    retrieved_chunks = [
        "Retrieval hit rate dropped after stale runbook embeddings were detected.",
        "Cache invalidation and embedding refresh improved grounding quality."
    ]

    result = {
        "query": query,
        "retrieved_chunks": retrieved_chunks,
        "retrieval_quality": {
            "retrieval_hit_rate": 0.84,
            "retrieval_latency_ms": 14.8,
            "stale_embedding_detected": True,
            "cache_refresh_required": True
        },
        "multi_agent_workflow": [
            "planner_agent",
            "retriever_agent",
            "analytics_agent",
            "eval_gate",
            "escalation_router"
        ],
        "analytics_summary": "Retrieval quality degradation was linked to stale embeddings and improved after cache invalidation and refresh.",
        "eval_gate": {
            "decision": "hold",
            "reason": "stale_embedding_detected",
            "human_review_required": True
        }
    }

    Path("mcp_rag_analytics/retrieval_quality_metrics.json").write_text(
        json.dumps(result["retrieval_quality"], indent=2)
    )
    Path("mcp_rag_analytics/eval_gate_report.json").write_text(
        json.dumps(result["eval_gate"], indent=2)
    )
    return result


if __name__ == "__main__":
    print(json.dumps(run_rag_query(), indent=2))
