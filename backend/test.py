import chromadb
from sentence_transformers import SentenceTransformer
from llama import *

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="chroma_db_technical")
meta_collection = chroma_client.get_collection(name="pdf_metadata")
content_collection = chroma_client.get_collection(name="pdf_chunks")

# Load embedding model
model = SentenceTransformer("intfloat/e5-large-v2")

def retrieve_relevant_documents(user_query, n_results=3):
    """Retrieve the most relevant metadata entries to find high-level references."""
    query_embedding = model.encode(user_query).tolist()
    results = meta_collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return [metadata["source"] for metadata in results["metadatas"][0]]

def retrieve_relevant_chunks(relevant_docs, user_query, n_results=5):
    """Retrieve relevant text chunks from the identified documents."""
    query_embedding = model.encode(user_query).tolist()
    results = content_collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where={"source": {"$in": relevant_docs}} 
    )
    
    retrieved_data = []
    for metadata in results["metadatas"][0]:
        chunk_info = f"Source: {metadata['source']}, Page: {metadata['page']}\nText: {metadata['text']}\n"
        retrieved_data.append(chunk_info)
    
    return retrieved_data

def get_final_context(user_query):
    """First retrieves relevant documents, then retrieves detailed text chunks."""
    relevant_docs = retrieve_relevant_documents(user_query)
    if not relevant_docs:
        return "No relevant documents found."
    
    text_chunks = retrieve_relevant_chunks(relevant_docs, user_query)
    if not text_chunks:
        return "No detailed content found for the query."
    
    return "\n".join(text_chunks)


def get_user_input(query):
    new_query = rephrase_query(query)
    new_query1 = rephrase_query(query)
    new_query2 = rephrase_query(query)
    
    best_query = select_best_query(new_query, new_query1, new_query2, query)

    context = get_final_context(best_query)
    
    answer = rephrase_answer(context, query, 3)
    answer1 = rephrase_answer(context, query, 3)
    answer2 = rephrase_answer(context, query, 3)
    
    best_answer = select_best_answer(answer, answer1, answer2, best_query, context)
    
    return best_answer


