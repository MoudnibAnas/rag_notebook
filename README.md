# Local RAG Debate Generator

## 🎥 Video Demo
[**Watch My Loom video demo here**](#)

A powerful application that generates structured academic debates from your PDF documents using Retrieval-Augmented Generation (RAG) and local LLMs.

## 🎯 Features

- **Upload PDF documents** and create a knowledge base
- **Generate structured debates** with multiple perspectives
- **Local LLM integration** with Ollama (no API keys required)
- **Web interface** for easy interaction
- **Command-line interface** for automation
- **Clean separation** between backend and frontend

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Ollama** (for local LLMs)
- **Node.js** (for frontend development)

### 1. Install Dependencies

```bash
# Backend dependencies
pip install -r requirements.txt

# Frontend dependencies (optional)
cd frontend
npm install
```

### 2. Install Ollama Model

```bash
# Download a model (recommended: mistral)
ollama pull mistral
```

### 3. Create Database

```bash
# Process PDFs and create vector database
python create_database.py
```

### 4. Start Application

#### Option A: Manual (Recommended for development)
```bash
# Terminal 1: Start backend
cd local_rag_debate
python app.py

# Terminal 2: Start frontend
cd frontend
npm run dev
```

#### Option B: Automated
```bash
# Windows
start_application.bat

# Linux/macOS
./start_application.sh
```

### 5. Access Application

- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:5000 (API server)

## 📁 Project Structure

```
local_rag_debate/
├── local_rag_debate/          # Backend (Flask API)
│   ├── app.py                 # Main Flask application
│   ├── create_database.py     # PDF processing
│   ├── query_debate.py        # Debate generation
│   ├── requirements.txt       # Python dependencies
│   ├── data/                  # PDF documents
│   ├── chroma_db/             # Vector database
│   ├── start_application.bat  # Startup script
│   └── SETUP_GUIDE.md         # Complete setup guide
└── frontend/                  # Frontend (React)
    ├── src/
    │   ├── components/
    │   │   ├── OriginalInterface.tsx    # Main debate interface (exact replica of Python HTML)
    │   │   └── DebateInterface.tsx     # Alternative Material-UI interface
    │   ├── App.tsx           # Main app component
    │   └── index.css         # Global styles
    ├── package.json          # Frontend dependencies
    ├── vite.config.ts        # Build configuration
    ├── SETUP.md              # Frontend setup guide
    └── README.md             # Frontend documentation
```
## 🙏 Acknowledgments

- **LangChain** - For RAG framework
- **ChromaDB** - For vector database
- **Ollama** - For local LLM integration
- **React** - For frontend framework
- **Material-UI** - For UI components

=
