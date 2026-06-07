import json
from pathlib import Path


def build_cost_governance_center():
    report = {
        "monthly_cost": 700.0,
        "monthly_budget": 500.0,
        "budget_consumed_pct": 140.0,
        "waste": {
            "duplicate_eval_runs_usd": 82.0,
            "low_value_experiments_usd": 64.0,
            "failed_tool_retry_cost_usd": 18.0,
            "total_estimated_waste_usd": 164.0
        },
        "optimization": [
            "hold noncritical experiments",
            "cache repeated retrieval evaluations",
            "reduce failed tool retries",
            "route low-confidence runs to batch evaluation"
        ],
        "status": "budget_risk"
    }

    Path("ai_operations_center/cost_governance_center.json").write_text(
        json.dumps(report, indent=2)
    )
    return report


if __name__ == "__main__":
    print(json.dumps(build_cost_governance_center(), indent=2))
