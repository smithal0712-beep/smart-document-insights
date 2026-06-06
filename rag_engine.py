import os
import pickle
import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Please add it in your .env file.")

model = SentenceTransformer("all-MiniLM-L6-v2")
client = Groq(api_key=GROQ_API_KEY)


def ingest_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    if not text.strip():
        raise ValueError("No text found in the PDF.")

    chunks = [text[i:i + 500] for i in range(0, len(text), 450)]
    embeddings = np.array(model.encode(chunks)).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, "faiss_index.bin")

    with open("chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

    return "PDF ingested successfully."


def ingest_multiple_pdfs(uploaded_files):
    text = ""

    for uploaded_file in uploaded_files:
        reader = PdfReader(uploaded_file)

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    if not text.strip():
        raise ValueError("No text found in uploaded PDFs.")

    chunks = [text[i:i + 500] for i in range(0, len(text), 450)]
    embeddings = np.array(model.encode(chunks)).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, "faiss_index.bin")

    with open("chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

    return f"{len(uploaded_files)} PDFs ingested successfully."


def ask_question(question):
    if not os.path.exists("faiss_index.bin") or not os.path.exists("chunks.pkl"):
        return "Please upload and ingest a PDF first."

    index = faiss.read_index("faiss_index.bin")

    with open("chunks.pkl", "rb") as f:
        chunks = pickle.load(f)

    question_embedding = np.array(model.encode([question])).astype("float32")
    _, indexes = index.search(question_embedding, 4)

    context = "\n".join([chunks[i] for i in indexes[0]])

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Answer the question using only the given context."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}"
            }
        ]
    )

    return response.choices[0].message.content
