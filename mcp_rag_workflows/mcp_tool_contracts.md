# MCP-Style Tool Contracts

## search_docs

Input:
- query
- trace_id

Output:
- retrieved_chunks
- retrieval_hit_rate
- retrieval_latency_ms

## analyze_logs

Input:
- trace_id
- service_name

Output:
- findings
- severity
- probable_issue_family

## query_metrics

Input:
- metric_name
- time_window

Output:
- metric_value
- aggregation
- source

## summarize_incident

Input:
- retrieved_context
- findings

Output:
- incident_summary
- probable_cause_hypothesis
- escalation_recommendation
