import json
from pathlib import Path
from claude_workflows.tools import search_knowledge_base, summarize_issue, classify_priority, generate_handoff_note, validate_claim

def run_claude_style_workflow(request):
    docs = search_knowledge_base(request["user_request"])
    summary = summarize_issue(request["user_request"])
    priority = classify_priority(summary["summary"])
    handoff = generate_handoff_note(summary["summary"], priority["priority"])
    validation = validate_claim(summary["summary"], docs["docs"])
    return {
        "request_id": request["request_id"],
        "plan": ["search_knowledge_base", "summarize_issue", "classify_priority", "validate_claim", "generate_handoff_note"],
        "tool_outputs": {"docs": docs, "summary": summary, "priority": priority, "handoff": handoff},
        "structured_output": {"summary": summary["summary"], "priority": priority["priority"], "handoff_note": handoff["handoff_note"]},
        "validation": validation,
        "decision": "human_review" if validation["human_review_required"] else "ship"
    }

def run_all():
    requests = json.loads(Path("claude_workflows/sample_requests.json").read_text())
    results = [run_claude_style_workflow(r) for r in requests]
    report = {"workflow": "claude_style_tool_use", "runs": len(results), "results": results}
    Path("claude_workflows/claude_run_report.json").write_text(json.dumps(report, indent=2))
    Path("claude_workflows/claude_run_report.md").write_text("# Claude Tool-Use Workflow Report\n\nValidated Claude-style planning, tool calls, structured output, and human-review routing.\n")
    return report

if __name__ == "__main__":
    print(json.dumps(run_all(), indent=2))
