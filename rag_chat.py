import ollama
import chromadb

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection(name="helpdesk")

SYSTEM_PROMPT = "You are the IT Helpdesk assistant. Answer using the provided documents."

def ask(question):
    # 1. Kelvi-a numbers-a mathurom
    q_vector = ollama.embed(model="nomic-embed-text", input=question)["embeddings"][0]

    # 2. Database-la mosta match aagura 2 documents thedurom
    results = collection.query(query_embeddings=[q_vector], n_results=2)
    docs = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]

    # 3. Documents-a oru text-a serkurom
    context = "\n\n".join(docs)

    # 4. Documents + kelvi-a llama3.1-kitta kudukkurom
    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Documents:\n{context}\n\nQuestion: {question}"},
        ],
    )
    return response["message"]["content"], sources

while True:
    q = input("\nYou: ")
    if q.lower() in ["exit", "quit"]:
        break
    answer, sources = ask(q)
    print("\nAssistant:", answer)
    print("(Sources:", sources, ")")