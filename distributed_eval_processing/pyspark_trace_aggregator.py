import json
from collections import Counter, defaultdict
from pathlib import Path


INPUT = "distributed_eval_processing/sample_agent_events.jsonl"
OUTPUT = "distributed_eval_processing/spark_metrics_output.json"


def pure_python_aggregate(path=INPUT):
    rows = [
        json.loads(line)
        for line in Path(path).read_text().splitlines()
        if line.strip()
    ]

    total = len(rows)
    decisions = Counter(row["decision"] for row in rows)

    by_model = defaultdict(list)
    for row in rows:
        by_model[row["model_version"]].append(row)

    model_metrics = {}
    for model, items in by_model.items():
        model_metrics[model] = {
            "count": len(items),
            "retrieval_hit_rate": round(sum(item["retrieval_hit"] for item in items) / len(items), 2),
            "tool_success_rate": round(sum(item["tool_success"] for item in items) / len(items), 2),
            "avg_latency_ms": round(sum(item["latency_ms"] for item in items) / len(items), 2),
            "avg_eval_score": round(sum(item["eval_score"] for item in items) / len(items), 2),
        }

    result = {
        "engine": "python_fallback",
        "total_events": total,
        "retrieval_hit_rate": round(sum(row["retrieval_hit"] for row in rows) / total, 2),
        "tool_success_rate": round(sum(row["tool_success"] for row in rows) / total, 2),
        "decision_counts": dict(decisions),
        "model_metrics": model_metrics,
    }

    Path(OUTPUT).write_text(json.dumps(result, indent=2))
    return result


def pyspark_aggregate(path=INPUT):
    try:
        from pyspark.sql import SparkSession
        from pyspark.sql import functions as F
    except Exception:
        return pure_python_aggregate(path)

    spark = (
        SparkSession.builder
        .appName("AgentGridTraceAggregator")
        .master("local[*]")
        .getOrCreate()
    )

    df = spark.read.json(path)
    total = df.count()

    summary_row = df.agg(
        F.avg(F.col("retrieval_hit").cast("double")).alias("retrieval_hit_rate"),
        F.avg(F.col("tool_success").cast("double")).alias("tool_success_rate")
    ).collect()[0]

    decision_counts = {
        row["decision"]: row["count"]
        for row in df.groupBy("decision").count().collect()
    }

    model_metrics = {}
    for row in df.groupBy("model_version").agg(
        F.count("*").alias("count"),
        F.avg(F.col("retrieval_hit").cast("double")).alias("retrieval_hit_rate"),
        F.avg(F.col("tool_success").cast("double")).alias("tool_success_rate"),
        F.avg("latency_ms").alias("avg_latency_ms"),
        F.avg("eval_score").alias("avg_eval_score"),
    ).collect():
        model_metrics[row["model_version"]] = {
            "count": row["count"],
            "retrieval_hit_rate": round(row["retrieval_hit_rate"], 2),
            "tool_success_rate": round(row["tool_success_rate"], 2),
            "avg_latency_ms": round(row["avg_latency_ms"], 2),
            "avg_eval_score": round(row["avg_eval_score"], 2),
        }

    result = {
        "engine": "pyspark",
        "total_events": total,
        "retrieval_hit_rate": round(summary_row["retrieval_hit_rate"], 2),
        "tool_success_rate": round(summary_row["tool_success_rate"], 2),
        "decision_counts": decision_counts,
        "model_metrics": model_metrics,
    }

    Path(OUTPUT).write_text(json.dumps(result, indent=2))
    spark.stop()
    return result


if __name__ == "__main__":
    print(json.dumps(pyspark_aggregate(), indent=2))
