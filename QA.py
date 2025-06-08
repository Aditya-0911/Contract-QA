from sentence_transformers import SentenceTransformer
from google.generativeai import GenerativeModel
from typing import Optional

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def answer_question(question: str, vector_store, chunks) -> Optional[str]:
    question_embedding = embedding_model.encode([question])
    D, I = vector_store.search(question_embedding, k=5)
    relevant_chunks = [chunks[i] for i in I[0]]
    context = "\n".join(relevant_chunks)

    prompt = f"""
    Context: {context}
    Question: {question}
    Answer in simple language:
    """
    model = GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()