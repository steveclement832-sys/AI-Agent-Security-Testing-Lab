import chromadb
client = chromadb.PersistentClient(path="chroma_db")
print("All collections:", [c.name for c in client.list_collections()])
print("public_docs count:", client.get_collection("public_docs").count())
print("helpdesk count:", client.get_collection("helpdesk").count())