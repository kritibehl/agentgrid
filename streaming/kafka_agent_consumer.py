import json
import time
from pathlib import Path
from collections import Counter


EVENT_LOG = Path("streaming/agent_event_log.jsonl")
REPORT = Path("streaming/stream_processing_report.json")


def consume_events(path: Path = EVENT_LOG) -> dict:
    start = time.time()
    failed_event_count = 0
    retry_count = 0
    processed = []

    if not path.exists():
        return {
            "processed_event_count": 0,
            "failed_event_count": 0,
            "retry_count": 0,
            "queue_lag_ms": 0,
            "processing_latency_ms": 0,
            "event_type_counts": {},
            "status": "no_events"
        }

    lines = [line for line in path.read_text().splitlines() if line.strip()]
    now_ms = int(time.time() * 1000)

    for line in lines:
        try:
            event = json.loads(line)
            if event["payload"].get("force_failure"):
                retry_count += 1
                raise ValueError("forced event processing failure")
            processed.append(event)
        except Exception:
            failed_event_count += 1

    event_counts = Counter(event["event_type"] for event in processed)
    oldest_ts = min((event["timestamp_ms"] for event in processed), default=now_ms)

    report = {
        "processed_event_count": len(processed),
        "failed_event_count": failed_event_count,
        "retry_count": retry_count,
        "queue_lag_ms": max(0, now_ms - oldest_ts),
        "processing_latency_ms": round((time.time() - start) * 1000, 2),
        "event_type_counts": dict(event_counts),
        "status": "processed"
    }

    REPORT.write_text(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    print(json.dumps(consume_events(), indent=2))
