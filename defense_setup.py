import ollama
import chromadb

client = chromadb.PersistentClient(path="chroma_db")

# Rendu THANI collection: public and confidential
public_col = client.get_or_create_collection(name="public_docs")
admin_col = client.get_or_create_collection(name="admin_docs")

def load(folder, collection):
    import os
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
print("Public docs:", public_col.count(), "| Admin docs:", admin_col.count())