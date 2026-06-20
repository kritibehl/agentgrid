from pathlib import Path
import json

for d in ["docs", "reports", "examples", "frontend/screenshots"]:
    Path(d).mkdir(parents=True, exist_ok=True)

Path("docs/architecture.md").write_text("""# AgentGrid Architecture

## Problem

Silent AI workflow failures can look correct while missing retrieval evidence, misusing tools, inventing claims, or skipping human review.

## Architecture

User request
→ classify
→ retrieve
→ tool call
→ structured answer
→ validation
→ eval gate
→ release / human review
→ handoff report
""")

Path("docs/agent_failure_modes.md").write_text("""# Agent Failure Modes

| Failure mode | Detection signal | Response |
|---|---|---|
| Retrieval miss | no grounding context | hold |
| Tool timeout | retry threshold exceeded | retry / escalate |
| Hallucinated claim | unsupported by evidence | block |
| Schema violation | missing required field | fail validation |
| Unsafe action | high-risk operation | human review |
| Eval regression | quality drop | hold release |
""")

Path("docs/evaluation_methodology.md").write_text("""# Evaluation Methodology

AgentGrid evaluates:

- retrieval hit rate
- tool-call correctness
- structured-output validity
- groundedness
- hallucination risk
- unsafe-answer refusal
- handoff quality
- latency and cost
- human-review outcomes

Gate decisions: ship, hold, escalate.
""")

Path("docs/product_requirements_ai_workflows.md").write_text("""# Product Requirements: AI Workflow Safety

## Problem

AI workflows can fail silently when outputs look plausible but lack evidence or skip review.

## Goal

Detect unsafe or unsupported outputs before they reach users.

## Requirements

- classify request
- retrieve grounding context
- execute traceable tools
- validate structured output
- run eval gate
- route risky outputs to human review
- generate handoff report

## Success Metrics

- retrieval hit rate >= 0.85
- tool success rate >= 0.90
- eval pass rate >= 0.80
- unsupported release rate = 0
""")

trace = {
    "trace_id": "ag_trace_001",
    "workflow": "ai_support_triage",
    "input": "The agent gave an unsupported deployment fix.",
    "steps": [
        {"stage": "classify", "output": "support_incident"},
        {"stage": "retrieve", "retrieval_hit": True, "docs": ["runbook: missing evidence requires hold"]},
        {"stage": "tool_call", "tool": "validate_claim", "status": "success", "latency_ms": 120},
        {"stage": "structured_answer", "schema_valid": True},
        {"stage": "eval_gate", "decision": "hold", "reason": "unsupported_fix_claim"},
        {"stage": "human_review", "status": "queued", "owner": "support_reviewer"}
    ],
    "metrics": {
        "retrieval_hit_rate": 1.0,
        "tool_success": True,
        "latency_ms": 820,
        "estimated_cost": 0.0145
    }
}
Path("reports/sample_agent_run_trace.json").write_text(json.dumps(trace, indent=2))

Path("reports/eval_gate_report.md").write_text("""# Eval Gate Report

| Check | Result |
|---|---|
| Schema validity | PASS |
| Retrieval grounding | PASS |
| Tool-call success | PASS |
| Unsupported claim risk | FAIL |
| Human review required | YES |

Decision: HOLD

Reason: unsupported deployment-fix claim.
""")

Path("reports/human_review_decisions.md").write_text("""# Human Review Decisions

| Review ID | Trace ID | Reason | Decision |
|---|---|---|---|
| review_001 | ag_trace_001 | unsupported_fix_claim | approved_after_edit |
| review_002 | ag_trace_002 | missing_retrieval | rejected |
| review_003 | ag_trace_003 | unsafe_action | escalated |
""")

workflow = {
    "workflow": "ai_authoring_workflow",
    "input": {
        "user_context": "Summarize support-risk trends for an AI workflow release.",
        "required_sections": ["summary", "evidence", "risks", "recommendation"]
    },
    "steps": [
        "retrieve_context",
        "draft_structured_report",
        "validate_groundedness",
        "eval_gate",
        "human_review_if_needed"
    ],
    "output": {
        "summary": "Release quality improved after agent_v2, but unsupported claims still require review.",
        "evidence": [
            "eval pass rate increased",
            "cost per run decreased",
            "human review catches unsupported claims"
        ],
        "risks": ["retrieval drift", "tool timeout"],
        "recommendation": "ship with monitoring"
    },
    "eval_gate": {
        "groundedness": "pass",
        "unsupported_claims": "none",
        "decision": "ship"
    }
}
Path("examples/ai_authoring_workflow.json").write_text(json.dumps(workflow, indent=2))

Path("examples/groundedness_eval.json").write_text(json.dumps({
    "report_id": "authoring_eval_001",
    "groundedness_score": 0.92,
    "unsupported_claims": 0,
    "missing_evidence": 0,
    "decision": "ship"
}, indent=2))

Path("examples/authoring_report.md").write_text("""# AI Authoring Workflow Report

AgentGrid converts user context into a structured report and checks whether the final output is grounded in retrieved evidence.

## Evidence

- Eval pass rate improved after workflow changes.
- Cost per run decreased in version benchmarking.
- Human review catches unsupported or risky outputs.

## Recommendation

Ship with continued monitoring, eval gates, and human-review routing.
""")

try:
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (1400, 850), (15, 23, 42))
    d = ImageDraw.Draw(img)
    d.text((60, 50), "AgentGrid Dashboard", fill=(240, 249, 255))
    d.text((60, 105), "Silent AI workflow failure prevention", fill=(147, 197, 253))
    cards = [
        ("Retrieval Hit Rate", "0.90"),
        ("Tool Success", "0.91"),
        ("Eval Decision", "HOLD"),
        ("Human Review", "Queued"),
        ("Avg Cost", "$0.0145"),
        ("p95 Latency", "820 ms"),
    ]
    for i, (label, value) in enumerate(cards):
        x = 60 + (i % 3) * 420
        y = 170 + (i // 3) * 190
        d.rounded_rectangle((x, y, x + 360, y + 140), radius=20, fill=(30, 41, 59), outline=(96, 165, 250), width=3)
        d.text((x + 25, y + 30), label, fill=(203, 213, 225))
        d.text((x + 25, y + 75), value, fill=(125, 211, 252))
    d.text((60, 610), "Trace: classify → retrieve → tool call → answer → eval → human review", fill=(226, 232, 240))
    img.save("frontend/screenshots/agent_dashboard.png")
except Exception:
    Path("frontend/screenshots/agent_dashboard.png").write_bytes(b"placeholder")

print("Flagship story layer generated.")
