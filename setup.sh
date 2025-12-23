#!/bin/bash
# Complete setup for Linux/Mac Local RAG Debate System

echo "============================================================"
echo "LOCAL RAG DEBATE SYSTEM - LINUX/MAC SETUP"
echo "============================================================"
echo

echo "1. Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo
echo "2. Setting up Ollama..."

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    
    # Detect OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Installing Ollama for Linux..."
        curl -fsSL https://ollama.com/install.sh | sh
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Installing Ollama for macOS..."
        echo "Please download Ollama from https://ollama.com/download/mac"
        echo "Or install via Homebrew: brew install ollama"
        read -p "Press Enter after installing Ollama..."
    else
        echo "Unknown OS. Please install Ollama manually from https://ollama.com"
        read -p "Press Enter after installing Ollama..."
    fi
else
    echo "Ollama already installed"
fi

echo
echo "3. Downloading Mistral model (this may take several minutes)..."
ollama pull mistral

if [ $? -ne 0 ]; then
    echo "❌ Failed to download Ollama model"
    echo "Please ensure Ollama is properly installed and running"
    exit 1
fi

echo
echo "4. Creating data directory..."
mkdir -p data

echo
echo "5. Setup complete! Next steps:"
echo "   - Add PDF files to the 'data' folder"
echo "   - Run: python create_database.py"
echo "   - Generate debates: python query_debate.py \"Your topic\""
echo
echo "Press Enter to continue..."
read