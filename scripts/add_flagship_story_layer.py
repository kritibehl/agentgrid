from pathlib import Path
import json

Path("docs").mkdir(exist_ok=True)
Path("reports").mkdir(exist_ok=True)
Path("examples").mkdir(exist_ok=True)
Path("frontend/screenshots").mkdir(parents=True, exist_ok=True)

files = {}

files["docs/architecture.md"] = """# AgentGrid Architecture

## Problem

Silent AI workflow failures are dangerous because outputs can look correct while missing retrieval evidence, misusing tools, inventing claims, or skipping human review.

## Architecture

```text
User request
→ classify
→ retrieve
→ tool call
→ structured answer
→ validation
→ eval gate
→ release / human review
→ handoff report
Core Components
Component	Purpose
Classification	Routes the request to the correct workflow
Retrieval	Pulls grounding context before generation
Tool calls	Executes external workflow actions
Structured output	Keeps responses machine-checkable
Validation	Checks schema, grounding, and unsafe actions
Eval gate	Decides ship / hold / escalate
Human review	Handles risky or unsupported outputs
Handoff	Converts reviewed output into an operational note
Scope

AgentGrid is a production-style prototype. It does not claim production traffic, enterprise deployment, or autonomous decision-making.
"""

files["docs/agent_failure_modes.md"] = """# Agent Failure Modes

AgentGrid treats AI failures as workflow states, not just model errors.

Failure mode	Detection signal	System response
Retrieval miss	no grounding context found	hold + request evidence
Tool timeout	tool latency/retry threshold exceeded	retry + escalate
Hallucinated claim	claim unsupported by retrieved context	block + human review
Schema violation	structured output missing required fields	fail validation
Unsafe action	operational action without review	block release
High latency	p95 threshold exceeded	degrade or hold
Eval regression	pass rate drops vs baseline	hold release
Human override	reviewer changes agent output	log decision
Why This Matters

The goal is to prevent AI outputs from silently reaching users when evidence, safety, or workflow quality is insufficient.
"""

files["docs/evaluation_methodology.md"] = """# Evaluation Methodology

Evaluation Layers

AgentGrid evaluates AI workflows across:

retrieval hit rate
tool-call correctness
structured-output validity
groundedness
hallucination risk
unsafe-answer refusal
handoff quality
cost and latency
human-review outcomes
Gate Decisions
Decision	Meaning
ship	output is grounded and valid
hold	output needs more evidence or validation
escalate	output needs human or operational review
Evaluation Artifacts
Promptfoo-style regression checks
RAGAS-style retrieval evaluation
trace analytics
cost governance
human review decisions
version benchmarking
Success Criteria
retrieval hit rate above threshold
tool success above threshold
eval pass rate stable or improving
no unsupported high-risk claims released
risky outputs routed to human review
"""

files["docs/product_requirements_ai_workflows.md"] = """# Product Requirements: AI Workflow Safety

Problem

AI workflow failures can be silent. A response may appear fluent while missing evidence, skipping tools, or making unsupported claims.

Goal

Build a workflow platform that detects unsafe or unsupported AI outputs before they reach users.

Primary Users
AI engineers
applied AI teams
support engineers
reviewers
AI product managers
Core Requirements
Requirement	Description
R1	Classify incoming workflow request
R2	Retrieve grounding context
R3	Execute tool calls with traceability
R4	Return structured output
R5	Validate schema and claims
R6	Run eval gate
R7	Route risky outputs to human review
R8	Generate handoff report
Success Metrics
Metric	Target
Retrieval hit rate	>= 0.85
Tool success rate	>= 0.90
Eval pass rate	>= 0.80
Human review routing accuracy	>= 0.90
Unsupported release rate	0
Non-Goals
autonomous production decision-making
real enterprise traffic
replacing human review for risky outputs
"""

sample_trace = {
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
files["reports/sample_agent_run_trace.json"] = json.dumps(sample_trace, indent=2)

files["reports/eval_gate_report.md"] = """# Eval Gate Report

Summary
Check	Result
Schema validity	PASS
Retrieval grounding	PASS
Tool-call success	PASS
Unsupported claim risk	FAIL
Human review required	YES
Decision

HOLD

Reason

The answer included an unsupported deployment-fix claim. AgentGrid blocked release and routed the output to human review.
"""

files["reports/human_review_decisions.md"] = """# Human Review Decisions

Review ID	Trace ID	Reason	Decision	Reviewer Action
review_001	ag_trace_001	unsupported_fix_claim	approved_after_edit	removed unsupported certainty
review_002	ag_trace_002	missing_retrieval	rejected	requested additional evidence
review_003	ag_trace_003	unsafe_action	escalated	routed to release manager
Summary

Human review is used when automated validation detects missing evidence, unsupported claims, or unsafe operational actions.
"""

files["examples/ai_authoring_workflow.json"] = json.dumps({
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
"evidence": ["eval pass rate increased", "cost per run decreased", "human review catches unsupported claims"],
"risks": ["retrieval drift", "tool timeout"],
"recommendation": "ship with monitoring"
},
"eval_gate": {
"groundedness": "pass",
"unsupported_claims": "none",
"decision": "ship"
}
}, indent=2)

files["examples/groundedness_eval.json"] = json.dumps({
"report_id": "authoring_eval_001",
"groundedness_score": 0.92,
"unsupported_claims": 0,
"missing_evidence": 0,
"decision": "ship"
}, indent=2)

files["examples/authoring_report.md"] = """# AI Authoring Workflow Report

Summary

AgentGrid converts user context into a structured report and checks whether the final output is grounded in retrieved evidence.

Evidence
Eval pass rate improved after workflow changes.
Cost per run decreased in version benchmarking.
Human review catches unsupported or risky outputs.
Risks
Retrieval drift can reduce grounding quality.
Tool timeouts can block release.
High-risk claims require reviewer approval.
Recommendation

Ship the workflow with continued monitoring, eval gates, and human-review routing.
"""

for path, content in files.items():
Path(path).parent.mkdir(parents=True, exist_ok=True)
Path(path).write_text(content)

Generate a lightweight PNG screenshot if Pillow exists.

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
x, y = 60, 170
for i, (label, value) in enumerate(cards):
x = 60 + (i % 3) * 420
y = 170 + (i // 3) * 190
d.rounded_rectangle((x, y, x + 360, y + 140), radius=20, fill=(30, 41, 59), outline=(96, 165, 250), width=3)
d.text((x + 25, y + 30), label, fill=(203, 213, 225))
d.text((x + 25, y + 75), value, fill=(125, 211, 252))
d.text((60, 610), "Trace: classify → retrieve → tool call → answer → eval → human review", fill=(226, 232, 240))
img.save("frontend/screenshots/agent_dashboard.png")
except Exception:
Path("frontend/screenshots/agent_dashboard.png").write_bytes(b"")

print("Flagship story layer generated.")
