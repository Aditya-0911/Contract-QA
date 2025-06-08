from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import streamlit as st

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(pdf_doc) -> str:
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def chunk_text(text, chunk_size=2000, chunk_overlap=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size - chunk_overlap)]

def build_vector_store(chunks):
    embeddings = embedding_model.encode(chunks)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index, chunks


