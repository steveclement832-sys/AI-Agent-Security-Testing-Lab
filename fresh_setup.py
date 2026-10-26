import ollama
import chromadb
import os

client = chromadb.PersistentClient(path="chroma_db")

# Pazhaiya boxes irundha delete pannu, clean-a start panna
for name in ["helpdesk", "public_docs", "admin_docs"]:
    try:
        client.delete_collection(name)
        print("Deleted old collection:", name)
    except Exception:
        pass

public_col = client.get_or_create_collection(name="public_docs")
admin_col = client.get_or_create_collection(name="admin_docs")

def load(folder, collection):
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        vector = ollama.embed(model="nomic-embed-text", input=text)["embeddings"][0]
        collection.add(ids=[path], documents=[text], embeddings=[vector],
                       metadatas=[{"source": path}])
        print("Loaded into", collection.name, ":", path)

load("data/public", public_col)
load("data/confidential", admin_col)
print("\nFINAL COUNT -> Public docs:", public_col.count(), "| Admin docs:", admin_col.count())
