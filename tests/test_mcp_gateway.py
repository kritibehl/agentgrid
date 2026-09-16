import json
from pathlib import Path

from mcp_gateway.run_mcp_gateway_check import run_gateway_check


def test_mcp_gateway_health_report():
    report = run_gateway_check()

    assert report["tool_count"] == 3
    assert report["healthy_tools"] == 3
    assert report["status"] == "healthy"

    trace = json.loads(Path("mcp_gateway/mcp_call_trace.json").read_text())
    assert trace["calls"][0]["tool"] == "fleet_query"
    assert trace["calls"][0]["latency_ms"] == 120
    assert trace["calls"][0]["status"] == "healthy"
