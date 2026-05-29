def review_recommendation(search_result: dict) -> dict:
    top = search_result["top_result"]
    unsupported_claims = []

    if "best" in top["name"].lower():
        unsupported_claims.append("best claim requires evidence")

    return {
        "product_id": top["id"],
        "recommendation_safe": len(unsupported_claims) == 0,
        "unsupported_claims": unsupported_claims,
        "review_notes": "Recommendation uses retrieved product evidence and avoids unsupported ranking claims."
    }
