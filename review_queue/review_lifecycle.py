import json
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4


def now():
    return datetime.now(timezone.utc).isoformat()


def create_review_item(agent_output: str, reason: str) -> dict:
    return {
        "review_id": f"review_{uuid4().hex[:10]}",
        "agent_output": agent_output,
        "reason": reason,
        "status": "blocked",
        "history": [
            {
                "status": "blocked",
                "actor": "eval_gate",
                "timestamp": now(),
                "note": reason
            }
        ]
    }


def review_item(item: dict, reviewer: str, approved: bool, note: str) -> dict:
    item["status"] = "approved" if approved else "rejected"
    item["history"].append({
        "status": item["status"],
        "actor": reviewer,
        "timestamp": now(),
        "note": note
    })
    return item


def release_item(item: dict, actor: str) -> dict:
    if item["status"] != "approved":
        item["history"].append({
            "status": "release_blocked",
            "actor": actor,
            "timestamp": now(),
            "note": "Item must be approved before release."
        })
        return item

    item["status"] = "released"
    item["history"].append({
        "status": "released",
        "actor": actor,
        "timestamp": now(),
        "note": "Reviewed output released."
    })
    return item


def run_review_lifecycle() -> dict:
    item = create_review_item(
        agent_output="The database was definitely overloaded and recovered.",
        reason="unsupported_root_cause_claim"
    )

    item = review_item(
        item,
        reviewer="human_reviewer",
        approved=True,
        note="Edited response to remove unsupported certainty and request DB health evidence."
    )

    item = release_item(item, actor="release_manager")

    report = {
        "workflow": "human_review_lifecycle",
        "final_status": item["status"],
        "review_id": item["review_id"],
        "history_count": len(item["history"]),
        "governance_path": ["blocked", "reviewed", "approved", "released"],
        "item": item
    }

    Path("review_queue/review_lifecycle_report.json").write_text(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    print(json.dumps(run_review_lifecycle(), indent=2))
