# ingest.py
from load import load_files
from chunker import chunk_texts, print_sample_chunk

REPO_PATH = "./repo"

def main():
    print("Loading repo files...")

    texts, metas = load_files(REPO_PATH)

    if not texts:
        print("No files loaded! Check REPO_PATH and ALLOWED_EXTENSIONS.")
        return

    print(f"Loaded {len(texts)} files")

    print("Chunking...")

    chunks = chunk_texts(texts, metas)

    print_sample_chunk(chunks, n=3)

    for meta in metas:
        ext = meta.get("extension")
        print(f"File: {meta['source']} -> extension: {ext}")

    return chunks

if __name__ == "__main__":
    main()