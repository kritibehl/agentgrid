from pathlib import Path
from streaming_runtime.stream_window_processor import process_window


def test_stream_window_processor_reports_lag_and_dlq_candidates():
    report = process_window()

    assert report["window_event_count"] == 6
    assert report["consumer_lag"] == 3
    assert report["failed_event_count"] == 1
    assert report["retry_count"] == 1
    assert report["backpressure_risk"] is True
    assert report["replay_from_offset"] == 15
    assert Path("streaming_runtime/consumer_lag_report.json").exists()
