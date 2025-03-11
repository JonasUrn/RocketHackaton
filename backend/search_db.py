import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path="chroma_db")  # Persistent storage
collection = chroma_client.get_or_create_collection(name="pdf_chunks")

def search_chroma(query):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1
    )

    top_3_results = results["metadatas"][0]

    response = "\n\n".join(
        [f"Result {i+1} (Source: {result['source']}):\n{result['text']}" for i, result in enumerate(top_3_results)]
    )

    return response 

    
    