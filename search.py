# search.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

VECTOR_PATH = "./vector.index"
META_PATH = "./metadata.npy"

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index(VECTOR_PATH)
chunks = np.load(META_PATH, allow_pickle=True)


def search(query, k=5, file_type=None, source_contains=None):

    query_vec = model.encode([query]).astype("float32")
    faiss.normalize_L2(query_vec)

    scores, idxs = index.search(query_vec, k*3)  # چند نتیجه اضافه برای فیلتر بعدی
    results = []

    for score, i in zip(scores[0], idxs[0]):
        chunk = chunks[i]

        # metadata filtering
        if file_type and chunk.metadata.get("extension") != file_type:
            continue
        if source_contains and source_contains not in chunk.metadata.get("source", ""):
            continue

        results.append({
            "text": chunk.page_content,
            "metadata": chunk.metadata,
            "score": float(score)
        })

        if len(results) >= k:
            break

    return results

if __name__ == "__main__":
    q = "Kafka producer"
    res = search(q, k=5, file_type=".py")
    for r in res:
        print("---")
        print(f"Score: {r['score']}")
        print(f"File: {r['metadata']['source']}")
        print(r["text"][:300], "\n")