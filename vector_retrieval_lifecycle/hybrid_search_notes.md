# Hybrid Search Notes

## Goal

Combine lexical retrieval and semantic retrieval for operational support workflows.

## Retrieval Strategy

```text
query
→ lexical keyword search
→ semantic vector retrieval
→ merged ranking
→ eval-gate grounding checks
Why Hybrid Retrieval

Lexical retrieval helps:

exact incident IDs
deployment names
trace IDs
error codes

Semantic retrieval helps:

related incidents
paraphrased runbook content
support summaries
RCA context
Example
Query	Lexical benefit	Semantic benefit
"DB timeout"	exact timeout string	related saturation incidents
"unsupported answer"	exact eval-gate docs	similar hallucination patterns
Scope

This is a retrieval-design artifact for operational AI systems.
