from customer_analytics.analyze_feedback import classify_feedback, analyze_feedback


def test_classifies_retry_feedback():
    labels = classify_feedback("missed retry amplification context")

    assert "retry_amplification" in labels


def test_feedback_report_detects_repeat_issues():
    report = analyze_feedback()

    assert report["total_feedback_events"] == 4
    assert "retry_amplification" in report["repeat_issue_flags"]
