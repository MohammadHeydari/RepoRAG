# chat.py

from search import search
import ollama


def build_context(results):
    """Combine retrieved chunks into a single context string"""
    return "\n\n".join([
        f"FILE: {r['metadata']['source']}\n{r['text']}"
        for r in results
    ])


def chat(query, k=5):
    print(f"\nQuery: {query}")

    # 1. Retrieve top chunks
    results = search(query, k=k)
    context = build_context(results)

    # 2. Prompt
    prompt = f"""
You are a helpful assistant that answers questions using ONLY the context below.

Context:
{context}

Question: {query}

Answer clearly and concisely:
"""

    # 3. Call Ollama correctly
    response = ollama.chat(
        model="gemma3:4b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]


if __name__ == "__main__":
    while True:
        q = input("\nAsk repo question: ")
        if q.lower() in ["exit", "quit"]:
            break

        resp = chat(q, k=5)
        print("\n--- ANSWER ---\n")
        print(resp)