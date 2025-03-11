import json
import chromadb
from sentence_transformers import SentenceTransformer

# Load processed text chunks
with open("processed_texts.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="chroma_db")  # Persistent storage
collection = chroma_client.get_or_create_collection(name="pdf_chunks")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight and efficient

# Store each text chunk with its embedding
for i, chunk in enumerate(chunks):
    embedding = model.encode(chunk["content"]).tolist()
    collection.add(
        ids=[str(i)],  # Unique ID for each entry
        embeddings=[embedding],
        metadatas=[{"source": chunk["source"], "text": chunk["content"]}],
    )

print(f"Stored {len(chunks)} text chunks in ChromaDB.")

query = "What is the project about?"
query_embedding = model.encode(query).tolist()

# Retrieve top 5 most relevant chunks
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)

# Print results
for i, result in enumerate(results["metadatas"][0]):
    print(f"Result {i+1}: (Source: {result['source']})\n{result['text']}\n")

