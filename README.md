# AgentGrid

<!-- AGENTGRID_RELIABILITY_HERO -->

## AgentGrid — AI Reliability Platform for Agentic Workflows

AgentGrid tests whether agentic AI workflows can survive retrieval, tool, grounding, schema, and latency failures without silently releasing invalid output.

**Ungated baseline**

    retrieve -> generate -> return

**AgentGrid**

    retrieve -> tools -> evaluate -> SHIP / HOLD / RETRY / ESCALATE

### Adversarial Reliability Benchmark

The deterministic `adversarial-v1` suite injects retrieval misses, irrelevant and contradictory context, stale and poisoned knowledge, transient and repeated tool failures, malformed tool results, unsupported claims, schema failures, latency-budget breaches, and partial dependency failures.

AgentGrid measures failure escapes, unsupported outputs, retrieval and grounding containment, tool recovery, gate precision/recall, false escalation, and modeled latency/token/cost overhead.

Each run also produces an explainable execution trace across:

    retrieval -> tool -> model -> evaluation -> terminal route

### Real MCP Tooling

AgentGrid exposes and invokes operational tools through the Model Context Protocol:

- `search_docs`
- `analyze_logs`
- `query_metrics`
- `create_action_plan`

Run the full demonstration with:

    make demo

> Scope: `adversarial-v1` is deterministic local fault injection. Latency, token, and cost figures are modeled values, not live-provider measurements.



**Production-style agent orchestration with retrieval, tools, evaluation gates and human review.**

`Python` · `FastAPI` · `React` · `TypeScript` · `Redis` · `Prometheus`

🔗 **[Live Demo](https://agentgrid-seven.vercel.app)**

---

## Why This Exists

**Problem:** Production GenAI systems fail in ways that are hard to observe: retrieval misses the relevant document, a tool call silently returns a stale result, an answer is generated without grounding. Aggregate pass rates hide these gaps.

**Impact:** AI systems that look correct in demos fail on real queries. Without eval gates and escalation routing, bad outputs reach users with no mechanism for detection or review.

**Proof:** Full orchestration pipeline with per-stage metrics, eval gates, and human review routing. Retrieval hit rate 80%, tool success rate 80%, p95 latency 880ms — all measured and gated per run, resulting in a `HOLD` decision rather than a ship.

---

## Latest Project Output

```json
{
  "retrieval_hit_rate": 0.80,
  "tool_success_rate": 0.80,
  "p95_latency_ms": 880,
  "human_review_gates": "enabled",
  "release_decision": "HOLD"
}
```

## Live Metrics Snapshot

| Signal | Value |
|---|---|
| Retrieval Hit Rate | **80%** |
| Tool Success Rate | **80%** |
| P95 Latency | **880ms** |
| Human Review Gates | **Enabled** |

---

## System Flow

```
User query
      │
      ▼
Triage agent
      │
      ▼
Retrieval agent  →  RAG over docs / logs / runbooks
      │
      ▼
MCP tool execution
      │
      ▼
Answer generation
      │
      ▼
Evaluation gate  →  SHIP / HOLD / ESCALATE
      │
      ▼
Human review (if escalated)  →  reviewer workflows · audit logs
```

## Agent Reliability Scorecard

| Eval Dimension | Coverage |
|---|---|
| Retrieval quality | RAG over docs / logs / runbooks |
| Tool execution | MCP-style tool server · success/failure rates |
| Latency | p95 per workflow stage |
| Cost | Per-run cost tracking |
| Drift detection | Model version regression signals |
| Escalation routing | Human review gates · reviewer workflows |
| Guardrails | Output quality gates · HOLD / SHIP / ESCALATE |

---

## Architecture

```
AgentGrid/
  Orchestration layer   triage → retrieval → tools → generation
  Eval warehouse        retrieval quality · tool metrics · latency · cost
  Escalation router     HOLD / SHIP / ESCALATE + human review gates
  Observability         trace IDs · audit logs · Prometheus metrics
  Frontend              React/TypeScript dashboard + trace viewer
```

## Agent Version Benchmarking

Compares agent releases head-to-head (`agent_v1` vs `agent_v2`) on retrieval hit rate, tool success rate, p95 latency, cost per run, eval pass rate, and the resulting release decision. See `agent_version_benchmark/`.

## MCP Gateway Infrastructure

A tool-server gateway layer with a tool registry, tool health reporting, MCP call tracing, and workflow-trigger/incident-lookup tools. See `mcp_gateway/`.

## Support Automation Case Study

An end-to-end example of a customer/internal issue becoming a structured, gated AI workflow: issue intake → knowledge retrieval → classification → next-action/escalation draft → eval gate → human review → feedback loop. See `examples/support_automation_workflow.json` and `docs/support_automation_architecture.md`.

---

## Repository Structure

```
agentgrid/
├── agents/          Triage · retrieval · generation agents
├── tools/            MCP-style tool server
├── rag/               Retrieval over docs / logs / runbooks
├── eval/               Evaluation gates · scorecard · drift detection
├── escalation/          Human review routing · reviewer workflows
├── frontend/              React/TypeScript dashboard + trace viewer
├── observability/          Prometheus metrics · trace exports · audit logs
├── agent_version_benchmark/  Agent-release comparison
├── mcp_gateway/                Tool registry + health checks
└── reports/                     Eval outputs (CI-generated)
```

## Run Locally

```bash
git clone https://github.com/kritibehl/agentgrid && cd agentgrid
pip install -r requirements.txt
make demo    # full agent workflow run
make eval    # eval suite → reports/latest/agent_reliability_scorecard.json
make test    # 65 tests
```

## Tests

```bash
make test
# → 65 tests passing
# Retrieval hit rate: 0.80 · Tool success rate: 0.80 · p95 latency: 880ms
```

## Selected Outputs

**Eval gate decision:**
```json
{
  "retrieval_hit_rate": 0.80,
  "tool_success_rate": 0.80,
  "p95_latency_ms": 880,
  "cost_per_run_avg": 0.0132,
  "release_decision": "HOLD",
  "hold_reason": "quality risk on entity search scenario"
}
```
