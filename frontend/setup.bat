@echo off
echo Setting up React frontend for RAG Debate Generator...
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed. Please install Node.js first.
    echo Download from: https://nodejs.org/
    pause
    exit /b 1
)

echo Installing dependencies...
npm install

echo.
echo Setup complete! You can now run the frontend with:
echo npm run dev
echo.
echo The frontend will be available at: http://localhost:3000
echo.
echo Make sure the Flask backend is running on port 5000:
echo python local_rag_debate/app.py
echo.

pause