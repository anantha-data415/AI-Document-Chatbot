
from __future__ import annotations

import os
import re
import time
from io import BytesIO
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from google import genai
from pydantic import BaseModel
from pypdf import PdfReader


# Load Gemini API key
load_dotenv("backend/app/.env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is missing from backend/app/.env"
    )

client = genai.Client(api_key=api_key)


# Create FastAPI application
app = FastAPI(
    title="AI Document Chatbot",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Store document chunks
DOCUMENT_CHUNKS: List[dict] = []


class AskRequest(BaseModel):
    question: str


# Split document into smaller chunks
def split_into_chunks(
    text: str,
    size: int = 850,
    overlap: int = 120
) -> List[str]:

    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = min(len(text), start + size)
        chunks.append(text[start:end])

        if end == len(text):
            break

        start = end - overlap

    return chunks


# Extract text from PDF or TXT
def extract_text(filename: str, data: bytes) -> str:

    lower = filename.lower()

    if lower.endswith(".txt"):
        return data.decode("utf-8", errors="replace")

    if lower.endswith(".pdf"):
        reader = PdfReader(BytesIO(data))

        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    raise HTTPException(
        status_code=400,
        detail="Upload a PDF or TXT file."
    )


# Home page
@app.get("/")
def home():
    return FileResponse("backend/app/index.html")


# Health check
@app.get("/health")
def health():
    return {
        "status": "ok",
        "stored_chunks": len(DOCUMENT_CHUNKS)
    }


# Upload document
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Missing filename."
        )

    data = await file.read()

    if len(data) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="File must be 10 MB or smaller."
        )

    text = extract_text(file.filename, data)
    chunks = split_into_chunks(text)

    if not chunks:
        raise HTTPException(
            status_code=400,
            detail="No readable text found in the document."
        )

    DOCUMENT_CHUNKS.clear()

    DOCUMENT_CHUNKS.extend(
        {
            "document": file.filename,
            "chunk_id": i + 1,
            "text": chunk
        }
        for i, chunk in enumerate(chunks)
    )

    return {
        "message": "Document processed successfully",
        "filename": file.filename,
        "chunks": len(chunks)
    }


# Retrieve relevant document sections
def retrieve(question: str, limit: int = 4) -> List[dict]:

    words = {
        word.lower()
        for word in re.findall(r"[A-Za-z0-9]+", question)
        if len(word) > 2
    }

    scored = []

    for chunk in DOCUMENT_CHUNKS:

        chunk_words = {
            word.lower()
            for word in re.findall(
                r"[A-Za-z0-9]+",
                chunk["text"]
            )
            if len(word) > 2
        }

        score = len(words & chunk_words)

        if score:
            scored.append((score, chunk))

    scored.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        chunk
        for score, chunk in scored[:limit]
    ]


# Generate answer using Gemini with retry
def generate_with_gemini(
    question: str,
    context: str
) -> str:

    prompt = (
        "You are an AI document assistant. "
        "Answer the user's question using only the "
        "information in the document below. "
        "Give a short, clear and direct answer. "
        "Do not invent information. "
        "If the answer is unavailable, clearly say "
        "that the document does not provide enough information.\n\n"
        f"DOCUMENT:\n{context}\n\n"
        f"QUESTION: {question}\n\n"
        "ANSWER:"
    )

    for attempt in range(3):

        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            return (response.text or "").strip()

        except Exception as error:

            error_message = str(error)

            temporary_error = (
                "503" in error_message
                or "UNAVAILABLE" in error_message
            )

            if temporary_error and attempt < 2:

                wait_time = 2 ** (attempt + 1)

                print(
                    f"Gemini busy. Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

                continue

            raise


# Ask questions about uploaded document
@app.post("/ask")
def ask(request: AskRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Please enter a question."
        )

    if not DOCUMENT_CHUNKS:
        raise HTTPException(
            status_code=400,
            detail="Upload a document first."
        )

    relevant_chunks = retrieve(
        question,
        limit=4
    )

    if not relevant_chunks:
        relevant_chunks = DOCUMENT_CHUNKS[:4]

    context = "\n\n".join(
        chunk["text"]
        for chunk in relevant_chunks
    )

    try:
        answer = generate_with_gemini(
            question,
            context
        )

        if not answer:
            answer = (
                "I couldn't generate an answer. "
                "Please try again."
            )

    except Exception as error:

        print("Gemini error:", error)

        raise HTTPException(
            status_code=502,
            detail=(
                f"Gemini error: {type(error).__name__}: {error}"
            )
        )

    return {
        "answer": answer,
        "sources": [
            {
                "document": chunk["document"],
                "section": chunk["chunk_id"],
                "excerpt": chunk["text"][:220]
            }
            for chunk in relevant_chunks
        ],
        "mode": "gemini-ai"
    }
