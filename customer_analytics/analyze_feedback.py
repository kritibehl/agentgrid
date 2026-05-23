import json
from collections import Counter
from pathlib import Path


TAXONOMY = {
    "missing_runbook_context": ["missed", "runbook", "missing evidence"],
    "retry_amplification": ["retry amplification", "retry"],
    "latency_threshold": ["latency", "p95"],
    "correct_hold": ["correctly held", "held the answer"],
}


def classify_feedback(text: str):
    lower = text.lower()
    labels = []
    for label, terms in TAXONOMY.items():
        if any(term in lower for term in terms):
            labels.append(label)
    return labels or ["general_feedback"]


def analyze_feedback(path="customer_analytics/feedback_events.json"):
    events = json.loads(Path(path).read_text())
    enriched = []

    for event in events:
        labels = classify_feedback(event["feedback"])
        enriched.append({**event, "issue_labels": labels})

    counts = Counter(label for event in enriched for label in event["issue_labels"])

    report = {
        "total_feedback_events": len(events),
        "issue_taxonomy_counts": dict(counts),
        "top_issue_families": counts.most_common(),
        "repeat_issue_flags": [
            label for label, count in counts.items() if count > 1
        ],
        "enriched_feedback": enriched
    }

    Path("customer_analytics/feedback_cluster_report.json").write_text(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    print(json.dumps(analyze_feedback(), indent=2))
