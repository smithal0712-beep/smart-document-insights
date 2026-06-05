# 🧠 Smart Document Insights

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)

> Upload any PDF and get instant, intelligent answers — powered by RAG, FAISS vector search, and Groq's blazing-fast Llama 3.

---

## 📸 Screenshots

### 📂 Document Upload & Processing
![Upload Screenshot](upload.png)
> *Drag-and-drop PDF upload with real-time chunking and embedding progress.*

### 💬 Ask Anything Interface
![Chat Screenshot](chat.png)
> *Natural language Q&A with highlighted source context from the original document.*

---

## ✨ Features

- 📄 **PDF Ingestion** — Parse and chunk documents with PyPDF for accurate context extraction
- 🔍 **Semantic Search** — Embed chunks using Sentence Transformers and index with FAISS for lightning-fast retrieval
- 🤖 **LLM-Powered Answers** — Generate grounded, context-aware responses via Groq's Llama 3 API
- 🖥️ **Clean Streamlit UI** — Minimal, responsive interface for uploading documents and chatting
- ⚡ **Low Latency** — Groq inference delivers near-instant answers even on large documents

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend / UI** | [Streamlit](https://streamlit.io/) |
| **PDF Parsing** | [PyPDF](https://pypdf.readthedocs.io/) |
| **Embeddings** | [Sentence Transformers](https://www.sbert.net/) |
| **Vector Store** | [FAISS](https://github.com/facebookresearch/faiss) |
| **LLM** | [Groq — Llama 3](https://groq.com/) |
| **Language** | Python 3.10+ |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- A [Groq API key](https://console.groq.com/)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/smart-document-insights.git
cd smart-document-insights

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Run the App

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📁 Project Structure

```
smart-document-insights/
├── app.py                  # Main Streamlit application
├── rag/
│   ├── loader.py           # PDF parsing with PyPDF
│   ├── embedder.py         # Sentence Transformer embeddings
│   ├── retriever.py        # FAISS index build & search
│   └── generator.py        # Groq Llama 3 answer generation
├── screenshots/
│   ├── upload.png
│   └── chat.png
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ How It Works

```
 PDF Upload
     │
     ▼
 PyPDF → Text Chunks
     │
     ▼
 Sentence Transformers → Embeddings
     │
     ▼
 FAISS Index (stored in memory)
     │
     ▼
 User Query → Top-K Retrieval
     │
     ▼
 Groq Llama 3 → Grounded Answer
```

1. **Load** — The PDF is parsed and split into overlapping text chunks.
2. **Embed** — Each chunk is encoded into a dense vector using a Sentence Transformer model.
3. **Index** — Vectors are stored in a FAISS index for efficient similarity search.
4. **Retrieve** — On each user query, the top-K most relevant chunks are fetched.
5. **Generate** — Retrieved context is passed to Groq's Llama 3, which synthesizes a precise answer.

---

## 📦 Requirements

```
streamlit
pypdf
sentence-transformers
faiss-cpu
groq
python-dotenv
```

Install all at once:

```bash
pip install -r requirements.txt
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please make sure your code follows the existing style and includes relevant comments.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Groq](https://groq.com/) for ultra-fast LLM inference
- [Meta AI](https://ai.meta.com/) for the Llama 3 model
- [Hugging Face](https://huggingface.co/) for Sentence Transformers
- [Facebook Research](https://github.com/facebookresearch/faiss) for FAISS

---

<p align="center">Made with ❤️ and Python</p>
