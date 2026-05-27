import json
from pathlib import Path
from collections import Counter


SAMPLE_EVENTS = [
    {"event_id": "evt_001", "type": "user_query", "latency_ms": 40, "status": "ok", "partition": 0, "offset": 10},
    {"event_id": "evt_002", "type": "retrieval", "latency_ms": 120, "status": "ok", "partition": 0, "offset": 11},
    {"event_id": "evt_003", "type": "eval_gate", "latency_ms": 35, "status": "hold", "partition": 0, "offset": 12},
    {"event_id": "evt_004", "type": "escalation", "latency_ms": 80, "status": "retry", "partition": 0, "offset": 13},
    {"event_id": "evt_005", "type": "latency_telemetry", "latency_ms": 258, "status": "ok", "partition": 0, "offset": 14},
    {"event_id": "evt_006", "type": "retrieval", "latency_ms": 310, "status": "failed", "partition": 0, "offset": 15}
]


def process_window(events=None, committed_offset=12):
    events = events or SAMPLE_EVENTS
    counts = Counter(event["type"] for event in events)
    failed = [event for event in events if event["status"] == "failed"]
    retries = [event for event in events if event["status"] == "retry"]
    latest_offset = max(event["offset"] for event in events)
    avg_latency = sum(event["latency_ms"] for event in events) / len(events)

    report = {
        "window_event_count": len(events),
        "event_type_counts": dict(counts),
        "consumer_lag": latest_offset - committed_offset,
        "avg_processing_latency_ms": round(avg_latency, 2),
        "failed_event_count": len(failed),
        "retry_count": len(retries),
        "backpressure_risk": avg_latency > 200 or len(failed) > 0,
        "dead_letter_candidates": failed,
        "replay_from_offset": min(event["offset"] for event in failed) if failed else None
    }

    Path("streaming_runtime/consumer_lag_report.json").write_text(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    print(json.dumps(process_window(), indent=2))
