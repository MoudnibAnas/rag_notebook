# Ollama Setup Guide

To get the full LLM response with debate generation, you need to install and configure Ollama.

## Installation Steps:

### 1. Download and Install Ollama
- Go to [ollama.com](https://ollama.com)
- Download Ollama for your operating system
- Install and run the application

### 2. Download a Model
Open a terminal/command prompt and run:
```bash
ollama pull mistral
```
Alternative models you can use:
```bash
ollama pull llama2
ollama pull mixtral
ollama pull neural-chat
```

### 3. Verify Installation
Test that Ollama is working:
```bash
ollama list
```
Should show your downloaded models.

### 4. Test the System
After installing Ollama, the debate generation should work with full LLM responses.

## Alternative: Use the Simplified Version

If you cannot install Ollama, the system will automatically fall back to a simplified response that still provides structured debate format based on your documents.

## Troubleshooting

### Ollama Not Found
If you get "Error connecting to Ollama", ensure:
1. Ollama application is running
2. The model is downloaded
3. You have internet access for the initial download

### Slow Response
Debate generation may take 1-2 minutes with local LLMs. This is normal for complex document analysis.

### Memory Issues
If you get memory errors, try:
1. Using a smaller model (like `mistral` instead of `llama2`)
2. Closing other applications to free memory
3. Using simpler topics for faster processing

## Expected Response Format

With Ollama installed, you should get responses like:
```
PERSPECTIVE A: [Detailed analysis with citations from documents]
- Point 1 with evidence [Source: document.pdf, Page 3]
- Point 2 with evidence [Source: document2.pdf, Page 1]

PERSPECTIVE B: [Counter-argument with citations]
- Point 1 with evidence [Source: document.pdf, Page 5]
- Point 2 with evidence [Source: document3.pdf, Page 2]

NEUTRAL SUMMARY: [Balanced synthesis]
```

Without Ollama, you'll get a simplified template response.