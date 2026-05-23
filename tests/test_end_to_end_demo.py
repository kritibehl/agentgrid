import json
from pathlib import Path
from demo_outputs.generate_end_to_end_demo import build_report


def test_end_to_end_demo_generates_operational_loop():
    report = build_report()

    assert report["agentgrid_detection"]["final_decision"] == "hold"
    assert report["agentgrid_detection"]["unsupported_answer"] is True
    assert report["autoops_classification"]["is_recurring"] is True
    assert report["rca_and_product_feedback"]["release_safety_outcome"] == "blocked_from_shipping"

    assert Path("demo_outputs/end_to_end_ai_support_incident.md").exists()
    assert Path("demo_outputs/end_to_end_ai_support_incident.json").exists()
