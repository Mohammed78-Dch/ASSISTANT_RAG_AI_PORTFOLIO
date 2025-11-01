# 🤖 AI Portfolio RAG Assistant

An intelligent **Retrieval-Augmented Generation (RAG)** system for analyzing and querying portfolio/CV documents using natural language. Built with **FastAPI**, **Sentence Transformers**, **FAISS**, and **Google Gemini** for semantic search and intelligent information retrieval.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📑 Table of Contents

1. [Overview](#-overview)
2. [Key Features](#-key-features)
3. [System Architecture](#-system-architecture)
4. [Project Structure](#-project-structure)
5. [Installation Guide](#-installation-guide)
6. [Configuration](#-configuration)
7. [Usage](#-usage)
8. [RAG Pipeline](#-rag-pipeline)
9. [API Documentation](#-api-documentation)
10. [Evaluation & Metrics](#-evaluation--metrics)
11. [Roadmap](#-roadmap)
12. [Contributing](#-contributing)
13. [License](#-license)

---

## 🌟 Overview

The **AI Portfolio RAG Assistant** is an intelligent application that:
- Provides a **REST API** for CV/portfolio document analysis
- Generates semantic embeddings for fast and accurate information retrieval
- Answers natural language questions about professional backgrounds
- Extracts and highlights skills, projects, and experiences
- Provides structured insights and summaries via API endpoints

Unlike traditional keyword-based search, this assistant uses **semantic understanding** through RAG (Retrieval-Augmented Generation) to comprehend context and provide accurate, relevant answers.

---

## ⚡ Key Features

### 🎯 Intelligent Document Processing
- **Pre-structured CV Support**: Works with structured text format resumes
- **Semantic Chunking**: Intelligent text splitting that preserves context
- **Context-Aware Retrieval**: FAISS-powered vector similarity search

### 🔍 Advanced RAG Pipeline
- **Vector Embeddings**: Using Sentence Transformers for semantic understanding
- **FAISS Index**: Fast similarity search with optimized indexing
- **Top-K Retrieval**: Configurable relevant chunk retrieval
- **Persistent Storage**: Pre-computed embeddings for instant responses

### 🌐 RESTful API
- **FastAPI Backend**: High-performance async API server
- **Chat Endpoint**: Conversational interface for CV queries
- **Flexible Integration**: Easy integration with any frontend
- **Auto Documentation**: Interactive Swagger UI included

### 🧠 Powered by Google Gemini
- **Advanced LLM**: Google Gemini 2.0 Flash for generation
- **Contextual Answers**: Grounded in retrieved CV content
- **Structured Responses**: Professional formatting and organization

### 📊 Evaluation & Testing
- **Built-in Metrics**: Retrieval precision and answer quality evaluation
- **Performance Testing**: Response time and accuracy measurements
- **Quality Assurance**: Faithfulness and relevance scoring

---

## 🏗️ System Architecture

```
┌─────────────────────┐
│   Frontend App      │
│   (React/Vue/etc)   │
└──────────┬──────────┘
           │ HTTP/REST
           ▼
┌─────────────────────┐         ┌──────────────────┐
│   FastAPI Server    │ ◄─────► │  Gemini AI LLM   │
│   (main.py)         │   API   │  (Generator)     │
└──────────┬──────────┘         └──────────────────┘
           │
           ▼
┌─────────────────────┐
│   Chat Handler      │
│   (chat.py)         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Prompt Generator   │
│  (prompt_gen.py)    │
└──────────┬──────────┘
           │
           ├────────► ┌──────────────────┐
           │          │  Retrieval       │
           │          │  (retrieval.py)  │
           │          └─────────┬────────┘
           │                    │
           │                    ▼
           │          ┌──────────────────┐
           │          │  FAISS Index     │
           │          │  (faiss_index)   │
           │          └─────────┬────────┘
           │                    │
           ▼                    ▼
┌─────────────────────┐  ┌──────────────────┐
│  Text Chunking      │  │  Embeddings      │
│  (chunking.py)      │  │  (embedding.py)  │
└─────────────────────┘  └──────────────────┘
           │                    │
           └────────┬───────────┘
                    ▼
           ┌──────────────────┐
           │  CV Document     │
           │  (data/*.txt)    │
           └──────────────────┘
```

---

## 📁 Project Structure

```plaintext
ASSISTANT_RAG_AI_PORTFOLIO/
├── data/                          # Resume data storage
│   └── structured_cv.txt          # Structured CV document
│
├── embeddings/                    # Pre-computed embeddings
│   ├── faiss_index.bin           # FAISS vector index
│   └── chunks.json               # Text chunks metadata
│
├── src/                          # Source code
│   ├── main.py                   # 🚀 FastAPI server & endpoints
│   ├── chat.py                   # 💬 Chat logic & model integration
│   ├── chunking.py               # ✂️ Text chunking strategy
│   ├── config.py                 # ⚙️ Configuration & environment vars
│   ├── embedding.py              # 🔢 Embedding generation + FAISS
│   ├── evaluate.py               # 📊 Evaluation metrics
│   ├── convert.py                # 🔄 Document format conversion
│   ├── formatter.py              # 📝 Response formatting
│   ├── prompt_gen.py             # 🎯 Prompt engineering
│   ├── retrieval.py              # 🔍 FAISS retrieval logic
│   └── requirements.txt          # Python dependencies
│
├── frontend/                      # React.js frontend
│   ├── public/
│   ├── src/
│   │   ├── App.jsx               # Root component
│   │   ├── index.js              # Entry point
│   │   ├── index.css             # Global styles
│   │   └── components/           # React components (optional)
│   ├── package.json              # Node dependencies
│   ├── .env                      # Frontend environment variables
│   └── README.md                 # Frontend documentation
│
├── .env                          # Backend environment variables (API keys)
└── README.md                     # Project documentation
```

---

## 🚀 Installation Guide

### Prerequisites

- **Python 3.8+**
- **Node.js 16+** and **npm/yarn**
- **Git**
- **Google Gemini API Key** ([Get it here](https://makersuite.google.com/app/apikey))

---

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ASSISTANT_RAG_AI_PORTFOLIO.git
cd ASSISTANT_RAG_AI_PORTFOLIO
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

3. **Install dependencies**
```bash
cd src
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the root directory:

```bash
# .env file
GEMINI_API_KEY=your_gemini_api_key_here
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
MODEL=gemini-2.0-flash-exp
INDEX_PATH=embeddings/faiss_index.bin
CHUNKS_PATH=embeddings/chunks.json
DATA_PATH=data/structured_cv.txt
CHUNK_SIZE=200
CHUNK_OVERLAP=50
TOP_K=5

```

5. **Prepare your CV document**

Place your structured CV in `data/structured_cv.txt`. Format example:

```text
# Professional Summary
Experienced AI Engineer with 5+ years in machine learning...

## Skills
- Python, TensorFlow, PyTorch
- NLP, Computer Vision
- AWS, Docker, Kubernetes

## Experience
### Senior ML Engineer | Tech Corp | 2021-Present
- Developed RAG systems...
```

6. **Generate embeddings (First time only)**
```bash
python embedding.py
```

This will create:
- `embeddings/faiss_index.bin`
- `embeddings/chunks.json`

7. **Run the FastAPI server**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

8. **Access API Documentation**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

### Frontend Setup (React.js)

1. **Navigate to frontend directory**
```bash
cd ../frontend
```

2. **Install dependencies**
```bash
npm install
# or
yarn install
```

4. **Start development server**
```bash
npm run dev
# or
yarn start
```

The frontend will open automatically at `http://localhost:5173`

### Running Both (Backend + Frontend)

**Option 1: Two Terminals**

Terminal 1 (Backend):
```bash
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

**Option 2: Using `concurrently` (Recommended)**

Install concurrently in the root directory:
```bash
npm install -g concurrently
```

Add to root `package.json`:
```json
{
  "scripts": {
    "start:backend": "cd src && uvicorn main:app --reload",
    "start:frontend": "cd frontend && npm start",
    "start": "concurrently \"npm run start:backend\" \"npm run start:frontend\""
  }
}
```

Then run:
```bash
npm start
```

---

## ⚙️ Configuration

### Environment Variables (`.env`)

#### Backend Configuration (`/.env`)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | - | ✅ Yes |
| `EMBEDDING_MODEL` | Sentence transformer model | `all-MiniLM-L6-v2` | ❌ No |
| `MODEL` | Gemini model name | `gemini-2.0-flash-exp` | ❌ No |
| `INDEX_PATH` | FAISS index file path | `embeddings/faiss_index.bin` | ❌ No |
| `CHUNKS_PATH` | Chunks JSON file path | `embeddings/chunks.json` | ❌ No |
| `DATA_PATH` | CV document path | `data/structured_cv.txt` | ❌ No |
| `CHUNK_SIZE` | Max tokens per chunk | `200` | ❌ No |
| `CHUNK_OVERLAP` | Overlap between chunks | `50` | ❌ No |
| `TOP_K` | Number of chunks to retrieve | `5` | ❌ No |
| `HOST` | API server host | `0.0.0.0` | ❌ No |
| `PORT` | API server port | `8000` | ❌ No |
| `CORS_ORIGINS` | Allowed CORS origins | `*` | ❌ No |

#### Frontend Configuration (`frontend/.env`)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `REACT_APP_API_URL` | Backend API base URL | `http://localhost:8000` | ✅ Yes |
| `REACT_APP_API_TIMEOUT` | Request timeout (ms) | `30000` | ❌ No |

### Chunking Strategy

The system uses semantic chunking with overlap to preserve context:
- **Chunk Size**: 200 tokens (adjustable)
- **Overlap**: 50 tokens (prevents information loss)
- **Section-aware**: Respects document structure

---

## 📖 Usage

### 1. Start the Application

**Backend (Terminal 1):**
```bash
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```

---

### 2. Using the Web Interface

Once the frontend is running, you can:

1. **Open the chat interface** at URL
1. **Upload the cv** in the chat input
2. **Ask questions** about the CV in the chat input
3. **View responses** with formatted markdown
4. **See conversation history** in the chat window


---

### 4. Example Queries

**Skills & Expertise:**
```json
{
  "message": "What programming languages do I know?",
  "conversation_id": null
}
```

**Experience:**
```json
{
  "message": "Summarize my work experience",
  "conversation_id": null
}
```

**Projects:**
```json
{
  "message": "What machine learning projects have I built?",
  "conversation_id": null
}
```

**General:**
```json
{
  "message": "Give me a professional summary",
  "conversation_id": null
}
```


---


### Metrics Tracked

| Metric | Description | Target |
|--------|-------------|--------|
| **Retrieval Precision** | Accuracy of retrieved chunks | > 0.90 |
| **Answer Faithfulness** | Groundedness in source context | > 0.95 |
| **Context Relevance** | Relevance of retrieved information | > 0.88 |
| **Response Time** | End-to-end API latency | < 2s |
| **Chunk Coverage** | % of CV content searchable | > 0.95 |

### Sample Evaluation Output

```
=== RAG System Evaluation ===
Retrieval Precision: 0.94
Answer Faithfulness: 0.98
Context Relevance: 0.91
Avg Response Time: 1.6s
Chunk Coverage: 0.97
API Success Rate: 99.8%
```


---

## 🗺️ Roadmap

### Phase 1: Core Features ✅
- [x] FastAPI REST API implementation
- [x] Semantic chunking and FAISS indexing
- [x] Google Gemini integration
- [x] Retrieval and generation pipeline
- [x] Evaluation framework

### Phase 2: Enhancements 🚧
- [ ] Multi-document support (multiple CVs)
- [ ] File upload endpoint (PDF/DOCX)
- [ ] Real-time streaming responses (SSE)
- [ ] Conversation history management
- [ ] Enhanced prompt templates
- [ ] Caching layer (Redis)

### Phase 3: Advanced Features 📅
- [ ] Skills gap analysis endpoint
- [ ] Job description matching API
- [ ] Resume scoring service
- [ ] Multi-language support
- [ ] Vector database integration (Pinecone/Weaviate)
- [ ] Authentication & rate limiting
- [ ] Docker containerization
- [ ] Cloud deployment (AWS/GCP)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit** your changes
   ```bash
   git commit -m 'Add AmazingFeature'
   ```
4. **Push** to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Add type hints to function signatures
- Write docstrings for all functions
- Add unit tests for new features
- Update API documentation
- Test endpoints with Swagger UI

### Running Tests

```bash
cd src
pytest tests/
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Google Gemini](https://ai.google.dev/) for the powerful LLM API
- [Sentence Transformers](https://www.sbert.net/) for semantic embeddings
- [FAISS](https://github.com/facebookresearch/faiss) for efficient vector search
- [FastAPI](https://fastapi.tiangolo.com/) for the high-performance API framework

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FAISS Documentation](https://faiss.ai/)
- [Sentence Transformers Documentation](https://www.sbert.net/)
- [Google Gemini API Guide](https://ai.google.dev/docs)

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star!**

Built with ❤️ for intelligent portfolio querying

</div>