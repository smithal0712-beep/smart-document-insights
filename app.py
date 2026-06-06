import streamlit as st
import html
from rag_engine import ingest_pdf, ingest_multiple_pdfs, ask_question

st.set_page_config(
    page_title="Smart Document Insights",
    page_icon="PDF",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- CSS --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(59, 130, 246, 0.22), transparent 35%),
        radial-gradient(circle at bottom right, rgba(124, 58, 237, 0.22), transparent 35%),
        linear-gradient(135deg, #020617, #0f172a, #111827);
    color: white;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

[data-testid="stSidebar"] {
    background: rgba(2, 6, 23, 0.88);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(148, 163, 184, 0.18);
}

.sidebar-title {
    font-size: 28px;
    font-weight: 900;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}

.sidebar-text {
    color: #94a3b8;
    font-size: 14px;
    line-height: 1.7;
}

.status-ready {
    padding: 16px;
    border-radius: 16px;
    background: rgba(34, 197, 94, 0.15);
    border: 1px solid rgba(34, 197, 94, 0.35);
    color: #bbf7d0;
    font-weight: 700;
    text-align: center;
}

.status-wait {
    padding: 16px;
    border-radius: 16px;
    background: rgba(251, 191, 36, 0.14);
    border: 1px solid rgba(251, 191, 36, 0.35);
    color: #fde68a;
    font-weight: 700;
    text-align: center;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 42px;
    border-radius: 30px;
    background: rgba(15, 23, 42, 0.72);
    border: 1px solid rgba(148, 163, 184, 0.24);
    box-shadow: 0 30px 80px rgba(0, 0, 0, 0.45);
    backdrop-filter: blur(24px);
    margin-bottom: 26px;
    animation: fadeUp 0.8s ease;
}

.hero::before {
    content: "";
    position: absolute;
    inset: -2px;
    background: linear-gradient(120deg, transparent, rgba(56, 189, 248, 0.18), transparent);
    animation: shine 4s linear infinite;
}

.hero-content {
    position: relative;
    z-index: 1;
}

.badge {
    display: inline-block;
    padding: 9px 16px;
    border-radius: 999px;
    background: rgba(59, 130, 246, 0.16);
    border: 1px solid rgba(96, 165, 250, 0.42);
    color: #bfdbfe;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1.4px;
    margin-bottom: 20px;
}

.hero-title {
    font-size: 56px;
    line-height: 1.05;
    font-weight: 900;
    letter-spacing: -1.8px;
    background: linear-gradient(90deg, #ffffff, #93c5fd, #c4b5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 18px;
}

.hero-subtitle {
    max-width: 850px;
    font-size: 18px;
    line-height: 1.8;
    color: #cbd5e1;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    margin-top: 30px;
}

.metric-box {
    padding: 22px;
    border-radius: 22px;
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(148, 163, 184, 0.18);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
    transition: all 0.25s ease;
}

.metric-box:hover {
    transform: translateY(-4px);
    border-color: rgba(96, 165, 250, 0.55);
    box-shadow: 0 18px 45px rgba(37, 99, 235, 0.20);
}

.metric-number {
    font-size: 25px;
    font-weight: 900;
    color: white;
}

.metric-label {
    color: #94a3b8;
    font-size: 13px;
    margin-top: 7px;
}

.card {
    padding: 28px;
    border-radius: 26px;
    background: rgba(15, 23, 42, 0.74);
    border: 1px solid rgba(148, 163, 184, 0.22);
    box-shadow: 0 22px 55px rgba(0,0,0,0.35);
    backdrop-filter: blur(20px);
    margin-bottom: 24px;
    animation: fadeUp 0.9s ease;
}

.card:hover {
    border-color: rgba(96, 165, 250, 0.45);
    transition: 0.25s ease;
}

.section-title {
    font-size: 14px;
    font-weight: 900;
    color: #60a5fa;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 20px;
}

.upload-zone {
    padding: 34px;
    border-radius: 24px;
    border: 1.5px dashed rgba(96, 165, 250, 0.55);
    background: rgba(30, 41, 59, 0.45);
    text-align: center;
    margin-bottom: 22px;
    transition: 0.25s ease;
}

.upload-zone:hover {
    background: rgba(30, 41, 59, 0.7);
    transform: scale(1.01);
}

.upload-icon {
    width: 72px;
    height: 72px;
    border-radius: 22px;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px auto;
    font-size: 22px;
    font-weight: 900;
    color: white;
    box-shadow: 0 18px 40px rgba(37, 99, 235, 0.35);
}

.upload-title {
    font-size: 24px;
    font-weight: 900;
    margin-bottom: 8px;
}

.upload-subtitle {
    color: #94a3b8;
    font-size: 15px;
    line-height: 1.6;
}

.tip-list {
    color: #cbd5e1;
    line-height: 2.1;
    font-size: 15px;
}

.chat-area {
    min-height: 450px;
    max-height: 570px;
    overflow-y: auto;
    padding-right: 8px;
}

.empty-state {
    min-height: 400px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    text-align: center;
    color: #94a3b8;
}

.empty-icon {
    width: 90px;
    height: 90px;
    border-radius: 28px;
    background: linear-gradient(135deg, #0ea5e9, #7c3aed);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 28px;
    font-weight: 900;
    margin-bottom: 22px;
    animation: floatBox 3s ease-in-out infinite;
    box-shadow: 0 24px 60px rgba(124, 58, 237, 0.35);
}

.empty-title {
    font-size: 30px;
    font-weight: 900;
    color: #e5e7eb;
    margin-bottom: 8px;
}

.empty-text {
    color: #94a3b8;
    font-size: 16px;
}

.user-msg {
    margin: 16px 0 16px auto;
    max-width: 78%;
    padding: 18px 20px;
    border-radius: 22px 22px 6px 22px;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white;
    box-shadow: 0 16px 38px rgba(37, 99, 235, 0.28);
    animation: slideRight 0.35s ease;
}

.ai-msg {
    margin: 16px auto 16px 0;
    max-width: 84%;
    padding: 20px 22px;
    border-radius: 22px 22px 22px 6px;
    background: rgba(30, 41, 59, 0.88);
    border: 1px solid rgba(148, 163, 184, 0.24);
    color: #e5e7eb;
    line-height: 1.75;
    box-shadow: 0 16px 38px rgba(0,0,0,0.25);
    animation: slideLeft 0.35s ease;
}

.msg-label {
    font-size: 12px;
    font-weight: 900;
    color: #bfdbfe;
    margin-bottom: 8px;
    letter-spacing: 1px;
}

div.stButton > button {
    width: 100%;
    border-radius: 16px;
    padding: 14px 24px;
    font-weight: 900;
    color: white;
    border: none;
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    box-shadow: 0 16px 36px rgba(37, 99, 235, 0.28);
    transition: 0.25s ease;
}

div.stButton > button:hover {
    transform: translateY(-3px);
    color: white;
    box-shadow: 0 20px 42px rgba(124, 58, 237, 0.42);
}

.stTextInput input {
    border-radius: 16px !important;
    background: rgba(15, 23, 42, 0.95) !important;
    color: white !important;
    border: 1px solid rgba(148, 163, 184, 0.32) !important;
    padding: 15px !important;
}

.stTextInput input:focus {
    border-color: rgba(96, 165, 250, 0.9) !important;
    box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.14) !important;
}

[data-testid="stFileUploader"] {
    background: rgba(15, 23, 42, 0.35);
    border-radius: 18px;
    padding: 12px;
}

.footer-text {
    text-align: center;
    color: #64748b;
    font-size: 13px;
    margin-top: 20px;
}

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(22px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideLeft {
    from {
        opacity: 0;
        transform: translateX(-18px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideRight {
    from {
        opacity: 0;
        transform: translateX(18px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes floatBox {
    0% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(-12px);
    }
    100% {
        transform: translateY(0px);
    }
}

@keyframes shine {
    0% {
        transform: translateX(-80%);
    }
    100% {
        transform: translateX(80%);
    }
}
</style>
""", unsafe_allow_html=True)

# -------------------- Session State --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_ready" not in st.session_state:
    st.session_state.pdf_ready = False

if "file_name" not in st.session_state:
    st.session_state.file_name = None

# -------------------- Sidebar --------------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">Smart Insights</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-text">AI-powered document understanding using PDF extraction, embeddings, FAISS search, and Groq LLM.</div>',
        unsafe_allow_html=True
    )

    st.divider()

    if st.session_state.pdf_ready:
        st.markdown('<div class="status-ready">Document Ready</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-wait">Waiting for PDF</div>', unsafe_allow_html=True)

    if st.session_state.file_name:
        st.info(f"Current file: {st.session_state.file_name}")

    st.divider()

    st.subheader("Project Stack")
    st.write("Python")
    st.write("Streamlit")
    st.write("PyPDF")
    st.write("Sentence Transformers")
    st.write("FAISS")
    st.write("Groq LLM")

    st.divider()

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# -------------------- Hero --------------------
st.markdown("""
<div class="hero">
<div class="hero-content">
<div class="badge">AI DOCUMENT INTELLIGENCE</div>
<div class="hero-title">Smart Document Insights</div>
<div class="hero-subtitle">
Upload any PDF and interact with it like a smart assistant.
The app reads your document, understands its content, retrieves the most relevant parts,
and generates clean answers instantly.
</div>

<div class="metric-grid">
<div class="metric-box">
<div class="metric-number">PDF</div>
<div class="metric-label">Document Upload</div>
</div>

<div class="metric-box">
<div class="metric-number">RAG</div>
<div class="metric-label">AI Retrieval</div>
</div>

<div class="metric-box">
<div class="metric-number">FAISS</div>
<div class="metric-label">Vector Search</div>
</div>
</div>

</div>
""", unsafe_allow_html=True)

# -------------------- Main Layout --------------------
left_col, right_col = st.columns([1, 1.6], gap="large")

# -------------------- Left Column --------------------
with left_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Document Upload</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="upload-zone">
        <div class="upload-icon">PDF</div>
        <div class="upload-title">Upload your PDF</div>
        <div class="upload-subtitle">
            Your document will be converted into searchable AI knowledge.
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
    "Choose PDF files",
    type=["pdf"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

    if uploaded_files:
        st.session_state.file_name = ", ".join([file.name for file in uploaded_files])

        for index, uploaded_file in enumerate(uploaded_files):
            file_path = f"uploaded_{index}.pdf"

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

        st.success(f"Selected {len(uploaded_files)} PDF files")

        if st.button("Process Documents"):
            with st.spinner("Building AI knowledge base..."):
                result = ingest_multiple_pdfs(uploaded_files)
                st.session_state.pdf_ready = True
                st.success(result)

    else:
        st.warning("Upload PDF files to unlock the chat.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Smart Question Ideas</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="tip-list">
        - Summarise this document<br>
        - What are the key points?<br>
        - Explain this document in simple words<br>
        - What are the conclusions?<br>
        - Give me interview questions from this PDF<br>
        - Create short notes from this document
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- Right Column --------------------
with right_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">AI Conversation</div>', unsafe_allow_html=True)

    st.markdown('<div class="chat-area">', unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">AI</div>
            <div class="empty-title">Ask your document anything</div>
            <div class="empty-text">Upload and process a PDF, then start asking questions.</div>
        </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        safe_content = html.escape(msg["content"]).replace("\\n", "<br>")

        if msg["role"] == "user":
            st.markdown(f"""
            <div class="user-msg">
                <div class="msg-label">YOU</div>
                {safe_content}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="ai-msg">
                <div class="msg-label">AI ASSISTANT</div>
                {safe_content}
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Ask a Question</div>', unsafe_allow_html=True)

    question = st.text_input(
        "Ask something",
        placeholder="Example: Summarise this document in simple points...",
        label_visibility="collapsed"
    )

    ask_button = st.button("Generate Answer")

    if ask_button:
        if not st.session_state.pdf_ready:
            st.warning("Please upload and process a PDF first.")
        elif not question.strip():
            st.warning("Please type a question.")
        else:
            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

            with st.spinner("AI is reading your document..."):
                answer = ask_question(question)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="footer-text">Built with Python, Streamlit, FAISS, Sentence Transformers and Groq.</div>',
    unsafe_allow_html=True
)
