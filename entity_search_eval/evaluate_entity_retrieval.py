import json
from pathlib import Path


PLACES_PATH = Path("entity_search_eval/sample_places.jsonl")
QUERIES_PATH = Path("entity_search_eval/search_queries.jsonl")
REPORT_JSON = Path("entity_search_eval/entity_quality_report.json")
REPORT_MD = Path("entity_search_eval/entity_quality_report.md")


def load_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def lexical_score(query, place):
    haystack = " ".join([
        place["name"],
        place["category"],
        place["city"],
        " ".join(str(v) for v in place.get("attributes", {}).values()),
    ]).lower()

    terms = query.lower().replace("now", "").split()
    return sum(1 for term in terms if term in haystack)


def search_places(query, places, top_k=3):
    ranked = sorted(
        places,
        key=lambda place: (
            lexical_score(query, place),
            place.get("attributes", {}).get("rating", 0)
        ),
        reverse=True
    )
    return [place for place in ranked[:top_k] if lexical_score(query, place) > 0]


def normalized_name(name):
    return name.lower().replace("'", "").replace(" ", "")


def duplicate_entity_rate(results):
    seen = set()
    duplicates = 0

    for place in results:
        key = (normalized_name(place["name"]), place["city"], place["category"])
        fuzzy_key = (place["category"], place["city"])

        if key in seen or fuzzy_key in seen:
            duplicates += 1

        seen.add(key)
        seen.add(fuzzy_key)

    return duplicates / len(results) if results else 0


def missing_attribute_rate(results, required_attributes):
    if not results:
        return 1.0

    total_required = len(results) * len(required_attributes)
    missing = 0

    for place in results:
        attributes = place.get("attributes", {})
        for attr in required_attributes:
            if attr not in attributes:
                missing += 1

    return missing / total_required if total_required else 0


def evaluate():
    places = load_jsonl(PLACES_PATH)
    queries = load_jsonl(QUERIES_PATH)

    per_query = []
    total_hits = 0
    total_expected = 0
    exact_first_matches = 0
    grounded_passes = 0

    duplicate_rates = []
    missing_rates = []
    ranking_scores = []

    for query in queries:
        results = search_places(query["query"], places)
        result_ids = [place["entity_id"] for place in results]
        expected_ids = query["expected_entity_ids"]

        hits = len(set(result_ids) & set(expected_ids))
        total_hits += hits
        total_expected += len(expected_ids)

        first_match = bool(result_ids and result_ids[0] == expected_ids[0])
        exact_first_matches += int(first_match)

        duplicate_rate = duplicate_entity_rate(results)
        missing_rate = missing_attribute_rate(results, query["required_attributes"])

        ranking_quality = 1.0 if first_match else 0.5 if hits else 0.0
        grounded_answer_pass = hits > 0 and missing_rate < 0.35

        grounded_passes += int(grounded_answer_pass)
        duplicate_rates.append(duplicate_rate)
        missing_rates.append(missing_rate)
        ranking_scores.append(ranking_quality)

        per_query.append({
            "query_id": query["query_id"],
            "query": query["query"],
            "expected_entity_ids": expected_ids,
            "result_entity_ids": result_ids,
            "hit_count": hits,
            "first_result_match": first_match,
            "duplicate_entity_rate": round(duplicate_rate, 2),
            "missing_attribute_rate": round(missing_rate, 2),
            "ranking_quality": ranking_quality,
            "grounded_answer_pass": grounded_answer_pass
        })

    query_count = len(queries)
    report = {
        "query_count": query_count,
        "retrieval_hit_rate": round(total_hits / total_expected, 2),
        "entity_match_accuracy": round(exact_first_matches / query_count, 2),
        "duplicate_entity_rate": round(sum(duplicate_rates) / query_count, 2),
        "missing_attribute_rate": round(sum(missing_rates) / query_count, 2),
        "ranking_quality": round(sum(ranking_scores) / query_count, 2),
        "grounded_answer_pass_rate": round(grounded_passes / query_count, 2),
        "release_decision": "ship" if grounded_passes == query_count else "hold",
        "per_query": per_query
    }

    REPORT_JSON.write_text(json.dumps(report, indent=2))
    REPORT_MD.write_text(build_markdown(report))
    return report


def build_markdown(report):
    rows = "\n".join(
        f"| {item['query_id']} | {item['hit_count']} | {item['first_result_match']} | "
        f"{item['duplicate_entity_rate']} | {item['missing_attribute_rate']} | "
        f"{item['ranking_quality']} | {item['grounded_answer_pass']} |"
        for item in report["per_query"]
    )

    return f"""# Entity Search Evaluation Report

## Summary

| Metric | Value |
|---|---:|
| query_count | {report['query_count']} |
| retrieval_hit_rate | {report['retrieval_hit_rate']} |
| entity_match_accuracy | {report['entity_match_accuracy']} |
| duplicate_entity_rate | {report['duplicate_entity_rate']} |
| missing_attribute_rate | {report['missing_attribute_rate']} |
| ranking_quality | {report['ranking_quality']} |
| grounded_answer_pass_rate | {report['grounded_answer_pass_rate']} |
| release_decision | {report['release_decision']} |

## Per-Query Results

| Query | Hits | First Match | Duplicate Rate | Missing Attr Rate | Ranking Quality | Grounded Pass |
|---|---:|---|---:|---:|---:|---|
{rows}

## What This Evaluates

This pack measures whether an entity-search workflow retrieves the right places, ranks the best match first, avoids duplicate entities, returns required attributes, and produces grounded answers.

## Scope

This is a deterministic entity-search evaluation pack. It does not claim production Places, Maps, or retail search infrastructure.
"""


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
