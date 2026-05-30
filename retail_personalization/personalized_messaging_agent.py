import json
from pathlib import Path


def load_json(path: str):
    return json.loads(Path(path).read_text())


def generate_personalized_experiences():
    segments = load_json("retail_personalization/user_segment_examples.json")
    experiments = load_json("retail_personalization/recommendation_experiments.json")

    by_segment = {segment["segment_id"]: segment for segment in segments}
    outputs = []

    for experiment in experiments:
        segment = by_segment[experiment["segment_id"]]

        quality = experiment["quality_checks"]
        decision = (
            "ship"
            if quality["segment_match"]
            and not quality["unsupported_claim"]
            and quality["message_relevance"] >= 0.85
            else "hold"
        )

        outputs.append({
            "segment_id": segment["segment_id"],
            "signals": segment["signals"],
            "recommendation": experiment["recommendation"],
            "evidence": experiment["evidence"],
            "personalized_message": experiment["personalized_message"],
            "message_relevance": quality["message_relevance"],
            "eval_gate_decision": decision,
            "reason": "segment_aligned_personalization" if decision == "ship" else "requires_review"
        })

    report = {
        "workflow": "retail_personalization",
        "segments_evaluated": len(segments),
        "recommendations_evaluated": len(experiments),
        "ship_decisions": sum(1 for item in outputs if item["eval_gate_decision"] == "ship"),
        "hold_decisions": sum(1 for item in outputs if item["eval_gate_decision"] == "hold"),
        "avg_message_relevance": round(
            sum(item["message_relevance"] for item in outputs) / len(outputs),
            2
        ),
        "outputs": outputs
    }

    Path("retail_personalization/personalization_report.json").write_text(
        json.dumps(report, indent=2)
    )
    return report


if __name__ == "__main__":
    print(json.dumps(generate_personalized_experiences(), indent=2))
