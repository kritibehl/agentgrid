import json
from pathlib import Path

files = [
    "benchmarks/results/gemini_flash_results.json",
    "benchmarks/results/gpt4o_mini_results.json",
    "benchmarks/results/claude_haiku_results.json",
]

summary = []

for path in files:
    data = json.loads(Path(path).read_text())

    runs = data["runs"]

    avg_groundedness = sum(r["groundedness_score"] for r in runs) / len(runs)
    avg_latency = sum(r["latency_ms"] for r in runs) / len(runs)
    avg_cost = sum(r["estimated_cost_usd"] for r in runs) / len(runs)
    avg_tool_quality = sum(r["tool_call_quality"] for r in runs) / len(runs)

    unsupported_count = sum(1 for r in runs if r["unsupported_answer"])

    summary.append({
        "model": data["model"],
        "avg_groundedness": round(avg_groundedness, 3),
        "avg_latency_ms": round(avg_latency, 2),
        "avg_cost_usd": round(avg_cost, 4),
        "avg_tool_call_quality": round(avg_tool_quality, 3),
        "unsupported_answer_count": unsupported_count,
    })

summary = sorted(summary, key=lambda x: x["avg_groundedness"], reverse=True)

print(json.dumps(summary, indent=2))
