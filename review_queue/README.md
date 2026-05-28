# Human Review Lifecycle

## Purpose

This artifact models the governance path for blocked AgentGrid outputs.

## Lifecycle

```text
agent output
→ eval-gate block
→ human review
→ approval / rejection
→ release or continued block
States
blocked
reviewed
approved
rejected
released
release_blocked
Why This Matters

Human review workflows provide governance and safety controls for operational GenAI systems where unsupported answers should not reach users without review.

Scope

This is a deterministic lifecycle proof. It does not claim production moderation or enterprise approval infrastructure.
