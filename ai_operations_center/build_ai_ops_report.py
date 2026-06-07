import json
from pathlib import Path

from ai_operations_center.agent_reliability_scorecard import build_scorecard
from ai_operations_center.cost_governance_center import build_cost_governance_center
from ai_operations_center.human_review_analytics import build_human_review_analytics


def build_ai_ops_report():
    report = {
        "agent_reliability": build_scorecard(),
        "cost_governance": build_cost_governance_center(),
        "human_review": build_human_review_analytics(),
        "platform_status": "watch",
        "release_recommendation": "hold_noncritical_ai_changes"
    }

    Path("ai_operations_center/ai_operations_report.json").write_text(
        json.dumps(report, indent=2)
    )
    return report


if __name__ == "__main__":
    print(json.dumps(build_ai_ops_report(), indent=2))
