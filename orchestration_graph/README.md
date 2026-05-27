# AgentGrid Multi-Agent Orchestration Graph

## Purpose

This artifact models AgentGrid as a graph-based multi-agent workflow.

## Agents

- planner agent
- retriever agent
- evaluator agent
- escalation agent
- response synthesis agent

## Flow

```text
planner
→ retriever
→ evaluator
→ response synthesis
       ↘
        escalation
Why This Matters

Graph-based orchestration makes the agent workflow easier to inspect, debug, extend, and compare across retrieval/evaluation strategies.
