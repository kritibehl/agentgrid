from rag_analytics_agent import run_analytics

if __name__ == "__main__":
    result = run_analytics()

    print("AgentGrid Analytics Demo")
    print("-----------------------")
    for k, v in result.items():
        print(f"{k}: {v}")
