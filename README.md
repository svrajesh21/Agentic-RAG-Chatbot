# Agentic RAG Chatbot (LangChain + Flask)

A futuristic, agent-powered chatbot that uses Retrieval-Augmented Generation (RAG) to answer questions from uploaded documents (PDF, DOCX, TXT, CSV, PPTX). Includes OCR support for scanned PDFs and an animated UI built with Flask + HTML/CSS/JS.

## 🚀 Features
- 📁 Supports PDFs (including scanned), DOCX, CSV, TXT, PPTX
- 🔍 Uses FAISS + OpenAI embeddings for semantic search
- 🧠 LLM (GPT-3.5) powered answers via LangChain
- 🤖 Animated robot-themed UI (HTML + Jinja)
- 🧼 Handles garbage OCR text and unsupported formats gracefully
- 🔐 .env API key loading

## 🛠 Setup Instructions

### 1. Clone and Navigate
git clone https://github.com/svrajesh21/Agentic-RAG-Chatbot.git

cd Agentic-RAG-Chatbot

### 2. Create & Activate Virtual Environment
python -m venv venv

venv\Scripts\activate  # Windows

source venv/bin/activate # macOS/Linux

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Add .env File
Create a .env file at root:
OPENAI_API_KEY=your-openai-api-key-here

### 5. (Optional) Install Tesseract + Poppler
- Tesseract: https://github.com/tesseract-ocr/tesseract
- Poppler (for pdf2image): Add its bin/ path to system PATH

## ▶️ Run the App
python app.py

## 📂 Project Structure
├── app.py
├── agents/
│   ├── ingestion_agent.py
│   ├── retrieval_agent.py
│   └── llm_response_agent.py
├── templates/
│   └── index.html
├── static/ (optional assets)
├── utils/
│   └── mcp.py
├── .env
└── requirements.txt

## 🧪 Supported Formats
- PDF (text or scanned)
- DOCX (Word)
- CSV (tabular)
- TXT / MD (plain text)
- PPTX (presentation)

## 💡 Credits
Built by SV Rajesh using LangChain, Flask, OpenAI 🛸
