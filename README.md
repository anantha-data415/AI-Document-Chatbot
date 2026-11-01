# 🤖 AI-Powered Document Chatbot

An AI-powered chatbot that allows users to upload PDF and TXT documents and ask questions about their content. It uses Gemini AI to generate answers based on the uploaded documents and displays relevant source information.

## 🚀 Project Overview

The AI Document Chatbot makes it easier to find information in documents. Instead of manually reading long files, users can upload a document and ask questions in natural language.

The application processes the document, retrieves relevant text sections, and uses Gemini AI to generate answers based on the available content.

## ✨ Features

- Upload PDF and TXT documents
- Extract text from uploaded documents
- Split document text into smaller chunks
- Retrieve relevant sections based on user questions
- Generate AI-powered answers using Gemini AI
- Display source document and relevant excerpts
- Simple and user-friendly chatbot interface

## 🛠️ Technologies Used

- **Programming Language:** Python
- **Backend:** FastAPI
- **AI Integration:** Google Gemini API
- **Frontend:** HTML, CSS, JavaScript
- **Document Processing:** PyPDF
- **Development Tools:** VS Code, Git, GitHub

## ⚙️ How It Works

1. The user uploads a PDF or TXT document.
2. The backend extracts text from the document.
3. The extracted text is divided into smaller chunks.
4. When the user asks a question, the application searches for relevant document sections.
5. The relevant context and question are sent to Gemini AI.
6. Gemini generates an answer based on the document context.
7. The chatbot displays the answer along with its source information.

## 💻 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/anantha-data415/AI-Document-Chatbot.git
```

### 2. Open the project folder

```bash
cd AI-Document-Chatbot
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```powershell
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the Gemini API key

Create a `.env` file inside `backend/app/` and add:

```env
GEMINI_API_KEY=your_api_key_here
```

Replace the placeholder with your own Gemini API key. Never upload your actual API key to GitHub.

### 7. Run the application

From the project root folder, run:

```bash
python -m uvicorn backend.app.main:app --reload
```

### 8. Open the application

Visit:

```text
http://127.0.0.1:8000
```

## 🎯 Learning Outcomes

Through this project, I gained practical experience in:

- Python application development
- Building REST APIs using FastAPI
- Integrating third-party AI APIs
- PDF and text document processing
- Text chunking and keyword-based retrieval
- Connecting frontend and backend components

## 👩‍💻 Developer

**Anantha**

GitHub: [anantha-data415](https://github.com/anantha-data415)

## 📌 Project Repository

[AI-Powered Document Chatbot](https://github.com/anantha-data415/AI-Document-Chatbot)