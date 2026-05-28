@echo off
title Pollin AI - Starting...
color 0A

echo.
echo  ================================
echo   Pollin AI - Stock Analysis App
echo  ================================
echo.

:: Start Backend
echo  [1/3] Starting Backend...
start "Pollin AI - Backend" cmd /k "cd /d C:\pollin-ai\backend && venv\Scripts\activate && uvicorn main:app --reload"

:: Wait longer for backend
echo  [2/3] Waiting for backend (8 seconds)...
timeout /t 8 /nobreak > nul

:: Start Frontend
echo  [3/3] Starting Frontend...
start "Pollin AI - Frontend" cmd /k "cd /d C:\pollin-ai\frontend && npm run dev"

:: Wait longer for frontend to compile
echo.
echo  Waiting for frontend to compile (15 seconds)...
timeout /t 15 /nobreak > nul

:: Try port 5173 first, then 5175
echo  Opening browser...
start "" "http://localhost:5173"
timeout /t 2 /nobreak > nul
start "" "http://localhost:5175"

echo.
echo  ================================
echo   Pollin AI is now running!
echo   Try: http://localhost:5173
echo   Or:  http://localhost:5175
echo  ================================
echo.
pause
