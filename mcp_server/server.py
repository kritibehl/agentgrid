import json
from mcp_server.tools.search_docs import search_docs
from mcp_server.tools.analyze_logs import analyze_logs
from mcp_server.tools.create_action_plan import create_action_plan
from mcp_server.tools.query_metrics import query_metrics
from mcp_server.tools.summarize_incident import summarize_incident
TOOLS={'search_docs':search_docs,'analyze_logs':analyze_logs,'create_action_plan':create_action_plan,'query_metrics':query_metrics,'summarize_incident':summarize_incident}
def list_tools(): return {'tools':sorted(TOOLS.keys())}
def call_tool(name: str, **kwargs): return TOOLS[name](**kwargs) if name in TOOLS else {'error':'tool_not_found','tool':name}
if __name__=='__main__': print(json.dumps(list_tools(),indent=2))
