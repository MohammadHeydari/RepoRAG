# chunker.py
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_texts(texts, metadatas, chunk_size=800, chunk_overlap=100):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    docs = []

    for text, meta in zip(texts, metadatas):

        if "extension" not in meta:
            meta["extension"] = os.path.splitext(meta.get("source", ""))[1].lower()

        chunks = splitter.create_documents(
            [text],
            metadatas=[meta]
        )
        docs.extend(chunks)

    return docs


def print_sample_chunk(chunks, n=3):
    print(f"Total chunks: {len(chunks)}\n")
    for i, chunk in enumerate(chunks[:n], 1):
        print(f"--- Chunk {i} ---")
        print(f"File: {chunk.metadata['source']} | Extension: {chunk.metadata.get('extension')}")
        print(chunk.page_content[:500])
        print()