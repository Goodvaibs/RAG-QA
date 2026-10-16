# Travel Planner — Backend

A FastAPI backend that powers two features:

1. **Travel Itinerary Planner** — generates 4-day trip plans using TinyLlama via HuggingFace Transformers
2. **RAG Pipeline (Ask Me)** — answers questions from a PDF document using chunking, embeddings, Chroma vector store, and TinyLlama

---

## Prerequisites

- **Python** 3.10 or higher — [Download](https://www.python.org/)
- **pip** (comes with Python)
- A PDF document placed at `backend/src/docs/Atomic habits.pdf`
- Internet access on first run (to download model weights from HuggingFace)

> **Windows users:** Always run the server using the project virtual environment (`.venv`), not system Python. See Step 3.

---

## Project Structure

```
backend/src/
├── agents/
│   ├── agent.py        # Travel planner agent (uses TinyLlama)
│   └── myagent.py      # RAG agent (orchestrates pipeline steps)
├── models/
│   ├── model.py        # TinyLlama pipeline for travel planning
│   └── mymodel.py      # Full RAG pipeline (load → chunk → embed → vectorstore → LLM)
├── routers/
│   └── mydata.py       # API routes for RAG pipeline
├── docs/
│   └── Atomic habits.pdf   # Source document for RAG Q&A
├── data_vector_db/     # Chroma vector store (auto-created at runtime)
├── main.py             # FastAPI app entry point
├── requirements.txt    # Python dependencies
└── .venv/              # Virtual environment (created in setup)
```

---

## Setup

### 1. Navigate to the backend source folder

```powershell
cd backend\src
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
# Windows (PowerShell)
.\.venv\Scripts\activate

# Windows (Command Prompt)
.\.venv\Scripts\activate.bat
```

> You should see `(.venv)` at the start of your prompt.

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

> **Note:** `torch` is a large package (~2 GB). This step may take several minutes.

### 5. Run the server

```powershell
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at `http://127.0.0.1:8000`.  
Interactive docs (Swagger UI) at `http://127.0.0.1:8000/docs`.

---

---

### RAG Pipeline — Step-by-Step

The RAG pipeline must be initialised in order before asking questions. Call each endpoint once per server session:

#### Step 1 — Load PDF data

```
GET /api/v1/load-data
```

Loads the PDF from `docs/medical_diagnosis_manual.pdf` into memory.  
Returns the total number of pages loaded.
We can implement document upload later

#### Step 2 — Check loaded data (optional)

```
GET /api/v1/check-data
```

Returns a preview of pages 8–14 to verify the document loaded correctly.

#### Step 3 — Chunk the document

```
POST /api/v1/data-chunking
```

Splits the document into overlapping chunks of 600 tokens (overlap: 20) using `RecursiveCharacterTextSplitter` with the `cl100k_base` tiktoken encoder.  
Also initialises the embedding model (`sentence-transformers/all-MiniLM-L6-v2`).  
Returns the total number of chunks created.

#### Step 4 — Generate vector store

```
POST /api/v1/generate-vector-store
```

Embeds all chunks and stores them in a **Chroma** vector database, persisted to `data_vector_db/` on disk.  
Returns a success message.

#### Step 5 — Load the LLM

```
GET /api/v1/generate-rag-pipeline
```

Loads the **TinyLlama-1.1B-Chat** model via HuggingFace Transformers pipeline.  
Model is downloaded from HuggingFace on first run and cached locally.  
Returns a success message.

#### Step 6 — Ask a question

```
POST /api/v1/ask-question
```

Runs the full RAG query: retrieves the 3 most relevant chunks from the vector store, builds a prompt with context, and generates an answer using TinyLlama.

**Request body:**

```json
{ "query": "What are the risk factors for undernutrition?" }
```

**Query the vector store directly (optional):**

```
POST /api/v1/query-vector-store
```

Returns raw matching document chunks without generating an answer.

---

## Dependencies

| Package                       | Purpose                                     |
| ----------------------------- | ------------------------------------------- |
| `fastapi[standard]`           | Web framework                               |
| `uvicorn[standard]`           | ASGI server                                 |
| `transformers`                | HuggingFace model loading (TinyLlama)       |
| `huggingface-hub>=1.5.0,<2.0` | Model download from HuggingFace             |
| `torch`                       | Deep learning backend for transformers      |
| `pydantic`                    | Request/response validation                 |
| `python-dotenv`               | Environment variable management             |
| `langchain`                   | LLM orchestration utilities                 |
| `langchain-community`         | Document loaders, embeddings, vector stores |
| `pymupdf`                     | PDF loading (`PyMuPDFLoader`)               |
| `tiktoken`                    | Token-based text splitting                  |
| `sentence-transformers`       | Embedding model (`all-MiniLM-L6-v2`)        |
| `chromadb`                    | Vector database                             |

---

## Troubleshooting

### `ImportError: cannot import name 'is_offline_mode' from 'huggingface_hub'`

Your system Python has an outdated `huggingface_hub`. Always run using the project `.venv` — see Step 3 above.

### `ModuleNotFoundError: No module named 'langchain.text_splitter'`

This module moved in langchain 1.x. The project already uses `langchain_classic.text_splitter` as the correct import.

### `ModuleNotFoundError: No module named 'langchain.llms'`

This module moved in langchain 1.x. The project uses `langchain_community.llms` as the correct import.

### Server starts but APIs return 500

Ensure you call the RAG pipeline steps in order (Steps 1 → 5) before calling `/ask-question`.
