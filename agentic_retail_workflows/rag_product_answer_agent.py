from agentic_retail_workflows.product_search_agent import search_products
from agentic_retail_workflows.recommendation_review_agent import review_recommendation
import json
from pathlib import Path


def generate_product_answer(query: str = "Find headphones for travel") -> dict:
    search_result = search_products(query)
    review = review_recommendation(search_result)

    answer = {
        "query": query,
        "answer": "The top retrieved option is noise-cancelling headphones, based on the product-search score.",
        "retrieval_quality": {
            "retrieval_hit_rate": search_result["retrieval_hit_rate"],
            "top_score": search_result["top_result"]["score"]
        },
        "review": review,
        "eval_gate": {
            "decision": "ship" if review["recommendation_safe"] else "hold",
            "reason": "recommendation_grounded" if review["recommendation_safe"] else "unsupported_recommendation_claim"
        }
    }

    Path("agentic_retail_workflows/retrieval_quality_report.json").write_text(
        json.dumps(answer["retrieval_quality"], indent=2)
    )
    Path("agentic_retail_workflows/eval_gate_report.json").write_text(
        json.dumps(answer["eval_gate"], indent=2)
    )
    return answer


if __name__ == "__main__":
    print(json.dumps(generate_product_answer(), indent=2))
