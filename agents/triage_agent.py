def triage_agent(user_issue: str) -> dict:
    t=user_issue.lower(); issue='timeout' if 'timeout' in t or 'latency' in t else 'tool_failure' if 'tool' in t else 'low_retrieval' if 'retrieval' in t or 'missing' in t else 'general'
    return {'agent':'triage_agent','issue_type':issue}
