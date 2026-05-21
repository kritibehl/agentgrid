from mcp_server.server import call_tool
def tool_agent(issue_type: str, logs: list[str]) -> dict:
    return {'agent':'tool_agent','log_analysis':call_tool('analyze_logs',logs=logs),'action_plan':call_tool('create_action_plan',issue_type=issue_type)}
