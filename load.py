# load.py
import os

ALLOWED_EXTENSIONS = {".py", ".md", ".txt", ".yml", ".yaml", ".json", ".sql", ".js"}

def load_files(repo_path):
    texts = []
    metadatas = []

    for root, dirs, files in os.walk(repo_path):
        if ".git" in root:
            continue

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                continue

            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if not content.strip():
                        continue
                    texts.append(content)

                    metadatas.append({
                        "source": file_path,
                        "extension": ext
                    })
            except Exception as e:
                print(f"Warning: failed to read {file_path}: {e}")
                continue

    return texts, metadatas