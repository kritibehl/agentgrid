# End-to-End AI Support Incident Demo

## Scenario

A GenAI support workflow produced an unsafe deployment explanation:

> "The deployment failed because the database cluster was definitely overloaded and has now recovered."

AgentGrid detected unsupported root-cause claims and missing retrieval grounding.

## End-to-End Flow

bad GenAI support answer
→ AgentGrid detects unsupported/missing context
→ escalation artifact created
→ AutoOps classifies recurring issue
→ RCA + product feedback summary generated

## AgentGrid Detection

- Final decision: HOLD
- Unsupported answer: True
- Safe to ship: False
- Reason: missing_retrieval_grounding

## Unsupported Claims

- database cluster was definitely overloaded
- has now recovered

## AutoOps Classification

- Recurring issue family: missing_retrieval_grounding
- Repeat count: 3
- Recommended route: support_reviewer_queue

## RCA Summary

The support answer was blocked because it asserted a definitive database-overload root cause without sufficient retrieved evidence.

## Product Feedback

Improve retrieval coverage for deployment-failure runbooks and surface missing-evidence warnings earlier in the support flow.

## Outcome

- Release safety outcome: blocked_from_shipping
- Customer impact: Prevents unsupported root-cause explanations from reaching users.

## Why This Matters

This demo connects:
- unsupported-answer detection
- eval-gate blocking
- escalation workflows
- recurring issue classification
- RCA generation
- product feedback generation

into one operational GenAI support workflow.
