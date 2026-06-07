import json
from pathlib import Path


def build_human_review_analytics():
    report = {
        "reviewed_outputs": 25,
        "approved_outputs": 17,
        "overridden_outputs": 6,
        "rejected_outputs": 2,
        "approval_rate": 0.68,
        "override_rate": 0.24,
        "rejection_rate": 0.08,
        "top_override_reasons": [
            "unsupported root-cause certainty",
            "missing retrieval evidence",
            "unsafe operational action"
        ],
        "status": "healthy_review_loop"
    }

    Path("ai_operations_center/human_review_analytics.json").write_text(
        json.dumps(report, indent=2)
    )
    return report


if __name__ == "__main__":
    print(json.dumps(build_human_review_analytics(), indent=2))
