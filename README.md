# 📚 NotebookLM-style RAG Application

A minimal, high-performance RAG application similar to NotebookLM, built with Python, Google Gemini Flash, and ChromaDB.

## ⚡ Features

- **🚀 Ultra-fast**: Optimized for < 2 second response times
- **🧠 Accurate**: Google Gemini Flash for concise, structured answers
- **🧼 Clean**: Minimal dependencies, no bloat
- **📊 FastAPI**: REST API for backend integration
- **🎨 Streamlit**: Simple, intuitive UI
- **📁 PDF Support**: Upload and index multiple PDFs
- **🔍 Smart Retrieval**: Top-K=4 similarity search with ChromaDB

## 🛠️ Tech Stack

- **Python 3.11+**
- **FastAPI** - Backend API
- **Streamlit** - Frontend UI
- **LangChain** - RAG orchestration
- **Google Gemini Flash** - LLM (model: gemini-2.0-flash)
- **ChromaDB** - Vector database
- **PyPDF** - PDF processing

## 📋 Requirements

- Google API Key for Gemini Flash
- Python 3.11+
- No Docker required

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variable

```bash
export GOOGLE_API_KEY=your_api_key_here
```

### 3. Run the Application

**Option A: Streamlit UI (Recommended)**
```bash
streamlit run app.py
```

**Option B: FastAPI Backend**
```bash
python api.py
```

**Option C: Both (Development)**
```bash
# Terminal 1: Run API
uvicorn api:app --reload

# Terminal 2: Run Streamlit
streamlit run app.py
```

### 4. Use the Application

1. **Upload PDFs**: Use the sidebar to upload one or more PDF files
2. **Ask Questions**: Type your question in the chat interface
3. **Get Answers**: Receive concise, structured responses with source citations

## 🏗️ Architecture

### File Structure
```
rag-app/
├── app.py                # Streamlit UI
├── rag.py                # RAG logic (load, chunk, embed, retrieve)
├── api.py                # FastAPI endpoint for chat
├── requirements.txt      # Dependencies
└── README.md            # This file
```

### RAG Pipeline Flow

```
PDF Upload
   ↓
Text Extraction (PyPDF)
   ↓
Chunking (600 chars, 80 overlap)
   ↓
Embedding (Gemini embeddings)
   ↓
ChromaDB (persistent storage)
   ↓
Retriever (Top-K=4)
   ↓
Gemini Flash (generation)
   ↓
Final Answer (concise + sources)
```

## 🔧 Configuration

### Performance Optimizations

- **Chunk Size**: 600 characters
- **Overlap**: 80 characters
- **Top-K**: 4 similar chunks
- **Temperature**: 0.1 (for concise answers)
- **Max Tokens**: 500 (response limit)

### Caching

- Embeddings are cached automatically
- Vector database persists between sessions
- No re-embedding of existing PDFs

## 📊 API Endpoints

### POST /upload
Upload PDF files for indexing
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "files=@document1.pdf" \
  -F "files=@document2.pdf"
```

### POST /query
Query the RAG system
```bash
curl -X POST "http://localhost:8000/query" \
  -F "question=What is the main topic of these documents?"
```

### GET /documents
List all indexed documents
```bash
curl "http://localhost:8000/documents"
```

### DELETE /clear
Clear the vector database
```bash
curl -X DELETE "http://localhost:8000/clear"
```

## 🎯 Usage Examples

### Streamlit UI
1. Open http://localhost:8501 in your browser
2. Upload PDF files in the sidebar
3. Ask questions in the chat interface
4. View answers with source citations

### API Integration
```python
import requests

# Upload documents
files = [('files', open('doc1.pdf', 'rb')), ('files', open('doc2.pdf', 'rb'))]
response = requests.post('http://localhost:8000/upload', files=files)

# Query
response = requests.post('http://localhost:8000/query', data={'question': 'What is this about?'})
print(response.json())
```

## ⚙️ Environment Variables

- `GOOGLE_API_KEY`: Required for Gemini Flash access


## 🧪 Testing

The application is designed to be minimal and functional:

1. **Functional Testing**: Upload PDFs and verify answers
2. **Performance Testing**: Measure response times (< 2 seconds target)
3. **Integration Testing**: Test API endpoints

## 📈 Performance

- **Response Time**: < 2 seconds (target)
- **Memory Usage**: Minimal (no unnecessary caching)
- **Startup Time**: Fast (minimal dependencies)
- **Scalability**: Single-user focused

## 🤝 Contributing

This is a minimal implementation. For contributions:

1. Keep dependencies minimal
2. Maintain performance focus
3. Preserve simplicity
4. No unnecessary abstraction

---

**Built with ❤️ for fast, accurate, and minimal RAG applications.**