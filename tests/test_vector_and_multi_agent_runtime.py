import json
from pathlib import Path


def test_agent_execution_graph_contains_core_agents():
    graph = json.loads(
        Path("multi_agent_runtime/agent_execution_graph.json").read_text()
    )

    agent_names = {agent["name"] for agent in graph["agents"]}

    assert "planner_agent" in agent_names
    assert "retriever_agent" in agent_names
    assert "evaluator_agent" in agent_names
    assert "escalation_agent" in agent_names


def test_retrieval_quality_benchmark_exists():
    text = Path(
        "vector_retrieval_lifecycle/retrieval_quality_benchmark.md"
    ).read_text()

    assert "retrieval_hit_rate" in text
    assert "unsupported_answer_reduction" in text


def test_embedding_refresh_strategy_mentions_cache_invalidation():
    text = Path(
        "vector_retrieval_lifecycle/embedding_refresh_strategy.md"
    ).read_text()

    assert "cache invalidation" in text
    assert "retrieval drift" in text
