import json
from pathlib import Path

from cost_governance.spend_tracker import calculate_spend


def run_budget_gate() -> dict:
    spend = calculate_spend()

    decision = "ship"
    if spend["status"] == "budget_risk":
        decision = "hold"
    elif spend["status"] == "over_budget":
        decision = "block"

    result = {
        "gate": "ai_cost_governance",
        "decision": decision,
        "monthly_budget": spend["monthly_budget"],
        "projected_spend": spend["projected_spend"],
        "status": spend["status"],
        "recommended_action": spend["recommended_action"]
    }

    Path("cost_governance/release_budget_gate_report.json").write_text(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    print(json.dumps(run_budget_gate(), indent=2))
