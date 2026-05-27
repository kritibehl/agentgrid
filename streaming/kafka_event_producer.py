import json
import time
from pathlib import Path
from uuid import uuid4


EVENT_LOG = Path("streaming/agent_event_log.jsonl")


def make_event(event_type: str, trace_id: str, payload: dict) -> dict:
    return {
        "event_id": f"evt_{uuid4().hex[:12]}",
        "event_type": event_type,
        "trace_id": trace_id,
        "timestamp_ms": int(time.time() * 1000),
        "payload": payload,
    }


def produce_demo_events() -> list[dict]:
    trace_id = "trace_stream_001"
    events = [
        make_event("user_query", trace_id, {"query": "Why did deployment fail?"}),
        make_event("retrieval", trace_id, {"hit_count": 1, "retrieval_hit_rate": 0.32}),
        make_event("eval_gate", trace_id, {"decision": "hold", "reason": "missing_retrieval_grounding"}),
        make_event("escalation", trace_id, {"target": "support_reviewer_queue", "severity": "high"}),
        make_event("latency_telemetry", trace_id, {"latency_ms": 258, "tokens_per_second": 950}),
    ]

    EVENT_LOG.write_text("\n".join(json.dumps(event) for event in events) + "\n")
    return events


if __name__ == "__main__":
    print(json.dumps(produce_demo_events(), indent=2))
