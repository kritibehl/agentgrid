#!/usr/bin/env python3
import json
from pathlib import Path

result = {
    "incident_id": "inc_agent_timeout_001",
    "likely_root_cause": "tool timeout combined with retrieval miss",
    "evidence": ["tool_timeout", "retrieval_miss", "escalation_triggered"],
    "recommended_actions": [
        "Check tool latency, retry policy, and downstream service health.",
        "Inspect index freshness, query routing, and retrieval thresholds.",
        "Review guardrail decision and human-review handoff."
    ],
    "runbook_count": 3
}

Path("developer_copilot/copilot_rca_report.json").write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
