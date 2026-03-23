import os
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from src.core.config import MODEL_NAME, EMBEDDING_MODEL


def get_chat_model() -> ChatOpenAI:
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        raise ValueError("XAI_API_KEY is missing. Add it in environment variables or .env file.")

    return ChatOpenAI(
        model=MODEL_NAME,
        api_key=api_key,
        base_url="https://api.x.ai/v1",
        temperature=0.2,
    )


def get_embedding_model() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
