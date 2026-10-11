import json
from pathlib import Path

from reliability_benchmark.benchmark import (
    agentgrid_agent,
    baseline_agent,
)

CORPUS = Path(
    "reliability_benchmark/corpus/adversarial_v1.json"
)


def load_cases():
    return json.loads(CORPUS.read_text())


def test_adversarial_suite_contains_core_failure_classes():
    kinds = {
        case["failure_type"]
        for case in load_cases()
    }

    required = {
        "retrieval_miss",
        "irrelevant_context",
        "contradictory_context",
        "stale_context",
        "poisoned_context",
        "tool_timeout",
        "malformed_tool_result",
        "tool_exception",
        "repeated_tool_failure",
        "unsupported_claim",
        "schema_failure",
        "latency_budget",
        "partial_service_failure",
    }

    assert required.issubset(kinds)


def test_ungated_baseline_allows_failure_escapes():
    escapes = 0

    for case in load_cases():
        result = baseline_agent(case)

        if (
            case["expected_intervention"]
            and result["route"] == "SHIP"
            and not result["recovered"]
        ):
            escapes += 1

    assert escapes > 0


def test_agentgrid_contains_every_expected_failure():
    for case in load_cases():
        result = agentgrid_agent(case)

        if case["expected_intervention"]:
            assert (
                result["route"] != "SHIP"
                or result["recovered"]
            ), case["id"]


def test_unsupported_claim_never_ships():
    case = next(
        c for c in load_cases()
        if c["id"] == "unsupported_claim"
    )

    result = agentgrid_agent(case)

    assert result["route"] == "HOLD"
    assert result["reason"] == "unsupported_claim"


def test_missing_retrieval_never_ships():
    case = next(
        c for c in load_cases()
        if c["id"] == "missing_retrieval"
    )

    result = agentgrid_agent(case)

    assert result["route"] == "HOLD"


def test_poisoned_context_never_ships():
    case = next(
        c for c in load_cases()
        if c["id"] == "poisoned_context"
    )

    result = agentgrid_agent(case)

    assert result["route"] == "HOLD"


def test_required_tool_failure_never_becomes_successful_evidence():
    failure_types = {
        "malformed_tool_result",
        "tool_exception",
        "repeated_tool_failure",
        "partial_service_failure",
    }

    for case in load_cases():
        if case["failure_type"] in failure_types:
            result = agentgrid_agent(case)
            assert result["route"] != "SHIP"


def test_transient_tool_timeout_recovers():
    case = next(
        c for c in load_cases()
        if c["id"] == "transient_tool_timeout"
    )

    result = agentgrid_agent(case)

    assert result["recovered"] is True
    assert result["route"] == "SHIP"


def test_healthy_request_is_not_false_escalated():
    case = next(
        c for c in load_cases()
        if c["id"] == "healthy_request"
    )

    result = agentgrid_agent(case)

    assert result["route"] == "SHIP"
    assert result["recovered"] is False


def test_routes_match_declared_policy():
    for case in load_cases():
        result = agentgrid_agent(case)

        assert (
            result["route"]
            == case["expected_terminal_route"]
        ), case["id"]
