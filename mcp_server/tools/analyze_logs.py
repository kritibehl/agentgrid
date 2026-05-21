def analyze_logs(logs: list[str]) -> dict:
    text=' '.join(logs).lower(); findings=[]
    if 'timeout' in text: findings.append('timeout_detected')
    if 'retry' in text: findings.append('retry_behavior_detected')
    if 'latency' in text: findings.append('latency_degradation_detected')
    return {'tool':'analyze_logs','findings':findings,'severity':'high' if len(findings)>=2 else 'medium'}
