@echo off
REM Quick start script for AI Meeting Host (Windows)

echo 🎙️ AI Meeting Host - Quick Start
echo ================================
echo.

REM Check if .env exists
if not exist .env (
    echo ⚠️  .env file not found!
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo ⚠️  Please edit .env and add your GITHUB_TOKEN
    echo Then run this script again.
    exit /b 1
)

REM Check if GITHUB_TOKEN is set
findstr /C:"your_github_token_here" .env >nul
if %errorlevel% equ 0 (
    echo ⚠️  Please set your GITHUB_TOKEN in .env file
    echo Get your token from: https://github.com/settings/tokens
    exit /b 1
)

echo ✅ Environment configured
echo.

echo 🚀 Starting backend server...
start cmd /k "cd backend && python main.py"

timeout /t 3 /nobreak >nul

echo 🚀 Starting frontend...
start cmd /k "cd frontend && npm start"

echo.
echo ================================
echo ✅ AI Meeting Host is starting!
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Two windows will open for backend and frontend
echo Close those windows to stop the services
echo ================================
echo.
pause
