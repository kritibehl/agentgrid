# Entity Search Evaluation Report

## Summary

| Metric | Value |
|---|---:|
| query_count | 4 |
| retrieval_hit_rate | 1.0 |
| entity_match_accuracy | 1.0 |
| duplicate_entity_rate | 0.33 |
| missing_attribute_rate | 0.06 |
| ranking_quality | 1.0 |
| grounded_answer_pass_rate | 1.0 |
| release_decision | ship |

## Per-Query Results

| Query | Hits | First Match | Duplicate Rate | Missing Attr Rate | Ranking Quality | Grounded Pass |
|---|---:|---|---:|---:|---:|---|
| q_001 | 2 | True | 0.33 | 0.0 | 1.0 | True |
| q_002 | 1 | True | 0.33 | 0.0 | 1.0 | True |
| q_003 | 1 | True | 0.33 | 0.11 | 1.0 | True |
| q_004 | 1 | True | 0.33 | 0.11 | 1.0 | True |

## What This Evaluates

This pack measures whether an entity-search workflow retrieves the right places, ranks the best match first, avoids duplicate entities, returns required attributes, and produces grounded answers.

## Scope

This is a deterministic entity-search evaluation pack. It does not claim production Places, Maps, or retail search infrastructure.
