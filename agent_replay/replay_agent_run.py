import json
from pathlib import Path


def replay_run(run_path="agent_replay/saved_runs/run_1023.json"):
    saved = json.loads(Path(run_path).read_text())
    state = saved["state"]

    replay = {
        "run_id": saved["run_id"],
        "trace_id": saved["trace_id"],
        "replayed_steps": [
            "load_saved_graph_state",
            "inspect_retrieved_context",
            "inspect_tool_history",
            "compare_eval_before_after",
            "resume_from_review_checkpoint"
        ],
        "tool_call_history": state["tool_history"],
        "before_eval": state["eval_before_review"],
        "checkpoint": state["human_review_checkpoint"],
        "replay_status": "ready_for_resume"
    }

    Path("agent_replay/replay_report.json").write_text(json.dumps(replay, indent=2))
    return replay


if __name__ == "__main__":
    print(json.dumps(replay_run(), indent=2))
