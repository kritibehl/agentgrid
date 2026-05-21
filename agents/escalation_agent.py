def escalation_agent(decision: str, reason: str) -> dict:
    target='none' if decision=='ship' else 'support_reviewer' if decision=='hold' else 'engineering_review'
    return {'agent':'escalation_agent','target':target,'reason':reason}
