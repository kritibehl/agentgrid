from pathlib import Path

from entity_search_eval.evaluate_entity_retrieval import evaluate


def test_entity_search_eval_generates_quality_metrics():
    report = evaluate()

    assert report["query_count"] == 4
    assert "retrieval_hit_rate" in report
    assert "entity_match_accuracy" in report
    assert "duplicate_entity_rate" in report
    assert "missing_attribute_rate" in report
    assert "ranking_quality" in report
    assert "grounded_answer_pass_rate" in report
    assert Path("entity_search_eval/entity_quality_report.md").exists()
    assert Path("entity_search_eval/entity_quality_report.json").exists()
