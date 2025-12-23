@echo off
echo Testing React frontend build...
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed. Please install Node.js first.
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: npm is not installed. Please install npm first.
    pause
    exit /b 1
)

echo Installing dependencies...
npm install

echo.
echo Building the application...
npm run build

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS: Build completed successfully!
    echo The built files are in the dist/ directory.
    echo.
    echo To start the development server, run:
    echo npm run dev
    echo.
    echo To preview the production build, run:
    echo npm run preview
) else (
    echo.
    echo ERROR: Build failed. Please check the error messages above.
)

echo.
pause