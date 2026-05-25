from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import List, Dict
from uuid import uuid4


@dataclass
class AgentRun:
    run_id: str
    trace_id: str
    user_query: str
    final_decision: str
    retrieval_hit_rate: float
    tool_call_status: str
    human_review_required: bool
    created_at: str


RUNS: Dict[str, AgentRun] = {}


def record_run(user_query: str, final_decision: str, retrieval_hit_rate: float, tool_call_status: str) -> dict:
    run = AgentRun(
        run_id=f"run_{uuid4().hex[:10]}",
        trace_id=f"trace_{uuid4().hex[:10]}",
        user_query=user_query,
        final_decision=final_decision,
        retrieval_hit_rate=retrieval_hit_rate,
        tool_call_status=tool_call_status,
        human_review_required=final_decision in ("hold", "escalate"),
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    RUNS[run.run_id] = run
    return asdict(run)


def list_runs() -> List[dict]:
    return [asdict(run) for run in RUNS.values()]


def get_human_review_queue() -> List[dict]:
    return [asdict(run) for run in RUNS.values() if run.human_review_required]


def compare_workflows() -> dict:
    return {
        "baseline_single_agent": {
            "steps": ["classify", "answer", "manual_review"],
            "risk": "higher unsupported-answer risk"
        },
        "agentgrid_multi_agent": {
            "steps": ["triage", "retrieval", "tool_execution", "eval_gate", "escalation"],
            "risk": "lower unsupported-answer risk through explicit checks"
        }
    }
