from pathlib import Path

from streaming_runtime.stream_window_processor import process_window
from streaming_runtime.redis_stream_processor import seed_stream, process_stream
from streaming_runtime.dlq_replay import replay_dlq


def test_stream_window_processor_reports_lag_and_dlq_candidates():
    report = process_window()

    assert report["window_event_count"] == 6
    assert report["consumer_lag"] == 3
    assert report["failed_event_count"] == 1
    assert report["retry_count"] == 1
    assert report["backpressure_risk"] is True
    assert report["replay_from_offset"] == 15
    assert Path("streaming_runtime/consumer_lag_report.json").exists()


def test_redis_stream_processor_moves_failed_event_to_dlq():
    stream = seed_stream()
    metrics = process_stream(stream)

    assert metrics["processed_event_count"] == 4
    assert metrics["failed_event_count"] == 1
    assert metrics["retry_count"] >= 2
    assert metrics["dlq_depth"] == 1
    assert metrics["backpressure_risk"] is True
    assert Path("streaming_runtime/stream_metrics.json").exists()


def test_dlq_replay_recovers_failed_event():
    stream = seed_stream()
    process_stream(stream)
    report = replay_dlq(stream)

    assert report["replayed_event_count"] >= 1
    assert report["remaining_dlq_depth"] == 0
    assert report["status"] == "replayed"
    assert Path("streaming_runtime/dlq_replay_report.json").exists()
