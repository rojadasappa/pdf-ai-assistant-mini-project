from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from src.core.config import VECTOR_DB_DIR, CHUNK_SIZE, CHUNK_OVERLAP
from src.services.llm_provider import get_embedding_model


def ingest_pdf(pdf_path: str, collection_name: str = "pdf_rag") -> dict:
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(docs)

    embeddings = get_embedding_model()
    vectordb = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=str(VECTOR_DB_DIR),
    )
    vectordb.add_documents(chunks)

    return {
        "pages": len(docs),
        "chunks": len(chunks),
        "collection": collection_name,
        "db_path": str(VECTOR_DB_DIR),
    }


def get_retriever(collection_name: str = "pdf_rag", k: int = 4):
    embeddings = get_embedding_model()
    vectordb = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=str(VECTOR_DB_DIR),
    )
    return vectordb.as_retriever(search_kwargs={"k": k})
