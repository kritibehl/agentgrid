import argparse
from reliability_benchmark.benchmark import main

parser = argparse.ArgumentParser(prog="agentgrid")
sub = parser.add_subparsers(dest="command", required=True)

benchmark = sub.add_parser("benchmark")
benchmark.add_argument("--suite", default="adversarial-v1")

args = parser.parse_args()

if args.command == "benchmark":
    if args.suite != "adversarial-v1":
        raise SystemExit(f"unknown suite: {args.suite}")
    main()
