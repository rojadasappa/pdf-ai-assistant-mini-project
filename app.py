import os
from dotenv import load_dotenv
import streamlit as st
from src.pipeline import RagAssistantPipeline

load_dotenv()
st.set_page_config(page_title="PDF RAG Assistant", layout="wide")
st.title("PDF RAG Assistant (Grok + Chroma)")

if "pipeline" not in st.session_state:
    st.session_state.pipeline = RagAssistantPipeline(collection_name="pdf_rag")

with st.sidebar:
    st.header("Setup")
    st.write("Set XAI_API_KEY in .env or environment before use.")
    uploaded = st.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded:
        os.makedirs("data", exist_ok=True)
        pdf_path = os.path.join("data", uploaded.name)
        with open(pdf_path, "wb") as f:
            f.write(uploaded.getbuffer())
        if st.button("Ingest PDF"):
            result = st.session_state.pipeline.ingest(pdf_path)
            st.success(f"Ingested: pages={result['pages']}, chunks={result['chunks']}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Q&A")
    question = st.text_input("Ask a question")
    if st.button("Get Answer") and question:
        out = st.session_state.pipeline.ask(question)
        st.markdown("### Answer")
        st.write(out["answer"])
        st.markdown("### Sources")
        st.json(out["sources"])

with col2:
    st.subheader("Structured Notes")
    topic = st.text_input("Topic for notes")
    if st.button("Generate Notes") and topic:
        out = st.session_state.pipeline.notes(topic)
        st.markdown("### Notes")
        st.write(out["notes"])
        st.markdown("### Sources")
        st.json(out["sources"])

st.subheader("Iterative Improvement")
iter_q = st.text_input("Question for iterative answer")
loops = st.slider("Improvement loops", min_value=1, max_value=5, value=2)
if st.button("Run Iterative Improvement") and iter_q:
    out = st.session_state.pipeline.iterative_answer(iter_q, loops=loops)
    st.markdown("### Initial Answer")
    st.write(out["initial_answer"])
    st.markdown("### Improved Answer")
    st.write(out["improved_answer"])
    st.markdown("### Evaluation Trace")
    st.json(out["evaluations"])
