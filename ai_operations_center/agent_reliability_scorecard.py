import json
from pathlib import Path


def build_scorecard():
    scorecard = {
        "retrieval": 0.82,
        "tool_success": 0.91,
        "hallucination_risk": 0.07,
        "latency_health": 0.86,
        "review_readiness": 0.88,
        "overall_reliability_score": 0.85,
        "status": "watch",
        "recommended_action": "monitor retrieval quality and hallucination-risk trend"
    }

    Path("ai_operations_center/agent_reliability_scorecard.json").write_text(
        json.dumps(scorecard, indent=2)
    )
    return scorecard


if __name__ == "__main__":
    print(json.dumps(build_scorecard(), indent=2))
