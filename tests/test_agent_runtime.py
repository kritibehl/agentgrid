from agent_runtime.run_history import RUNS, record_run, list_runs, get_human_review_queue, compare_workflows


def setup_function():
    RUNS.clear()


def test_records_agent_run_history():
    run = record_run("Why did deployment fail?", "hold", 0.2, "success")

    assert run["final_decision"] == "hold"
    assert len(list_runs()) == 1


def test_human_review_queue_collects_hold_runs():
    record_run("Why did deployment fail?", "hold", 0.2, "success")
    record_run("Summarize healthy deployment", "ship", 1.0, "success")

    queue = get_human_review_queue()

    assert len(queue) == 1
    assert queue[0]["human_review_required"] is True


def test_workflow_comparison_exists():
    comparison = compare_workflows()

    assert "baseline_single_agent" in comparison
    assert "agentgrid_multi_agent" in comparison
