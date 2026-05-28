@echo off
title InvestIQ - Starting...
color 0A

echo.
echo  ================================
echo   InvestIQ - AI Stock Analysis
echo  ================================
echo.

:: Start Backend
echo  [1/3] Starting Backend...
start "InvestIQ - Backend" cmd /k "cd /d C:\pollin-ai\backend && venv\Scripts\activate && uvicorn main:app --reload"

:: Wait for backend
echo  [2/3] Waiting for backend (8 seconds)...
timeout /t 8 /nobreak > nul

:: Start Frontend
echo  [3/3] Starting Frontend...
start "InvestIQ - Frontend" cmd /k "cd /d C:\pollin-ai\frontend && npm run dev"

:: Wait for frontend to compile
echo.
echo  Waiting for frontend to compile (15 seconds)...
timeout /t 15 /nobreak > nul

:: Open browser
echo  Opening InvestIQ...
start "" "http://localhost:5173"
timeout /t 2 /nobreak > nul
start "" "http://localhost:5175"

echo.
echo  ================================
echo   InvestIQ is now running!
echo   Try: http://localhost:5173
echo   Or:  http://localhost:5175
echo  ================================
echo.
pause
