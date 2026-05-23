import json
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone


BAD_ANSWER_EVENT = {
    "input": "Why did deployment fail?",
    "bad_genai_answer": "The deployment failed because the database cluster was definitely overloaded and has now recovered.",
    "available_context": [
        "deployment logs mention DB timeout",
        "retrieval did not return the DB saturation runbook",
        "no database health snapshot was available"
    ],
    "detected_failures": [
        "unsupported_root_cause_claim",
        "missing_retrieval_grounding",
        "insufficient_evidence"
    ]
}


def agentgrid_detect(event):
    return {
        "trace_id": "trace_e2e_001",
        "decision_id": "decision_e2e_001",
        "final_decision": "hold",
        "reason": "missing_retrieval_grounding",
        "unsupported_answer": True,
        "unsupported_claims": [
            "database cluster was definitely overloaded",
            "has now recovered"
        ],
        "eval_gate": {
            "groundedness": "fail",
            "unsupported_detail_risk": "high",
            "missing_context": True,
            "safe_to_ship": False
        }
    }


def create_escalation_artifact(agentgrid_result):
    return {
        "system": "jira_style_issue",
        "issue_type": "GenAI Support Escalation",
        "summary": "Unsupported GenAI deployment explanation blocked by AgentGrid eval gate",
        "severity": "high",
        "trace_id": agentgrid_result["trace_id"],
        "decision_id": agentgrid_result["decision_id"],
        "owner": "ai_support_engineering",
        "support_action": "Request DB health snapshot and matching runbook evidence before answering.",
        "engineering_escalation_summary": "AgentGrid detected unsupported root-cause claims and missing retrieval grounding in a deployment-support answer."
    }


def autoops_classify(escalation):
    prior_issues = [
        "missing_retrieval_grounding",
        "retry_amplification_missing_context",
        "missing_retrieval_grounding",
        "unsupported_root_cause_claim",
        "missing_retrieval_grounding"
    ]

    counts = Counter(prior_issues)

    return {
        "incident_type": "genai_support_quality_issue",
        "severity": "sev2",
        "recurring_issue_family": "missing_retrieval_grounding",
        "repeat_count": counts["missing_retrieval_grounding"],
        "is_recurring": counts["missing_retrieval_grounding"] >= 2,
        "recommended_route": "support_reviewer_queue",
        "linked_trace_id": escalation["trace_id"]
    }


def generate_rca_and_feedback(agentgrid_result, autoops_result):
    return {
        "rca_summary": "The support answer was blocked because it asserted a definitive database-overload root cause without sufficient retrieved evidence.",
        "probable_cause_hypothesis": "The likely workflow failure is missing retrieval grounding rather than a confirmed database outage.",
        "missing_diagnostics": [
            "database health snapshot",
            "connection pool metrics",
            "matching DB saturation runbook",
            "trace-correlated deployment logs"
        ],
        "product_feedback_summary": "Improve retrieval coverage for deployment-failure runbooks and surface missing-evidence warnings earlier in the support flow.",
        "support_response_draft": "I do not have enough evidence to confirm the deployment root cause yet. Please provide the DB health snapshot, connection pool metrics, and trace-correlated logs so we can safely continue.",
        "customer_impact": "Prevents unsupported root-cause explanations from reaching users.",
        "next_actions": [
            "Hold answer until evidence is available",
            "Route trace to support reviewer",
            "Add missing runbook to retrieval corpus",
            "Track recurrence under missing_retrieval_grounding"
        ],
        "release_safety_outcome": "blocked_from_shipping",
        "autoops_recurring_issue": autoops_result["recurring_issue_family"]
    }


def build_report():
    agentgrid_result = agentgrid_detect(BAD_ANSWER_EVENT)
    escalation = create_escalation_artifact(agentgrid_result)
    autoops_result = autoops_classify(escalation)
    rca = generate_rca_and_feedback(agentgrid_result, autoops_result)

    payload = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "bad_answer_event": BAD_ANSWER_EVENT,
        "agentgrid_detection": agentgrid_result,
        "escalation_artifact": escalation,
        "autoops_classification": autoops_result,
        "rca_and_product_feedback": rca
    }

    Path("demo_outputs/end_to_end_ai_support_incident.json").write_text(json.dumps(payload, indent=2))

    md = f"""# End-to-End AI Support Incident Demo

## Scenario

A GenAI support workflow produced an unsafe deployment explanation:

> "{BAD_ANSWER_EVENT['bad_genai_answer']}"

AgentGrid detected that the answer contained unsupported root-cause claims and missing retrieval grounding.

## End-to-End Flow

```text
bad GenAI support answer
→ AgentGrid detects unsupported / missing context
→ escalation artifact created
→ AutoOps classifies recurring issue
→ RCA + product feedback summary generated
1. AgentGrid Detection
Field	Value
Trace ID	{agentgrid_result['trace_id']}
Decision ID	{agentgrid_result['decision_id']}
Final decision	{agentgrid_result['final_decision'].upper()}
Reason	{agentgrid_result['reason']}
Unsupported answer	{agentgrid_result['unsupported_answer']}
Safe to ship	{agentgrid_result['eval_gate']['safe_to_ship']}
Unsupported Claims
database cluster was definitely overloaded
has now recovered
2. Escalation Artifact
Field	Value
System	{escalation['system']}
Issue type	{escalation['issue_type']}
Severity	{escalation['severity']}
Owner	{escalation['owner']}
Engineering Escalation Summary

{escalation['engineering_escalation_summary']}

3. AutoOps Classification
Field	Value
Incident type	{autoops_result['incident_type']}
Severity	{autoops_result['severity']}
Recurring issue family	{autoops_result['recurring_issue_family']}
Repeat count	{autoops_result['repeat_count']}
Recommended route	{autoops_result['recommended_route']}
4. RCA Summary

{rca['rca_summary']}

Probable-Cause Hypothesis

{rca['probable_cause_hypothesis']}

Missing Diagnostics
database health snapshot
connection pool metrics
matching DB saturation runbook
trace-correlated deployment logs
5. Product Feedback Summary

{rca['product_feedback_summary']}

6. Support Response Draft

{rca['support_response_draft']}

7. Outcome
Outcome	Value
Release safety outcome	{rca['release_safety_outcome']}
Customer impact	{rca['customer_impact']}
AutoOps recurring issue	{rca['autoops_recurring_issue']}
Why This Matters

This demo connects AgentGrid and AutoOps into one operational loop:

unsafe AI answer detection
eval-gate blocking
support escalation
recurring issue classification
RCA generation
product feedback generation

This is the core FDE / TAM / AI-support workflow.
"""

Path("demo_outputs/end_to_end_ai_support_incident.md").write_text(md)
return payload

if name == "main":
print(json.dumps(build_report(), indent=2))
