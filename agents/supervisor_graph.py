from agents.triage_agent import triage_agent
from agents.retrieval_agent import retrieval_agent
from agents.tool_agent import tool_agent
from agents.eval_agent import eval_agent
from agents.escalation_agent import escalation_agent
def run_supervisor_graph(user_issue: str) -> dict:
    logs=['ERROR db connection timeout','retry attempt 1','p95 latency exceeded threshold']
    triage=triage_agent(user_issue); retrieval=retrieval_agent(user_issue); tools=tool_agent(triage['issue_type'],logs)
    evaluation=eval_agent(retrieval['retrieval']['hit_count'],tools['log_analysis']['findings']); escalation=escalation_agent(evaluation['decision'],evaluation['reason'])
    return {'user_issue':user_issue,'workflow':[triage,retrieval,tools,evaluation,escalation],'final_decision':evaluation['decision'],'escalation_target':escalation['target']}
if __name__=='__main__':
    import json; print(json.dumps(run_supervisor_graph('Deployment timeout caused retry storm'),indent=2))
