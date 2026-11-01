# AI Document Chatbot (Original Starter Project)

A starter full-stack project for asking questions about uploaded PDF or TXT documents.

## Features
- React chat interface
- FastAPI backend
- PDF/TXT upload and text extraction
- Simple retrieval from document chunks
- Optional local LLM integration through Ollama (no paid API key required)
- Clear fallback answer when no relevant document text is found

## Important
This is an original starter implementation, not a production-ready RAG system. The basic retrieval uses keyword overlap. For stronger semantic retrieval, add embeddings and a vector database later. Review, run, test, and customize it before presenting it in a portfolio.

## Requirements
- Python 3.10+
- Node.js 18+
- Optional: Ollama installed locally with a model pulled (for example `ollama pull llama3.2`)

## Run the backend
```bash
cd backend
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Backend runs at http://127.0.0.1:8000. API docs: http://127.0.0.1:8000/docs

## Run the frontend
Open a second terminal:
```bash
cd frontend
npm install
npm run dev
```
Open the local URL shown by Vite.

## Optional local AI
Install Ollama and pull a model. Set `OLLAMA_MODEL` if you want a different model name.
The backend attempts to call Ollama at `http://localhost:11434/api/generate`. If Ollama is unavailable, it returns the relevant retrieved text as a simple extractive response.

## Suggested next improvements
- Add semantic embeddings and vector search
- Add tests and input-size limits
- Add document deletion and per-session document isolation
- Add citations/page numbers for retrieved chunks
- Add authentication before deploying publicly
