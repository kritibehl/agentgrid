import json
import statistics
from pathlib import Path

ROOT = Path(__file__).parent
CORPUS = ROOT / "corpus" / "adversarial_v1.json"
REPORT_JSON = ROOT / "reports" / "baseline_vs_agentgrid.json"
REPORT_MD = ROOT / "reports" / "baseline_vs_agentgrid.md"

RETRIEVAL_FAILURES = {
    "retrieval_miss",
    "irrelevant_context",
    "contradictory_context",
    "stale_context",
    "poisoned_context",
}

TOOL_FAILURES = {
    "tool_timeout",
    "malformed_tool_result",
    "tool_exception",
    "repeated_tool_failure",
    "partial_service_failure",
}


def baseline_agent(case):
    return {
        "route": "SHIP",
        "recovered": False,
        "reason": "ungated_return",
        "latency_ms": case.get("latency_ms", 600),
        "tokens": 700,
        "estimated_cost_usd": 0.0028,
    }


def agentgrid_agent(case):
    retrieval = case["retrieval"]
    tool = case["tool"]
    model = case["model"]

    route = "SHIP"
    reason = "validated"
    recovered = False

    if retrieval.get("status") == "miss":
        route, reason = "HOLD", "retrieval_miss"

    elif retrieval.get("relevance", 1.0) < 0.50:
        route, reason = "HOLD", "irrelevant_context"

    elif retrieval.get("contradiction"):
        route, reason = "ESCALATE", "contradictory_context"

    elif retrieval.get("stale"):
        route, reason = "HOLD", "stale_context"

    elif retrieval.get("poisoned"):
        route, reason = "HOLD", "poisoned_context"

    elif tool.get("status") == "timeout":
        if tool.get("retryable") and tool.get("retry_result") == "success":
            route = "SHIP"
            reason = "recovered_after_retry"
            recovered = True
        else:
            route, reason = "ESCALATE", "tool_timeout"

    elif tool.get("status") == "malformed":
        route, reason = "HOLD", "malformed_tool_result"

    elif tool.get("status") in {"exception", "failed", "partial_failure"}:
        route, reason = "ESCALATE", tool["status"]

    elif not model.get("schema_valid", True):
        route, reason = "HOLD", "schema_failure"

    elif not model.get("supported", False):
        route, reason = "HOLD", "unsupported_claim"

    elif case.get("latency_ms", 0) > case.get(
        "latency_budget_ms",
        float("inf"),
    ):
        route, reason = "HOLD", "latency_budget"

    gate_overhead_ms = 90
    retry_overhead_ms = 240 if recovered else 0

    return {
        "route": route,
        "recovered": recovered,
        "reason": reason,
        "latency_ms": (
            case.get("latency_ms", 600)
            + gate_overhead_ms
            + retry_overhead_ms
        ),
        "tokens": 820,
        "estimated_cost_usd": 0.0033,
    }


def percentile(values, pct):
    values = sorted(values)
    index = round((pct / 100) * (len(values) - 1))
    return values[index]


def evaluate(cases, outputs):
    tp = fp = fn = tn = 0
    uncontained_failures = 0
    unsupported_outputs_shipped = 0
    retrieval_caught = 0
    tools_handled = 0
    grounding_caught = 0
    recoveries = 0
    route_matches = 0

    for case, output in zip(cases, outputs):
        expected = case["expected_intervention"]
        intervened = output["route"] != "SHIP" or output["recovered"]

        if expected and intervened:
            tp += 1
        elif not expected and intervened:
            fp += 1
        elif expected and not intervened:
            fn += 1
        else:
            tn += 1

        if expected and output["route"] == "SHIP" and not output["recovered"]:
            uncontained_failures += 1

        if (
            case["failure_type"] in RETRIEVAL_FAILURES
            and output["route"] != "SHIP"
        ):
            retrieval_caught += 1

        if (
            case["failure_type"] in TOOL_FAILURES
            and (output["route"] != "SHIP" or output["recovered"])
        ):
            tools_handled += 1

        if (
            not case["model"].get("supported", False)
            and output["route"] != "SHIP"
        ):
            grounding_caught += 1

        if (
            not case["model"].get("supported", False)
            and output["route"] == "SHIP"
            and not output["recovered"]
        ):
            unsupported_outputs_shipped += 1

        if output["recovered"]:
            recoveries += 1

        if output["route"] == case["expected_terminal_route"]:
            route_matches += 1

    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    fpr = fp / (fp + tn) if fp + tn else 0
    fnr = fn / (fn + tp) if fn + tp else 0

    return {
        "cases": len(cases),
        "uncontained_injected_failures": uncontained_failures,
        "unsupported_outputs_shipped": unsupported_outputs_shipped,
        "retrieval_failures_caught": retrieval_caught,
        "tool_failures_safely_handled": tools_handled,
        "grounding_failures_caught": grounding_caught,
        "successful_transient_recoveries": recoveries,
        "gate_precision": round(precision, 4),
        "gate_recall": round(recall, 4),
        "false_escalation_rate": round(fpr, 4),
        "false_negative_rate": round(fnr, 4),
        "route_accuracy": round(route_matches / len(cases), 4),
        "p50_latency_ms": statistics.median(
            x["latency_ms"] for x in outputs
        ),
        "p95_latency_ms": percentile(
            [x["latency_ms"] for x in outputs],
            95,
        ),
        "avg_tokens": round(
            statistics.mean(x["tokens"] for x in outputs),
            2,
        ),
        "avg_estimated_cost_usd": round(
            statistics.mean(x["estimated_cost_usd"] for x in outputs),
            6,
        ),
    }


def main():
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)

    cases = json.loads(CORPUS.read_text())

    baseline_outputs = [baseline_agent(c) for c in cases]
    agentgrid_outputs = [agentgrid_agent(c) for c in cases]

    baseline = evaluate(cases, baseline_outputs)
    agentgrid = evaluate(cases, agentgrid_outputs)

    report = {
        "suite": "adversarial-v1",
        "scope": {
            "failure_results": "deterministic fault-injection benchmark",
            "latency": "modeled",
            "tokens": "modeled",
            "cost": "modeled; not provider billing data"
        },
        "baseline": baseline,
        "agentgrid": agentgrid,
        "tradeoffs": {
            "failure_escapes_prevented":
                baseline["uncontained_injected_failures"]
                - agentgrid["uncontained_injected_failures"],
            "p95_gate_overhead_ms":
                agentgrid["p95_latency_ms"]
                - baseline["p95_latency_ms"],
            "avg_token_overhead":
                agentgrid["avg_tokens"]
                - baseline["avg_tokens"],
            "avg_cost_overhead_usd": round(
                agentgrid["avg_estimated_cost_usd"]
                - baseline["avg_estimated_cost_usd"],
                6,
            ),
        }
    }

    REPORT_JSON.write_text(json.dumps(report, indent=2))

    REPORT_MD.write_text(
        "# AgentGrid Reliability Benchmark\n\n"
        "## Thesis\n\n"
        "Benchmark an ungated agent against AgentGrid under the same "
        "adversarial failure corpus.\n\n"
        "## Results\n\n"
        "| Metric | Baseline | AgentGrid |\n"
        "|---|---:|---:|\n"
        f"| Uncontained injected failures | {baseline['uncontained_injected_failures']} | "
        f"{agentgrid['uncontained_injected_failures']} |\n"
        f"| Unsupported outputs shipped | {baseline['unsupported_outputs_shipped']} | "
        f"{agentgrid['unsupported_outputs_shipped']} |\n"
        f"| Retrieval failures caught | {baseline['retrieval_failures_caught']} | "
        f"{agentgrid['retrieval_failures_caught']} |\n"
        f"| Tool failures safely handled | {baseline['tool_failures_safely_handled']} | "
        f"{agentgrid['tool_failures_safely_handled']} |\n"
        f"| Grounding failures caught | {baseline['grounding_failures_caught']} | "
        f"{agentgrid['grounding_failures_caught']} |\n"
        f"| Successful transient recoveries | "
        f"{baseline['successful_transient_recoveries']} | "
        f"{agentgrid['successful_transient_recoveries']} |\n"
        f"| Gate precision | {baseline['gate_precision']:.2%} | "
        f"{agentgrid['gate_precision']:.2%} |\n"
        f"| Gate recall | {baseline['gate_recall']:.2%} | "
        f"{agentgrid['gate_recall']:.2%} |\n"
        f"| False escalation rate | "
        f"{baseline['false_escalation_rate']:.2%} | "
        f"{agentgrid['false_escalation_rate']:.2%} |\n"
        f"| Route accuracy | {baseline['route_accuracy']:.2%} | "
        f"{agentgrid['route_accuracy']:.2%} |\n"
        f"| p95 latency | {baseline['p95_latency_ms']} ms | "
        f"{agentgrid['p95_latency_ms']} ms |\n"
        f"| Avg modeled tokens | {baseline['avg_tokens']} | "
        f"{agentgrid['avg_tokens']} |\n"
        f"| Avg modeled cost | ${baseline['avg_estimated_cost_usd']} | "
        f"${agentgrid['avg_estimated_cost_usd']} |\n\n"
        "## Scope\n\n"
        "Failure-containment results are deterministic local benchmark "
        "results. Latency, token, and cost values are modeled and are "
        "not live-provider measurements.\n"
    )

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
