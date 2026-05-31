import json
from pathlib import Path


def calculate_spend(policy_path="cost_governance/budget_policy.json") -> dict:
    policy = json.loads(Path(policy_path).read_text())
    monthly_budget = policy["monthly_budget_usd"]

    provider_spend = []
    projected_spend = 0.0

    for provider in policy["providers"]:
        spend = provider["cost_per_run_usd"] * provider["monthly_runs"]
        projected_spend += spend
        provider_spend.append({
            **provider,
            "projected_monthly_cost": round(spend, 2)
        })

    budget_consumed_pct = round((projected_spend / monthly_budget) * 100, 1)

    if projected_spend > monthly_budget * 1.15:
        status = "budget_risk"
    elif projected_spend > monthly_budget:
        status = "watch"
    else:
        status = "safe"

    report = {
        "monthly_budget": monthly_budget,
        "projected_spend": round(projected_spend, 2),
        "budget_consumed_pct": budget_consumed_pct,
        "status": status,
        "recommended_action": policy["actions"].get(status, "review"),
        "provider_spend": provider_spend
    }

    Path("cost_governance/projected_cost_report.json").write_text(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    print(json.dumps(calculate_spend(), indent=2))
