from mcp_server.server import list_tools, call_tool
from agents.supervisor_graph import run_supervisor_graph

def test_mcp_server_exposes_core_tools():
    tools=list_tools()['tools']; assert 'search_docs' in tools; assert 'analyze_logs' in tools; assert 'query_metrics' in tools; assert 'create_action_plan' in tools

def test_mcp_tool_call_search_docs():
    result=call_tool('search_docs',query='db timeout'); assert result['tool']=='search_docs'; assert result['hit_count']>=1

def test_supervisor_graph_returns_decision():
    result=run_supervisor_graph('Deployment timeout caused retry storm'); assert result['final_decision'] in ('ship','hold','escalate'); assert len(result['workflow'])==5
