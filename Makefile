.PHONY: demo benchmark traces mcp test

demo:
	python3 -m reliability_benchmark.cli benchmark --suite adversarial-v1
	python3 -m reliability_benchmark.generate_traces
	python3 -m mcp_runtime.client_demo

benchmark:
	python3 -m reliability_benchmark.cli benchmark --suite adversarial-v1

traces:
	python3 -m reliability_benchmark.generate_traces

mcp:
	python3 -m mcp_runtime.client_demo

test:
	python3 -m pytest -q
