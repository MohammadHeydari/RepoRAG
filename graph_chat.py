# chat_graph.py
import ollama
from graph_search import search_graph

llm = ollama.chat


def build_context(results):
    return "\n\n".join(
        f"FILE: {r['metadata']['source']}\n{r['text']}"
        for r in results
    )


def chat(query):
    print(f"\nQuery: {query}")

    results = search_graph(query, k=5)
    context = build_context(results)

    prompt = f"""
You are a code assistant using GRAPH RAG.

Context:
{context}

Question: {query}

Answer clearly and precisely:
"""

    response = llm(
        model="gemma3:4b",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]


if __name__ == "__main__":
    while True:
        q = input("\nAsk repo question: ")
        if q.lower() in ["exit", "quit"]:
            break

        print(chat(q))