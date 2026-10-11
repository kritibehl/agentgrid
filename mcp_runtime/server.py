from mcp.server import MCPServer


mcp = MCPServer(
    "AgentGrid Reliability Tools",
    instructions=(
        "Operational tools used by AgentGrid "
        "for grounded support and reliability workflows."
    ),
)


@mcp.tool()
def search_docs(query: str) -> dict:
    """Search operational documentation."""
    return {
        "query": query,
        "documents": [
            {
                "id": "runbook-001",
                "title": (
                    "Deployment Reliability Runbook"
                ),
                "relevance": 0.94,
            }
        ],
        "hit_count": 1,
    }


@mcp.tool()
def analyze_logs(service: str) -> dict:
    """Analyze logs for operational signals."""
    return {
        "service": service,
        "signals": [
            "elevated_latency"
        ],
        "severity": "medium",
    }


@mcp.tool()
def query_metrics(service: str) -> dict:
    """Query operational service metrics."""
    return {
        "service": service,
        "p95_latency_ms": 820,
        "error_rate": 0.02,
    }


@mcp.tool()
def create_action_plan(
    issue: str,
    evidence: str,
) -> dict:
    """Create an evidence-backed action plan."""
    return {
        "issue": issue,
        "evidence": evidence,
        "action": (
            "validate evidence and route "
            "high-risk actions to human review"
        ),
    }
