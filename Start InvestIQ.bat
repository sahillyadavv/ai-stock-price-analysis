@echo off
title InvestIQ - Starting...
color 0A

echo.
echo  ================================
echo   InvestIQ - AI Stock Analysis
echo  ================================
echo.

:: Step 1 - Build frontend (only if not built yet)
if not exist "C:\pollin-ai\frontend\dist" (
    echo  [1/2] Building frontend for fast loading...
    echo  This only happens once, please wait...
    cd /d C:\pollin-ai\frontend
    call npm run build
    echo  Frontend built successfully!
    echo.
) else (
    echo  [1/2] Frontend already built. Skipping...
)

:: Step 2 - Start backend (serves everything)
echo  [2/2] Starting InvestIQ...
start "InvestIQ" cmd /k "cd /d C:\pollin-ai\backend && venv\Scripts\activate && uvicorn main:app --reload"

:: Wait for backend to start
echo  Waiting for server to start...
timeout /t 5 /nobreak > nul

:: Open browser
echo  Opening InvestIQ...
start "" "http://localhost:8000"

echo.
echo  ================================
echo   InvestIQ is running!
echo   Open: http://localhost:8000
echo  ================================
echo.
pause
