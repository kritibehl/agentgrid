# MCP Gateway Tool Health Report

## Summary

| Metric | Value |
|---|---:|
| tool_count | 3 |
| healthy_tools | 3 |
| avg_latency_ms | 121.0 |
| gateway_status | healthy |

## Tool Health

| Tool | Latency ms | Status |
|---|---:|---|
| fleet_query | 120 | healthy |
| workflow_trigger | 145 | healthy |
| incident_lookup | 98 | healthy |

## Example MCP Call

```json
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
}
```

## Scope

This is an MCP-style gateway proof for AI agents and workflow automation. It does not claim production Tesla integrations or real fleet data access.
