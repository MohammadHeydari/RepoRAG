# graph_search.py
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np

GRAPH_PATH = "./graph.pkl"

model = SentenceTransformer("all-MiniLM-L6-v2")

with open(GRAPH_PATH, "rb") as f:
    G = pickle.load(f)


def get_seed_nodes(query, top_k=3):
    """Return top_k nodes most similar to query (semantic)"""
    node_texts = [G.nodes[n]["text"] for n in G.nodes]

    query_vec = model.encode([query])[0]
    text_vecs = model.encode(node_texts)

    # cosine similarity via normalized vectors
    text_vecs = text_vecs / np.linalg.norm(text_vecs, axis=1, keepdims=True)
    query_vec = query_vec / np.linalg.norm(query_vec)

    scores = np.dot(text_vecs, query_vec)

    top_idx = np.argsort(scores)[-top_k:][::-1]
    return list(top_idx)


def expand_graph(seed_nodes, depth=1):
    """Breadth-first expansion from seed nodes"""
    visited = set(seed_nodes)
    frontier = set(seed_nodes)

    for _ in range(depth):
        new_frontier = set()
        for node in frontier:
            neighbors = G.neighbors(node)
            for nb in neighbors:
                if nb not in visited:
                    visited.add(nb)
                    new_frontier.add(nb)
        frontier = new_frontier

    return list(visited)


def search_graph(query, k=5):
    """Return top-k results from graph with dedup and scoring"""
    seeds = get_seed_nodes(query)
    expanded = expand_graph(seeds, depth=2)  # depth can be tuned

    scored = []

    for n in expanded:
        node = G.nodes[n]
        # simple scoring: #entities + node degree
        score = len(node.get("entities", [])) + G.degree(n)
        scored.append((score, node))

    scored.sort(key=lambda x: x[0], reverse=True)

    # dedup based on file source
    seen_sources = set()
    results = []
    for score, node in scored:
        src = node["metadata"].get("source")
        if src in seen_sources:
            continue
        seen_sources.add(src)
        results.append({
            "text": node["text"],
            "metadata": node["metadata"],
            "entities": node.get("entities", []),
            "score": score
        })
        if len(results) >= k:
            break

    return results


if __name__ == "__main__":
    query = "Kafka producer"
    results = search_graph(query, k=5)
    for r in results:
        print(f"Score: {r['score']} | File: {r['metadata']['source']}")
        print(r["text"][:300], "\n")