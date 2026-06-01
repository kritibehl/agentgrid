# AgentGrid

> A production-style GenAI operations platform that orchestrates AI support workflows with retrieval, MCP-style tool use, eval gates, cost governance, and structured escalation.

`Python` · `LangGraph` · `FastAPI` · `Prometheus` · `Redis` · `Docker`

🔗 **[Live Demo](https://agentgrid-seven.vercel.app/)**

---

## Why This Project Matters

- GenAI support systems fail silently: answers ship without retrieval context, with unsupported claims, or after tool failures — no gate stops them
- AgentGrid puts a 5-signal eval gate between generation and the user: every answer must pass correctness, citation coverage, hallucination risk, safety, and latency checks before it ships
- Unsafe or low-confidence answers escalate to human review with full AutoOps context attached — they don't ship with a disclaimer
- This proves: agentic workflow design, eval gate engineering, retrieval system discipline, and operational AI tooling judgment

---

## 30-Second Proof

| Signal | Verified output |
|---|---|
| Unsafe outputs shipped | **0** across 25 validation runs |
| Retrieval hit rate drift detected | 0.91 → 0.76 → **HOLD** |
| Projected spend vs budget | $700 vs $500 → **HOLD** |
| Gate decisions | 9 ship · 10 hold · 6 escalate |
| p95 latency | 258ms |
| Tool-call success rate | 0.88 |
| Tests | 54 passing |

---

## Screenshots

> Add these to `docs/screenshots/` — they are the highest ROI improvement remaining.

| Trace View | Eval Gate Decision |
|---|---|
| ![Trace View](screenshots/workflow_trace.png) | ![Eval Gate](screenshots/eval_gate.png) |

| Cost Governance | Operational Dashboard |
|---|---|
| ![Cost Governance](screenshots/latency_cost_report.png) | ![Dashboard](screenshots/dashboard.png) |

**Request lifecycle — what the trace view shows:**

```
User query: "Deployment failed — DB timeout causing retry storm"
      │
      ▼  [retrieve_context]  hit_rate=0.88  citations=3
      │
      ▼  [analyze_logs]      tool_status=success  pattern=retry_storm
      │
      ▼  [create_action_plan] recommended_action="reduce connection pool size"
      │
      ▼  [generate_answer]   tokens=312  cost=$0.0004
      │
      ▼  [eval_gate]
            correctness:        PASS
            citation_coverage:  FAIL  ← 0% on one claim
            hallucination_risk: PASS
            safety:             PASS
            latency:            PASS
      │
      ▼  decision: HOLD  →  queued for human review
         autoops_event: { incident_type: "low_citation_coverage" }
```

---

## Demo

```bash
git clone https://github.com/kritibehl/agentgrid-demo
cd agentgrid-demo
make demo
```

Expected output:
```json
{
  "eval_gate": {
    "correctness": true,
    "citation_coverage": false,
    "final_decision": "hold"
  },
  "metrics": {
    "latency_seconds": 0.0028,
    "tool_call_success_rate": 1.0,
    "tokens_used": 312,
    "estimated_cost_usd": 0.0004
  },
  "autoops_event": {
    "incident_type": "low_citation_coverage",
    "escalated": false,
    "hold_reason": "citation_coverage"
  }
}
```

```bash
make test    # 54 tests · 0 unsafe outputs
make report  # batch summary → reports/mixed_batch/mock_summary.json
```

---

## Architecture

![AgentGrid Architecture](screenshots/architecture_hero.png)

```
User query
      │
      ▼
RAG retrieval  →  docs / logs / runbooks + citation check
      │
      ▼
LangGraph workflow
  classify → retrieve → analyze_logs → plan → generate
      │
      ▼
Eval gate (5 signals)
  correctness · citation coverage · hallucination risk · safety · latency
      │
      ├── all pass  →  SHIP
      ├── any fail  →  HOLD  →  human review queue
      └── critical  →  ESCALATE  →  AutoOps event + RCA
      │
      ▼
Prometheus  →  tokens · cost · latency · tool success · escalation rate
```

---

## Core Workflows

### 1. Eval gate enforcement

Every answer passes 5 signals before shipping. Citation coverage = 0% → HOLD. Safety signal triggered → ESCALATE. No bypasses.

```bash
make demo
# → 0 unsafe outputs · 9 ship · 10 hold · 6 escalate
```

### 2. Cost governance

Tracks token usage and projected spend per query and per session. Projected overage → HOLD decision with cost context attached.

```
projected_spend: $700  budget: $500  →  decision: HOLD
```

### 3. Retrieval drift detection

Tracks retrieval hit rate over time. Drift from 0.91 → 0.76 triggers a HOLD — the system detects degrading retrieval quality before it produces unsupported answers.

```
retrieval_hit_rate: 0.91 → 0.76  →  decision: HOLD
```

---

## Failure Scenarios Covered

| Failure | Signal | Decision |
|---|---|---|
| Zero citation coverage | Unsupported claim | **HOLD** |
| Safety signal triggered | Unsafe content | **ESCALATE** |
| Tool call failure | `tool_success_rate` drop | **ESCALATE** |
| Retrieval drift | Hit rate 0.91 → 0.76 | **HOLD** |
| Latency SLO breach | p95 > threshold | **HOLD** |
| Budget overrun | Projected spend > limit | **HOLD** |
| Retry storm ingested | AutoOps incident type | **ESCALATE** |

---

## Engineering Decisions

**Why a 5-signal gate instead of a single confidence score:** A single score obscures which signal failed. A model can hallucinate confidently. Citation coverage, safety, and latency are independent failure modes that require independent gates.

**Why LangGraph instead of a simple chain:** Each node in the workflow emits observable state. This makes the execution trace inspectable — you can see exactly which step produced a bad retrieval or a tool failure, not just that the answer was wrong.

**Why escalate to AutoOps instead of retrying:** Retry amplifies the same failure. Escalation with structured context (incident type, tool status, gate decision) enables RCA. The system learns from failures instead of hiding them.

---

## What Is Intentionally Out of Scope

- 102 incidents are from controlled validation scenarios, not production customer incidents
- Mock model is default; real model requires a Gemini API key
- "MCP-style tools" is the tool-call pattern — not the full MCP protocol implementation
- Redis-backed async workflows are architectural proof, not production-scale deployment

---

## Resume Bullets

- Built an operational GenAI support platform with LangGraph orchestration, RAG retrieval, and a 5-signal eval gate (correctness, citation, hallucination, safety, latency) — 0 unsafe outputs across 25 validation runs
- Implemented cost governance and retrieval drift detection as first-class gate signals; caught projected budget overage ($700 vs $500) and retrieval quality degradation (0.91 → 0.76) before answers shipped
- Instrumented with per-query token tracking, escalation rate by issue type, and tool-call success rate; structured escalations emit AutoOps events for downstream RCA

---

## Interview Walkthrough

*"AgentGrid models what production AI support tooling needs to do: not just generate answers, but validate them before they ship. Every answer goes through a 5-signal eval gate. If citation coverage is zero, it holds for human review — it doesn't ship with a caveat. I also added cost governance and retrieval drift detection as gate signals. In 25 validation runs I had 0 unsafe outputs, with 9 ships, 10 holds, and 6 escalations. The escalations emit structured AutoOps events so failures generate RCA, not just logs."*

---

## Run Locally

```bash
git clone https://github.com/kritibehl/agentgrid-demo && cd agentgrid-demo
pip install -r requirements.txt
make demo    # 25 validation cases
make test    # 54 tests · 0 unsafe outputs
make report  # batch summary
```

---

## Repository Map

```
agentgrid-demo/
├── src/api/         FastAPI server
├── src/agent/       LangGraph workflow + eval gate
├── src/tools/       MCP-style tool implementations
├── src/rag/         Retrieval over docs/logs/runbooks
├── scripts/         Batch validation + real model runners
├── reports/         Gate decision outputs
├── screenshots/     Dashboard · trace · eval gate · tools
└── docs/            Architecture + case study
```
