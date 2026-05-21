def search_docs(query: str) -> dict:
    docs=['DB timeout runbook: check DB health and connection pool saturation','Deployment failure doc: retries and latency indicate dependency saturation']
    hits=[d for d in docs if any(t in d.lower() for t in query.lower().split())]
    return {'tool':'search_docs','query':query,'hits':hits,'hit_count':len(hits)}
