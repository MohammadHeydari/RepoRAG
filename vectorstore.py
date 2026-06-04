# vectorstore.py

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from load import load_files
from chunker import chunk_texts

REPO_PATH = "./repo"
VECTOR_PATH = "./vector.index"
META_PATH = "./metadata.npy"


def build_vectorstore():
    print("Loading repo...")

    texts, metas = load_files(REPO_PATH)

    if not texts:
        print("No files loaded!")
        return

    print(f"Loaded files: {len(texts)}")

    print("Chunking...")
    chunks = chunk_texts(texts, metas)

    print(f"Total chunks: {len(chunks)}")

    # embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    texts_only = [c.page_content for c in chunks]

    print("Embedding...")
    embeddings = model.encode(texts_only, show_progress_bar=True)

    embeddings = np.array(embeddings).astype("float32")

    # cosine similarity via inner product
    faiss.normalize_L2(embeddings)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)

    index.add(embeddings)

    # save index
    faiss.write_index(index, VECTOR_PATH)

    # save chunks (metadata + text)
    np.save(META_PATH, chunks, allow_pickle=True)

    print("Vector store created successfully!")


if __name__ == "__main__":
    build_vectorstore()