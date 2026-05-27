import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class StreamEvent:
    event_id: str
    event_type: str
    trace_id: str
    payload: dict
    offset: int
    attempts: int = 0
    status: str = "pending"
    error: Optional[str] = None


class InMemoryRedisStream:
    def __init__(self):
        self.events: List[StreamEvent] = []
        self.dlq: List[StreamEvent] = []
        self.committed_offset = 0

    def xadd(self, event_type: str, trace_id: str, payload: dict) -> StreamEvent:
        event = StreamEvent(
            event_id=f"{int(time.time() * 1000)}-{len(self.events)}",
            event_type=event_type,
            trace_id=trace_id,
            payload=payload,
            offset=len(self.events) + 1,
        )
        self.events.append(event)
        return event

    def read_from_offset(self, offset: int) -> List[StreamEvent]:
        return [event for event in self.events if event.offset > offset]

    def move_to_dlq(self, event: StreamEvent, error: str):
        event.status = "dead_lettered"
        event.error = error
        self.dlq.append(event)


def seed_stream() -> InMemoryRedisStream:
    stream = InMemoryRedisStream()
    trace_id = "trace_stream_runtime_001"

    stream.xadd("retrieval", trace_id, {"hit_count": 2, "retrieval_hit_rate": 0.84})
    stream.xadd("eval_gate", trace_id, {"decision": "hold", "reason": "missing_retrieval_grounding"})
    stream.xadd("escalation", trace_id, {"target": "support_reviewer_queue"})
    stream.xadd("latency_telemetry", trace_id, {"latency_ms": 258})
    stream.xadd("retrieval", trace_id, {"force_failure": True, "reason": "stale_embedding"})
    return stream


def process_stream(stream: InMemoryRedisStream, max_retries: int = 2) -> Dict:
    start = time.time()
    processed = []
    retry_count = 0
    failed_count = 0

    for event in stream.read_from_offset(stream.committed_offset):
        while event.attempts < max_retries:
            event.attempts += 1

            if event.payload.get("force_failure"):
                retry_count += 1
                event.status = "retrying"
                event.error = "forced stream processing failure"
                continue

            event.status = "processed"
            event.error = None
            processed.append(event)
            stream.committed_offset = max(stream.committed_offset, event.offset)
            break

        if event.status != "processed":
            failed_count += 1
            stream.move_to_dlq(event, event.error or "processing_failed")
            stream.committed_offset = max(stream.committed_offset, event.offset)

    latest_offset = max((event.offset for event in stream.events), default=0)
    consumer_lag = max(0, latest_offset - stream.committed_offset)
    avg_latency = round((time.time() - start) * 1000, 2)

    metrics = {
        "stream": "agentgrid_runtime_stream",
        "processed_event_count": len(processed),
        "failed_event_count": failed_count,
        "retry_count": retry_count,
        "dlq_depth": len(stream.dlq),
        "consumer_lag": consumer_lag,
        "processing_latency_ms": avg_latency,
        "backpressure_risk": len(stream.dlq) > 0 or consumer_lag > 0,
        "processed_event_types": [event.event_type for event in processed],
        "dlq_events": [asdict(event) for event in stream.dlq],
    }

    Path("streaming_runtime/stream_metrics.json").write_text(json.dumps(metrics, indent=2))
    return metrics


if __name__ == "__main__":
    runtime_stream = seed_stream()
    print(json.dumps(process_stream(runtime_stream), indent=2))
