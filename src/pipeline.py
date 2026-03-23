from typing import Any
from src.core.config import DEFAULT_TOP_K, DEFAULT_IMPROVEMENT_LOOPS
from src.services.ingestion import ingest_pdf, get_retriever
from src.services.rag import (
    answer_question,
    generate_structured_notes,
    evaluate_answer,
    improve_answer,
)
from src.utils.helpers import format_docs


class RagAssistantPipeline:
    def __init__(self, collection_name: str = "pdf_rag"):
        self.collection_name = collection_name

    def ingest(self, pdf_path: str) -> dict[str, Any]:
        return ingest_pdf(pdf_path=pdf_path, collection_name=self.collection_name)

    def _retrieve(self, query: str, k: int = DEFAULT_TOP_K):
        retriever = get_retriever(collection_name=self.collection_name, k=k)
        docs = retriever.invoke(query)
        context = format_docs(docs)
        return docs, context

    def ask(self, question: str, k: int = DEFAULT_TOP_K) -> dict[str, Any]:
        docs, context = self._retrieve(question, k)
        answer = answer_question(question, context)
        return {
            "question": question,
            "answer": answer,
            "sources": [d.metadata for d in docs],
            "context": context,
        }

    def notes(self, topic: str, k: int = DEFAULT_TOP_K) -> dict[str, Any]:
        docs, context = self._retrieve(topic, k)
        notes = generate_structured_notes(topic, context)
        return {
            "topic": topic,
            "notes": notes,
            "sources": [d.metadata for d in docs],
            "context": context,
        }

    def iterative_answer(self, question: str, loops: int = DEFAULT_IMPROVEMENT_LOOPS, k: int = DEFAULT_TOP_K) -> dict[str, Any]:
        docs, context = self._retrieve(question, k)
        answer = answer_question(question, context)

        evaluations = []
        improved = answer
        for _ in range(loops):
            eval_json = evaluate_answer(question, improved, context)
            evaluations.append(eval_json)
            instructions = eval_json.get("improvement_instructions", [])
            if eval_json.get("score", 0) >= 9 or not instructions:
                break
            improved = improve_answer(question, improved, context, instructions)

        return {
            "question": question,
            "initial_answer": answer,
            "improved_answer": improved,
            "evaluations": evaluations,
            "sources": [d.metadata for d in docs],
            "context": context,
        }
