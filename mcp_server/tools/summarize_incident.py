def summarize_incident(findings: list[str], metrics: dict, actions: list[str]) -> dict:
    return {'tool':'summarize_incident','summary':'Grounded incident summary from tool findings and metrics','findings':findings,'metrics':metrics,'recommended_actions':actions,'root_cause_framing':'hypothesis'}
