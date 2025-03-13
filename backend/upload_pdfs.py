import json
import chromadb
import os
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from pdfminer.high_level import extract_text
from transformers import AutoTokenizer

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="chroma_db_technical")
collection = chroma_client.get_or_create_collection(name="pdf_chunks")

# Load embedding model
model = SentenceTransformer("intfloat/e5-large-v2")
tokenizer = AutoTokenizer.from_pretrained("intfloat/e5-large-v2")

def extract_text_from_pdf(pdf_path):
    try:
        return extract_text(pdf_path).strip()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

def chunk_text(text, max_words=200, overlap=50):
    words = text.split()
    chunks = []
    
    i = 0
    while i < len(words):
        chunk = " ".join(words[i : i + max_words])
        chunks.append(chunk)
        i += max_words - overlap
    
    return chunks

def process_and_store(pdf_file):
    text = extract_text_from_pdf(pdf_file)
    if not text:
        print(f"Skipping {pdf_file}, no text found.")
        return

    chunks = [{"source": pdf_file, "content": chunk} for chunk in chunk_text(text)]
    batch_size = 8
    texts = [chunk["content"] for chunk in chunks]
    sources = [chunk["source"] for chunk in chunks]

    for i in tqdm(range(0, len(texts), batch_size), desc=f"Processing {pdf_file}"):
        batch_texts = texts[i : i + batch_size]
        batch_embeddings = model.encode(batch_texts, batch_size=batch_size).tolist()

        collection.upsert( 
            ids=[str(hash(src + txt)) for src, txt in zip(sources[i : i + batch_size], batch_texts)],
            embeddings=batch_embeddings,
            metadatas=[{"source": src, "text": txt} for src, txt in zip(sources[i : i + batch_size], batch_texts)],
        )

def process_pdfs(pdf_folder):
    pdf_files = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

    for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
        process_and_store(pdf_file) 

pdf_directory = r"backend\pdfs\IBM_Redbooks"
process_pdfs(pdf_directory)

print("✅ All PDFs processed and stored in ChromaDB.")
