def eval_agent(retrieval_hit_count: int, tool_findings: list[str]) -> dict:
    if retrieval_hit_count==0: return {'agent':'eval_agent','decision':'hold','reason':'missing_retrieval_grounding'}
    if 'timeout_detected' in tool_findings or 'retry_behavior_detected' in tool_findings: return {'agent':'eval_agent','decision':'ship','reason':'grounded_operational_answer'}
    return {'agent':'eval_agent','decision':'hold','reason':'insufficient_evidence'}
