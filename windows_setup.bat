@echo off
REM Complete setup for Windows Local RAG Debate System

echo ================================================================
echo LOCAL RAG DEBATE SYSTEM - WINDOWS SETUP
echo ================================================================
echo.

echo 1. Installing Python dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo 2. Setting up Ollama...
echo Please download Ollama from https://ollama.com/download/windows
echo Install it, then press Enter to continue...
pause

echo.
echo 3. Downloading Mistral model (this may take several minutes)...
ollama pull mistral

if %errorlevel% neq 0 (
    echo ❌ Failed to download Ollama model
    echo Please ensure Ollama is properly installed and running
    pause
    exit /b 1
)

echo.
echo 4. Creating data directory...
if not exist "data" mkdir data

echo.
echo 5. Setup complete! Next steps:
echo    - Add PDF files to the 'data' folder
echo    - Run: python create_database.py
echo    - Generate debates: python query_debate.py "Your topic"
echo.
echo Press any key to continue...
pause