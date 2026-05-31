import json
from pathlib import Path


LOWER_IS_BETTER = {"p95_latency_ms", "unsupported_answer_rate"}


def metric_status(metric: str, baseline: float, current: float) -> dict:
    drift = round(current - baseline, 4)

    if metric in LOWER_IS_BETTER:
        regression = current > baseline * 1.10
    else:
        regression = current < baseline * 0.90

    return {
        "baseline": baseline,
        "current": current,
        "drift": drift,
        "status": "regression" if regression else "stable"
    }


def detect_drift(
    baseline_path="evaluation_drift/baseline_metrics.json",
    current_path="evaluation_drift/current_metrics.json"
) -> dict:
    baseline = json.loads(Path(baseline_path).read_text())
    current = json.loads(Path(current_path).read_text())

    metrics = {}
    for key, baseline_value in baseline.items():
        if key == "period":
            continue
        metrics[key] = metric_status(key, baseline_value, current[key])

    regressions = [
        name for name, data in metrics.items()
        if data["status"] == "regression"
    ]

    decision = "hold" if regressions else "ship"

    report = {
        "baseline_period": baseline["period"],
        "current_period": current["period"],
        "metrics": metrics,
        "regressions": regressions,
        "decision": decision,
        "reason": "quality_regression_detected" if regressions else "no_regression"
    }

    Path("evaluation_drift/drift_report.json").write_text(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    print(json.dumps(detect_drift(), indent=2))
