# 📊 RAG Pipeline Diagram

## ASCII Diagram

```
┌─────────────────┐
│   PDF Upload    │
│   (Multiple)    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Text Extraction│
│   (PyPDF)       │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│    Chunking     │
│  (600 chars)    │
│  (80 overlap)   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   Embedding     │
│ (Gemini Embed)  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   ChromaDB      │
│ (Vector Store)  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   Retriever     │
│   (Top-K=4)     │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Gemini Flash or
 ollama local LLm  │
│ (Generation)    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   Final Answer  │
│ (Concise + Src) │
└─────────────────┘
```

## Mermaid Diagram

```mermaid
graph TD
    A[PDF Upload] --> B[Text Extraction<br/>(PyPDF)]
    B --> C[Chunking<br/>(600 chars, 80 overlap)]
    C --> D[Embedding<br/>(Gemini Embeddings)]
    D --> E[ChromaDB<br/>(Vector Storage)]
    E --> F[Retriever<br/>(Top-K=4)]
    F --> G[Gemini Flash<br/>(Generation)]
    G --> H[Final Answer<br/>(Concise + Sources)]
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#e8f5e8
    style D fill:#fff3e0
    style E fill:#fce4ec
    style F fill:#e0f2f1
    style G fill:#fff8e1
    style H fill:#f1f8e9
```

## Performance Characteristics

- **Chunk Size**: 600 characters
- **Overlap**: 80 characters
- **Top-K**: 4 similar chunks retrieved
- **Model**: gemini-2.0-flash
- **Response Target**: < 2 seconds
- **Embedding Model**: models/embedding-001

## Key Optimizations

1. **Caching**: Embeddings cached automatically
2. **Minimal Dependencies**: Only essential packages
3. **Fast LLM**: Gemini Flash for speed
4. **Efficient Chunking**: Optimized size and overlap
5. **Simple Retrieval**: No complex rerankers