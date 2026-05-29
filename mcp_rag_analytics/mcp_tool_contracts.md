# MCP Tool Contracts for RAG Analytics

## search_docs

Input:
- query
- trace_id
- max_results

Output:
- chunks
- retrieval_hit_rate
- latency_ms

## query_metrics

Input:
- metric_name
- window

Output:
- value
- aggregation
- source

## summarize_findings

Input:
- retrieved_chunks
- metric_summary

Output:
- analytics_summary
- confidence
- escalation_needed
