from pathlib import Path
import json


DOCUMENTS = [
    {
        "doc_id": "runbook_db_timeout",
        "text": "DB timeout runbook. Check database health, connection pool saturation, retry fanout, and p95 latency."
    },
    {
        "doc_id": "runbook_retrieval_grounding",
        "text": "Missing retrieval grounding should hold the answer and route to a support reviewer."
    },
    {
        "doc_id": "runbook_eval_gate",
        "text": "Eval gates block unsupported answers, unsafe root-cause claims, and missing evidence."
    }
]


def chunk_text(text: str, size: int = 12) -> list[str]:
    words = text.split()
    return [" ".join(words[i:i + size]) for i in range(0, len(words), size)]


def build_chunks() -> list[dict]:
    chunks = []
    for doc in DOCUMENTS:
        for idx, chunk in enumerate(chunk_text(doc["text"])):
            chunks.append({
                "chunk_id": f"{doc['doc_id']}_chunk_{idx}",
                "doc_id": doc["doc_id"],
                "text": chunk,
                "version": "v1"
            })

    Path("vector_indexing/document_chunks.json").write_text(json.dumps(chunks, indent=2))
    return chunks


if __name__ == "__main__":
    print(json.dumps(build_chunks(), indent=2))
