import json
import hashlib
from pathlib import Path


def fake_embedding(text: str) -> list[float]:
    digest = hashlib.sha256(text.encode()).hexdigest()
    return [round(int(digest[i:i+4], 16) / 65535, 4) for i in range(0, 24, 4)]


def build_embeddings() -> list[dict]:
    chunks = json.loads(Path("vector_indexing/document_chunks.json").read_text())
    embeddings = []

    for chunk in chunks:
        embeddings.append({
            "chunk_id": chunk["chunk_id"],
            "doc_id": chunk["doc_id"],
            "embedding": fake_embedding(chunk["text"]),
            "embedding_version": "fake_hash_embedding_v1",
            "stale": False
        })

    Path("vector_indexing/vector_index.json").write_text(json.dumps(embeddings, indent=2))
    return embeddings


if __name__ == "__main__":
    print(json.dumps(build_embeddings(), indent=2))
