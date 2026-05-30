from pathlib import Path
from retail_personalization.personalized_messaging_agent import generate_personalized_experiences


def test_retail_personalization_generates_segmented_messages():
    report = generate_personalized_experiences()

    assert report["segments_evaluated"] == 3
    assert report["recommendations_evaluated"] == 3
    assert report["ship_decisions"] == 3
    assert report["avg_message_relevance"] >= 0.89
    assert Path("retail_personalization/personalization_report.json").exists()
