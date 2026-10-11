# AgentGrid Reliability Benchmark

## Thesis

Benchmark an ungated agent against AgentGrid under the same adversarial failure corpus.

## Results

| Metric | Baseline | AgentGrid |
|---|---:|---:|
| Uncontained injected failures | 13 | 0 |
| Unsupported outputs shipped | 10 | 0 |
| Retrieval failures caught | 0 | 5 |
| Tool failures safely handled | 0 | 5 |
| Grounding failures caught | 0 | 10 |
| Successful transient recoveries | 0 | 1 |
| Gate precision | 0.00% | 100.00% |
| Gate recall | 0.00% | 100.00% |
| False escalation rate | 0.00% | 0.00% |
| Route accuracy | 14.29% | 100.00% |
| p95 latency | 600 ms | 930 ms |
| Avg modeled tokens | 700 | 820 |
| Avg modeled cost | $0.0028 | $0.0033 |

## Scope

Failure-containment results are deterministic local benchmark results. Latency, token, and cost values are modeled and are not live-provider measurements.
