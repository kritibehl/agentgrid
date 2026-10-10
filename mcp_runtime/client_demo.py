import json
import anyio

from mcp import Client
from mcp_runtime.server import mcp


async def main():
    async with Client(mcp) as client:
        tools = await client.list_tools()

        print("protocol:", client.protocol_version)
        print(
            "tools:",
            [tool.name for tool in tools.tools],
        )

        result = await client.call_tool(
            "search_docs",
            {
                "query": "deployment latency failure"
            },
        )

        print("search_docs error:", result.is_error)

        print(
            "search_docs response:",
            json.dumps(
                result.model_dump(mode="json"),
                indent=2,
            ),
        )


if __name__ == "__main__":
    anyio.run(main)
