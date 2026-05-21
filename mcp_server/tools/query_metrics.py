def query_metrics(service: str) -> dict:
    data={'checkout':{'p95_latency_ms':1800,'error_rate_pct':7.2,'retry_count':42}}
    return {'tool':'query_metrics','service':service,'metrics':data.get(service,{})}
