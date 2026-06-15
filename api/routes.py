from fastapi import APIRouter
from claude_workflows.claude_tool_runner import run_claude_style_workflow
from runtime_telemetry.collect_runtime_metrics import collect_metrics

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/run-agent")
def run_agent(payload: dict):
    return run_claude_style_workflow(payload)

@router.post("/evaluate")
def evaluate(payload: dict):
    return {"eval_status": "pass", "release_decision": "ship", "request": payload}

@router.get("/metrics")
def metrics():
    return collect_metrics()

@router.get("/runs/{run_id}")
def get_run(run_id: str):
    return {"run_id": run_id, "status": "available"}
