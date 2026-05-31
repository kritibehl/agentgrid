import json
from pathlib import Path

from agent_replay.replay_agent_run import replay_run


def resume_after_review(approved=True):
    replay = replay_run()

    after_eval = {
        "decision": "ship" if approved else "escalate",
        "reason": "reviewer_approved_fallback" if approved else "reviewer_escalated"
    }

    result = {
        "run_id": replay["run_id"],
        "trace_id": replay["trace_id"],
        "resumed_from_checkpoint": True,
        "before_eval": replay["before_eval"],
        "after_eval": after_eval,
        "final_status": "released" if approved else "escalated"
    }

    Path("agent_replay/human_review_resume_report.json").write_text(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    print(json.dumps(resume_after_review(), indent=2))
