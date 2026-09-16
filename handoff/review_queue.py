import json
from pathlib import Path

def build_review_queue():
    item = {
        "handoff_id": "handoff_001",
        "agent_output": "Missing retrieval context detected.",
        "risk_score": 0.72,
        "review_status": "needs_review",
        "owner": "support_reviewer",
        "runbook_note": "Validate retrieved evidence before release."
    }
    report = {"queue_size": 1, "items": [item], "decision": "route_to_human_review"}
    Path("handoff/sample_handoff_report.md").write_text("# Sample Handoff Report\n\nRisky output routed to human review with runbook-style ownership note.\n")
    Path("handoff/handoff_report.json").write_text(json.dumps(report, indent=2))
    return report

if __name__ == "__main__":
    print(json.dumps(build_review_queue(), indent=2))
