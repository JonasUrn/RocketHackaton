import os
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm import tqdm
import json

PDF_FOLDER = "backend\pdfs\IBM_Redbooks"
OUTPUT_FILE = "processed_texts.json"

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text.strip()

def process_pdfs(pdf_folder):
    """Extract text from all PDFs and split into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    all_chunks = []

    for pdf in tqdm(os.listdir(pdf_folder)):
        if pdf.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, pdf)
            text = extract_text_from_pdf(pdf_path)
            chunks = text_splitter.split_text(text)
            for chunk in chunks:
                all_chunks.append({"source": pdf, "content": chunk})

    return all_chunks

# Extract and store data
chunks = process_pdfs(PDF_FOLDER)

# Save to JSON (efficient and easy to load later)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=4)

print(f"Processed {len(chunks)} text chunks. Saved to {OUTPUT_FILE}")
