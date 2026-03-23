import json
from src.services.llm_provider import get_chat_model


def answer_question(question: str, context: str) -> str:
    llm = get_chat_model()
    prompt = (
        "You are a PDF assistant. Answer only from the context. "
        "If context is insufficient, explicitly say what is missing.\n\n"
        f"Question:\n{question}\n\n"
        f"Context:\n{context}"
    )
    return llm.invoke(prompt).content


def generate_structured_notes(topic: str, context: str) -> str:
    llm = get_chat_model()
    prompt = (
        "Create concise structured notes using this exact format:\n"
        "1) Topic Overview\n"
        "2) Key Concepts\n"
        "3) Important Facts\n"
        "4) Formulas/Definitions (if any)\n"
        "5) Quick Revision Points\n"
        "Keep notes accurate to context only.\n\n"
        f"Topic: {topic}\n\n"
        f"Context:\n{context}"
    )
    return llm.invoke(prompt).content


def evaluate_answer(question: str, answer: str, context: str) -> dict:
    llm = get_chat_model()
    prompt = (
        "Evaluate the answer quality from context and return strict JSON with keys: "
        "score (1-10), issues (list), improvement_instructions (list).\n\n"
        f"Question:\n{question}\n\n"
        f"Answer:\n{answer}\n\n"
        f"Context:\n{context}"
    )
    raw = llm.invoke(prompt).content
    return json.loads(raw)


def improve_answer(question: str, answer: str, context: str, instructions: list[str]) -> str:
    llm = get_chat_model()
    prompt = (
        "Improve the answer using the instructions. Keep it faithful to context.\n\n"
        f"Question:\n{question}\n\n"
        f"Current answer:\n{answer}\n\n"
        f"Instructions:\n{instructions}\n\n"
        f"Context:\n{context}"
    )
    return llm.invoke(prompt).content
