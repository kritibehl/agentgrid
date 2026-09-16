# AgentGrid Architecture

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
