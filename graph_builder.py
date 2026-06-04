# graph_builder.py
import os
import pickle
import networkx as nx
import spacy
from load import load_files
from chunker import chunk_texts

REPO_PATH = "./repo"
GRAPH_PATH = "./graph.pkl"

nlp = spacy.load("en_core_web_sm")


def extract_entities(text):
    doc = nlp(text)
    return list(set([ent.text for ent in doc.ents]))


def build_graph():
    print("Loading repo...")
    texts, metas = load_files(REPO_PATH)

    print("Chunking...")
    chunks = chunk_texts(texts, metas)

    G = nx.Graph()

    print("Building graph...")

    for i, chunk in enumerate(chunks):
        node_id = i

        entities = extract_entities(chunk.page_content)

        G.add_node(
            node_id,
            text=chunk.page_content,
            metadata=chunk.metadata,
            entities=entities
        )

    # edges: simple co-occurrence graph
    for i in range(len(chunks)):
        for j in range(i + 1, len(chunks)):
            ent_i = set(G.nodes[i]["entities"])
            ent_j = set(G.nodes[j]["entities"])

            if len(ent_i & ent_j) > 0:
                G.add_edge(i, j, weight=len(ent_i & ent_j))

    with open(GRAPH_PATH, "wb") as f:
        pickle.dump(G, f)

    print(f"Graph built with {len(G.nodes)} nodes")


if __name__ == "__main__":
    build_graph()