import os
import ollama
import chromadb

# 1. Database create (data folder-la save aagum)
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="helpdesk")

# 2. Ella .txt files-a padikkirom
count = 0
for folder in ["data/public", "data/confidential"]:
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        # 3. Text-a numbers-a mathurom (embedding)
        result = ollama.embed(model="nomic-embed-text", input=text)
        vector = result["embeddings"][0]

        # 4. Database-la save
        collection.add(
            ids=[path],
            documents=[text],
            embeddings=[vector],
            metadatas=[{"source": path}],
        )
        count += 1
        print("Loaded:", path, "| numbers count:", len(vector))

print("Total documents in database:", collection.count())