
![Uploading Rag_Archi.png…]()

# Local RAG Debate Generator

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

## 🎨 Interface Options

### OriginalInterface (Default)

The `OriginalInterface` component is an exact replica of the HTML interface that was previously embedded in the Python backend. It provides:

- **Sidebar with notebook management**
- **Document upload and management**
- **Real-time chat interface for debates**
- **Loading states and error handling**
- **Responsive design**

### DebateInterface (Alternative)

A Material-UI based interface with:
- **Modern Material-UI components**
- **Enhanced user experience**
- **Professional design**
- **Better accessibility**

## 📊 Usage Examples

### Web Interface

1. **Upload Documents**: Drag and drop PDF files
2. **Create Database**: Automatically processes uploaded files
3. **Generate Debates**: Enter topics and get structured debates
4. **Export Results**: Download debate transcripts

### Command Line

```bash
# Generate a debate
python query_debate.py "Should AI replace human teachers?"

# Generate with custom parameters
python query_debate.py "Renewable energy vs fossil fuels" --model mistral --temperature 0.7
```

### API Usage

```bash
# Get document list
curl http://localhost:5000/api/documents

# Generate debate
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "Should AI replace human teachers?"}'

# Upload documents
curl -X POST http://localhost:5000/api/upload \
  -F "files=@document1.pdf" \
  -F "files=@document2.pdf"
```

## 🔧 Configuration

### Backend Configuration

Edit `app.py` to configure:
- **Port**: Change the server port
- **Model**: Specify different Ollama models
- **Timeout**: Adjust generation timeouts
- **Database**: Configure vector database settings

### Frontend Configuration

Edit `vite.config.ts` to configure:
- **Proxy**: Backend server address
- **Build settings**: Production optimizations
- **Environment variables**: API endpoints

## 🛠️ Development

### Backend Development

```bash
# Start backend with auto-reload
python app.py

# Debug mode
export FLASK_ENV=development
python app.py
```

### Frontend Development

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Adding New Features

1. **Backend**: Add new endpoints in `app.py`
2. **Frontend**: Create new components in `src/components/`
3. **Database**: Modify `create_database.py` for new document types
4. **API**: Update `query_debate.py` for new generation features

## 🐛 Troubleshooting

### Common Issues

1. **Ollama not found**
   - Ensure Ollama is installed and running
   - Check if the model is downloaded: `ollama list`

2. **Port already in use**
   - Change the port in `app.py` or `vite.config.ts`
   - Kill existing processes using the port

3. **PDF processing errors**
   - Check PDF file integrity
   - Ensure PDFs are not password protected
   - Verify file permissions

4. **Frontend-backend communication**
   - Check if backend is running on port 5000
   - Verify proxy configuration in `vite.config.ts`
   - Check CORS settings in backend

### Performance Optimization

1. **Large PDFs**: Split large documents into smaller chunks
2. **Multiple models**: Use different models for different tasks
3. **Caching**: Implement result caching for frequently asked topics
4. **Database**: Optimize vector database settings for your use case

## 📚 API Reference

### GET /api/documents

Get list of uploaded documents.

**Response:**
```json
{
  "success": true,
  "documents": [
    {
      "name": "document.pdf",
      "size": 1024000,
      "uploaded_at": "2023-12-23T10:00:00Z"
    }
  ]
}
```

### POST /api/upload

Upload PDF files.

**Request:**
- Form data with `files` field containing PDF files

**Response:**
```json
{
  "success": true,
  "message": "Files uploaded successfully"
}
```

### POST /api/generate

Generate a debate on a topic.

**Request:**
```json
{
  "topic": "Should AI replace human teachers?"
}
```

**Response:**
```json
{
  "success": true,
  "result": "Generated debate content..."
}
```

### POST /api/create_database

Create or update the vector database.

**Response:**
```json
{
  "success": true,
  "message": "Database created successfully"
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **LangChain** - For RAG framework
- **ChromaDB** - For vector database
- **Ollama** - For local LLM integration
- **React** - For frontend framework
- **Material-UI** - For UI components

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the API documentation

---

**Note**: This application requires significant computational resources for optimal performance. Ensure your system meets the requirements for running local LLMs.
