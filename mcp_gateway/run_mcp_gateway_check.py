import json
from pathlib import Path


TOOLS = [
    {"tool": "fleet_query", "latency_ms": 120, "status": "healthy"},
    {"tool": "workflow_trigger", "latency_ms": 145, "status": "healthy"},
    {"tool": "incident_lookup", "latency_ms": 98, "status": "healthy"}
]


def run_gateway_check():
    report = {
        "gateway": "agentgrid_mcp_gateway",
        "tool_count": len(TOOLS),
        "healthy_tools": sum(1 for tool in TOOLS if tool["status"] == "healthy"),
        "avg_latency_ms": round(sum(tool["latency_ms"] for tool in TOOLS) / len(TOOLS), 2),
        "tools": TOOLS,
        "status": "healthy"
    }

    trace = {
        "trace_id": "mcp_trace_001",
        "calls": [
            {
                "tool": "fleet_query",
                "input": {
                    "fleet_id": "fleet_demo_001",
                    "metric": "availability"
                },
                "latency_ms": 120,
                "status": "healthy",
                "output": {
                    "value": 0.997,
                    "status": "nominal"
                }
            },
            {
                "tool": "workflow_trigger",
                "input": {
                    "workflow_id": "support_escalation_review",
                    "trace_id": "mcp_trace_001"
                },
                "latency_ms": 145,
                "status": "healthy",
                "output": {
                    "triggered": True,
                    "workflow_status": "queued"
                }
            }
        ]
    }

    Path("mcp_gateway/tool_health_report.json").write_text(json.dumps(report, indent=2))
    Path("mcp_gateway/mcp_call_trace.json").write_text(json.dumps(trace, indent=2))
    Path("mcp_gateway/tool_health_report.md").write_text(build_markdown(report, trace))
    return report


def build_markdown(report, trace):
    rows = "\n".join(
        f"| {tool['tool']} | {tool['latency_ms']} | {tool['status']} |"
        for tool in report["tools"]
    )

    return f"""# MCP Gateway Tool Health Report

## Summary

| Metric | Value |
|---|---:|
| tool_count | {report['tool_count']} |
| healthy_tools | {report['healthy_tools']} |
| avg_latency_ms | {report['avg_latency_ms']} |
| gateway_status | {report['status']} |

## Tool Health

| Tool | Latency ms | Status |
|---|---:|---|
{rows}

## Example MCP Call

```json
{json.dumps(trace['calls'][0], indent=2)}
Scope

This is an MCP-style gateway proof for AI agents and workflow automation. It does not claim production Tesla integrations or real fleet data access.
"""

if name == "main":
print(json.dumps(run_gateway_check(), indent=2))
