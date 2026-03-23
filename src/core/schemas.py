from dataclasses import dataclass
from typing import List, Dict


@dataclass
class RetrievalChunk:
    source: str
    page: int
    text: str


@dataclass
class RagAnswer:
    question: str
    answer: str
    chunks: List[RetrievalChunk]


@dataclass
class EvaluationResult:
    score: int
    issues: List[str]
    improvement_instructions: List[str]


@dataclass
class IterativeAnswerResult:
    initial_answer: str
    improved_answer: str
    evaluations: List[Dict]
