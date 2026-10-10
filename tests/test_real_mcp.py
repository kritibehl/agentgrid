import json
import anyio

from mcp import Client
from mcp_runtime.server import mcp


def test_real_mcp_discovers_agentgrid_tools():
    async def run():
        async with Client(mcp) as client:
            result = await client.list_tools()

            names = {
                tool.name
                for tool in result.tools
            }

            assert {
                "search_docs",
                "analyze_logs",
                "query_metrics",
                "create_action_plan",
            }.issubset(names)

    anyio.run(run)


def test_real_mcp_executes_tool():
    async def run():
        async with Client(mcp) as client:
            result = await client.call_tool(
                "analyze_logs",
                {"service": "deployment-api"},
            )

            assert result.is_error is False
            assert result.content

            serialized = json.dumps(
                result.model_dump(mode="json")
            )

            assert "deployment-api" in serialized
            assert "elevated_latency" in serialized
            assert "medium" in serialized

    anyio.run(run)
