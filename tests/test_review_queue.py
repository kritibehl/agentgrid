from review_queue.review_lifecycle import run_review_lifecycle


def test_review_lifecycle_releases_approved_output():
    report = run_review_lifecycle()

    assert report["final_status"] == "released"
    assert report["governance_path"] == ["blocked", "reviewed", "approved", "released"]
    assert report["history_count"] == 3
