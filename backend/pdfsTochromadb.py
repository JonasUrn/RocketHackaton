import json
import chromadb
import os
import fitz  # PyMuPDF for PDF processing
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="chroma_db_technical")
meta_collection = chroma_client.get_or_create_collection(name="pdf_metadata")
content_collection = chroma_client.get_or_create_collection(name="pdf_chunks")

# Load embedding model
model = SentenceTransformer("intfloat/e5-large-v2")

def extract_metadata(doc):
    """Extracts metadata summary from the first two pages."""
    metadata_text = " ".join([page.get_text("text").split("\n")[0] for page in doc[:2] if page.get_text("text").strip()])
    return metadata_text.strip()

def chunk_text(text, max_words=200, overlap=50):
    """Splits text into overlapping chunks."""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i : i + max_words])
        chunks.append(chunk)
        i += max_words - overlap
    return chunks

def process_pdf(pdf_path):
    """Extracts metadata, chunks text, and stores both in ChromaDB."""
    try:
        doc = fitz.open(pdf_path)
        pdf_name = os.path.basename(pdf_path)
        
        # Store metadata summary
        metadata_text = extract_metadata(doc)
        if metadata_text:
            meta_embedding = model.encode(metadata_text).tolist()
            meta_collection.upsert(ids=[pdf_name], embeddings=[meta_embedding],
                                   metadatas=[{"source": pdf_name, "summary": metadata_text}])
        
        # Process full-text with chunking
        all_chunks = []
        for i, page in enumerate(doc):
            text = page.get_text("text").strip()
            if not text:
                continue
            
            # Chunk page text
            chunks = chunk_text(text)
            for chunk in chunks:
                all_chunks.append({"source": pdf_name, "page": i, "content": chunk})
        
        # Batch process embeddings
        batch_size = 8
        for j in tqdm(range(0, len(all_chunks), batch_size), desc=f"Processing {pdf_name}"):
            batch = all_chunks[j : j + batch_size]
            batch_texts = [b["content"] for b in batch]
            batch_embeddings = model.encode(batch_texts, batch_size=batch_size).tolist()
            
            content_collection.upsert(
                ids=[f"{pdf_name}_p{b['page']}_{hash(b['content'])}" for b in batch],
                embeddings=batch_embeddings,
                metadatas=[{"source": b["source"], "page": b["page"], "text": b["content"]} for b in batch]
            )
        
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")

def process_pdfs(pdf_folder):
    """Processes all PDFs in a directory."""
    pdf_files = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
    for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
        process_pdf(pdf_file)

pdf_directory = r"Redbooks" # (sometimes it doesn't work so change to your full path name to Redbooks folder)
process_pdfs(pdf_directory)

print("All PDFs processed and stored in ChromaDB.")
