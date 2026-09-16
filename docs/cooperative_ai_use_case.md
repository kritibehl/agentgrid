# Cooperative AI Use Case: Support Automation

## Problem

Support teams need AI systems that assist with triage and next actions without silently releasing unsupported or unsafe answers.

## Cooperative Workflow

AgentGrid models AI as a cooperative assistant:

```text
human/customer issue
→ AI triage
→ knowledge retrieval
→ draft next action
→ eval gate
→ human review
→ feedback loop
Human + AI Responsibilities
Responsibility	AI	Human
Classify issue	yes	review edge cases
Retrieve knowledge	yes	validate critical evidence
Draft next action	yes	approve risky actions
Detect unsupported claims	yes	confirm final decision
Own operational outcome	no	yes
Why This Matters

The workflow improves support speed while keeping humans responsible for risky operational or unsupported outputs.
