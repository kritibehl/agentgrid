from mcp_server.server import call_tool
def retrieval_agent(user_issue: str) -> dict:
    return {'agent':'retrieval_agent','retrieval':call_tool('search_docs',query=user_issue)}
