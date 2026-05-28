from agent_failure_recovery.recovery_runner import run_recovery_cases


def test_agent_failure_recovery_blocks_unsafe_paths():
    report = run_recovery_cases()

    assert report["cases_evaluated"] == 4
    assert report["trace_preservation_rate"] == 1.0
    assert report["unsafe_outputs_blocked"] >= 2
    assert report["fallback_paths_verified"] == 1
