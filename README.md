# PDF AI Assistant Mini Project (Grok + RAG + Streamlit)

This mini project implements the complete workflow requested:
- Upload PDF
- Extract text + chunk it
- Store chunks in a vector database
- Answer questions using RAG
- Generate structured notes
- Evaluate and iteratively improve answers
- Run everything from Streamlit UI
- Include 2 Jupyter notebook assignments

## Tech Stack
- LLM: Grok (`grok-2-latest`) through xAI OpenAI-compatible endpoint
- Embeddings: `sentence-transformers/all-MiniLM-L6-v2`
- Vector DB: ChromaDB (local persistent storage)
- PDF parser: `pypdf` via `PyPDFLoader`
- UI: Streamlit
- Language: Python

## Folder Structure
- `app.py` -> Streamlit UI application
- `src/pipeline.py` -> Main orchestration class used by UI + notebooks
- `src/services/ingestion.py` -> PDF loading, chunking, and vector DB ingestion
- `src/services/rag.py` -> Q&A, notes generation, answer evaluation, iterative improvement calls
- `src/services/llm_provider.py` -> Grok LLM client + embedding model initialization
- `src/utils/helpers.py` -> Document formatting helper used for source-aware context
- `src/core/config.py` -> Project constants (chunking, model, defaults, paths)
- `src/core/schemas.py` -> Typed dataclasses for logical project entities
- `notebooks/assignment_1_ingestion_rag.ipynb` -> Assignment 1 notebook
- `notebooks/assignment_2_notes_improvement.ipynb` -> Assignment 2 notebook
- `.env.example` -> Environment variable template
- `requirements.txt` -> Python dependencies

## End-to-End Logic
1. User uploads PDF from Streamlit sidebar.
2. Uploaded PDF is saved into `data/`.
3. Ingestion pipeline reads PDF pages and splits text into overlapping chunks.
4. Chunks are embedded and stored in Chroma vector DB (`data/vector_db`).
5. For any question/topic, retriever fetches top-k relevant chunks.
6. Context from chunks is passed to Grok for:
   - direct answer generation,
   - structured notes generation,
   - answer evaluation in JSON format.
7. Iterative loop:
   - generate initial answer,
   - evaluate score/issues/instructions,
   - improve answer using instructions,
   - repeat until score is high or loops completed.
8. UI shows answer/notes plus source metadata and evaluation trace.

## File-wise Explanation

### `src/core/config.py`
Contains all runtime constants so settings are centralized:
- model name (`grok-2-latest`)
- embedding model
- chunk size/overlap
- top-k retrieval and default improvement loop count
- base directories for data and vector DB

### `src/core/schemas.py`
Defines clear dataclasses for logical units like retrieved chunks, answers, and evaluation result. This improves readability and future extension even if current returns are mostly dict-based for Streamlit compatibility.

### `src/services/llm_provider.py`
Responsible for model providers:
- `get_chat_model()` creates Grok chat client using xAI endpoint (`https://api.x.ai/v1`) and reads `XAI_API_KEY`.
- `get_embedding_model()` returns local sentence-transformer embeddings.

Why this separation: one place to switch model/provider settings without touching business logic.

### `src/services/ingestion.py`
Handles PDF ingestion and retrieval backend:
- reads PDF pages with `PyPDFLoader`
- chunks text via `RecursiveCharacterTextSplitter`
- stores vectors in persistent Chroma collection
- returns ingestion summary (page count, chunk count)
- builds retriever for semantic search

### `src/services/rag.py`
Implements all Grok calls:
- `answer_question()` -> grounded answer from context
- `generate_structured_notes()` -> fixed-format notes
- `evaluate_answer()` -> strict JSON output with score/issues/instructions
- `improve_answer()` -> rewrites answer using evaluator guidance

This is where generation + evaluation logic lives.

### `src/utils/helpers.py`
Formats retrieved chunks into a single context string while preserving source and page metadata in each block.

### `src/pipeline.py`
Main orchestration class (`RagAssistantPipeline`) with methods:
- `ingest(pdf_path)`
- `ask(question, k)`
- `notes(topic, k)`
- `iterative_answer(question, loops, k)`

`iterative_answer` performs evaluation-driven refinement loop and returns full trace.

### `app.py`
Streamlit user interface with 3 workflows:
1. PDF upload + ingest
2. Q&A
3. Notes generation
4. Iterative improvement demo (initial answer, improved answer, evaluations)

It stores a single pipeline instance in Streamlit session state.

### `notebooks/assignment_1_ingestion_rag.ipynb`
Assignment notebook focused on:
- environment loading
- ingestion call
- one RAG Q&A call

### `notebooks/assignment_2_notes_improvement.ipynb`
Assignment notebook focused on:
- notes generation
- iterative answer improvement loop

## Setup

### 1) Open in VS Code
- Open VS Code
- `File -> Open Folder -> C:\Users\Roja\smart-content-pipeline`

### 2) Create environment and install
```powershell
cd C:\Users\Roja\smart-content-pipeline
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Configure Grok API key
Create `.env` from `.env.example` and set:
```env
XAI_API_KEY=YOUR_REAL_XAI_KEY
```

### 4) Run Streamlit UI
```powershell
streamlit run app.py
```

## Demo Flow (for submission)
1. Launch Streamlit.
2. Upload any PDF and click **Ingest PDF**.
3. Ask a question in **Q&A** and show answer + sources.
4. Generate topic notes in **Structured Notes**.
5. Run **Iterative Improvement** and show initial answer, improved answer, and evaluation trace JSON.

## Notes on Design Choices
- LLM and embedding providers are separated for maintainability.
- Chroma persistence allows reuse across app restarts.
- Iterative improvement uses evaluator output to drive refinement, instead of generic rewriting.
- Code comments are intentionally minimal; full explanation is documented here as requested.

## GitHub Push Commands
After verifying everything works, run:
```powershell
echo "# pdf-ai-assistant-mini-project" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/rojadasappa/pdf-ai-assistant-mini-project.git
git push -u origin main
'''
