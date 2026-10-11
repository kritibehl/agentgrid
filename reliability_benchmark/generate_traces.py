import json
from pathlib import Path

from reliability_benchmark.benchmark import (
    CORPUS,
    agentgrid_agent,
)


OUT = Path(
    "reliability_benchmark/reports/traces"
)


def main():
    OUT.mkdir(
        parents=True,
        exist_ok=True,
    )

    cases = json.loads(
        CORPUS.read_text()
    )

    for number, case in enumerate(
        cases,
        start=1,
    ):
        result = agentgrid_agent(case)

        trace = {
            "trace_id": f"ag-{number:04d}",
            "scenario": case["id"],
            "failure_type": case["failure_type"],
            "workflow": [
                {
                    "span": "retrieval",
                    "status": case["retrieval"].get(
                        "status"
                    ),
                    "relevance": case[
                        "retrieval"
                    ].get("relevance"),
                    "contradiction": case[
                        "retrieval"
                    ].get(
                        "contradiction",
                        False,
                    ),
                    "stale": case[
                        "retrieval"
                    ].get(
                        "stale",
                        False,
                    ),
                    "poisoned": case[
                        "retrieval"
                    ].get(
                        "poisoned",
                        False,
                    ),
                },
                {
                    "span": "tool",
                    "status": case["tool"].get(
                        "status"
                    ),
                    "attempts": case[
                        "tool"
                    ].get("attempts"),
                    "retryable": case[
                        "tool"
                    ].get(
                        "retryable",
                        False,
                    ),
                },
                {
                    "span": "model",
                    "supported": case[
                        "model"
                    ].get("supported"),
                    "schema_valid": case[
                        "model"
                    ].get(
                        "schema_valid"
                    ),
                },
                {
                    "span": "evaluation",
                    "route": result["route"],
                    "reason": result["reason"],
                    "recovered": result[
                        "recovered"
                    ],
                },
            ],
            "telemetry": {
                "latency_ms": result[
                    "latency_ms"
                ],
                "modeled_tokens": result[
                    "tokens"
                ],
                "modeled_cost_usd": result[
                    "estimated_cost_usd"
                ],
            },
            "final_route": result["route"],
            "decision_reason": result["reason"],
        }

        path = OUT / (
            case["id"] + ".json"
        )

        path.write_text(
            json.dumps(
                trace,
                indent=2,
            )
        )

    print(
        f"generated {len(cases)} traces"
    )


if __name__ == "__main__":
    main()
