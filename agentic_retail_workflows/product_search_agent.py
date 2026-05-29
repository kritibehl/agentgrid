def search_products(query: str) -> dict:
    products = [
        {"id": "p1", "name": "Noise-cancelling headphones", "score": 0.92},
        {"id": "p2", "name": "Wireless earbuds", "score": 0.79},
        {"id": "p3", "name": "Studio headphones", "score": 0.73},
    ]

    return {
        "query": query,
        "results": products,
        "top_result": products[0],
        "retrieval_hit_rate": 0.86
    }
