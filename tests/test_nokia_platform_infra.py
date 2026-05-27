import json
from pathlib import Path

from streaming.kafka_event_producer import produce_demo_events
from streaming.kafka_agent_consumer import consume_events
from vector_indexing.chunk_documents import build_chunks
from vector_indexing.embedding_pipeline import build_embeddings
from vector_indexing.index_refresh_workflow import refresh_index


def test_streaming_pipeline_processes_agent_events():
    produce_demo_events()
    report = consume_events()

    assert report["processed_event_count"] == 5
    assert report["event_type_counts"]["eval_gate"] == 1
    assert "queue_lag_ms" in report


def test_vector_index_lifecycle_refreshes_stale_entries():
    chunks = build_chunks()
    embeddings = build_embeddings()
    report = refresh_index()

    assert len(chunks) >= 3
    assert len(embeddings) == len(chunks)
    assert report["refreshed_count"] >= 1


def test_agent_trace_graph_contains_core_agents():
    graph = json.loads(Path("orchestration_graph/agent_trace_graph.json").read_text())
    node_ids = {node["id"] for node in graph["nodes"]}

    assert "planner_agent" in node_ids
    assert "retriever_agent" in node_ids
    assert "evaluator_agent" in node_ids
    assert "escalation_agent" in node_ids
