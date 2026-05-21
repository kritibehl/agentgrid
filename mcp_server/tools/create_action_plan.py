def create_action_plan(issue_type: str) -> dict:
    plans={'timeout':['Check dependency health','Inspect connection pool saturation','Reduce retry fanout'],'tool_failure':['Inspect tool logs','Collect trace_id','Route to engineering']}
    return {'tool':'create_action_plan','issue_type':issue_type,'actions':plans.get(issue_type,['Collect trace_id','Escalate for review'])}
