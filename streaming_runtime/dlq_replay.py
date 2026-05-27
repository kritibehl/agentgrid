import json
from pathlib import Path
from dataclasses import asdict

from streaming_runtime.redis_stream_processor import InMemoryRedisStream, seed_stream, process_stream


def replay_dlq(stream: InMemoryRedisStream) -> dict:
    replayed = []

    for event in list(stream.dlq):
        repaired = event
        repaired.payload.pop("force_failure", None)
        repaired.payload["replayed_from_dlq"] = True
        repaired.status = "pending"
        repaired.error = None
        repaired.attempts = 0

        stream.dlq.remove(event)
        stream.events.append(repaired)

    before_second_pass = len(stream.events)
    second_pass_metrics = process_stream(stream)

    replayed = [
        asdict(event)
        for event in stream.events[:before_second_pass]
        if event.payload.get("replayed_from_dlq")
    ]

    report = {
        "replayed_event_count": len(replayed),
        "remaining_dlq_depth": len(stream.dlq),
        "second_pass_processed": second_pass_metrics["processed_event_count"],
        "second_pass_failed": second_pass_metrics["failed_event_count"],
        "status": "replayed" if len(stream.dlq) == 0 else "partial_replay",
        "replayed_events": replayed,
    }

    Path("streaming_runtime/dlq_replay_report.json").write_text(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    stream = seed_stream()
    process_stream(stream)
    print(json.dumps(replay_dlq(stream), indent=2))
