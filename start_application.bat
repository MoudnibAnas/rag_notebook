@echo off
REM Local RAG Debate Generator - Startup Script

echo ================================================================
echo LOCAL RAG DEBATE GENERATOR
echo ================================================================
echo.
echo This script will start both the backend and frontend.
echo.
echo Requirements:
echo - Python 3.8+ with pip
echo - Node.js 16+ with npm
echo - Ollama installed with Mistral model
echo.
echo Make sure you have:
echo 1. Installed Python dependencies: pip install -r requirements.txt
echo 2. Installed Node.js dependencies: cd frontend && npm install
echo 3. Downloaded Ollama model: ollama pull mistral
echo.

pause

echo.
echo Starting Backend (Flask)...
echo Backend will run on http://localhost:5000
echo.

REM Start backend in new window
start "Local RAG Backend" cmd /k "cd /d %~dp0 && python app.py"

echo Backend started. Waiting 5 seconds...
timeout /t 5 /nobreak >nul

echo.
echo Starting Frontend (React)...
echo Frontend will run on http://localhost:3000
echo.

REM Start frontend in new window
start "Local RAG Frontend" cmd /k "cd /d %~dp0\frontend && npm run dev"

echo.
echo ================================================================
echo APPLICATION STARTED
echo ================================================================
echo.
echo Backend: http://localhost:5000 (API server)
echo Frontend: http://localhost:3000 (User interface)
echo.
echo The backend will automatically redirect to the frontend.
echo.
echo To access the application:
echo 1. Open your browser
echo 2. Go to http://localhost:3000
echo.
echo To stop the application:
echo 1. Close the backend window (Flask server)
echo 2. Close the frontend window (React dev server)
echo.
echo Press any key to exit this window...
pause >nul