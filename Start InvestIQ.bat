@echo off
title InvestIQ - Starting...
color 0A

echo.
echo  ================================
echo   InvestIQ - AI Stock Analysis
echo  ================================
echo.

:: Build frontend once if not already built
if not exist "C:\pollin-ai\frontend\dist\index.html" (
    echo  Building app for the first time...
    echo  This takes 1-2 minutes but only happens ONCE.
    echo.
    cd /d C:\pollin-ai\frontend
    call npm run build
    echo.
    echo  Build complete!
    echo.
)

:: Start backend silently in background
echo  Starting InvestIQ...
start /min "InvestIQ-Server" cmd /c "cd /d C:\pollin-ai\backend && venv\Scripts\activate && uvicorn main:app --host 0.0.0.0 --port 8000"

:: Poll until server is ready (check every half second)
echo  Waiting for server...
:waitloop
ping -n 1 localhost > nul 2>&1
curl -s http://localhost:8000 > nul 2>&1
if %errorlevel% neq 0 (
    timeout /t 1 /nobreak > nul
    goto waitloop
)

:: Server is ready! Open browser instantly
echo  Opening InvestIQ...
start "" "http://localhost:8000"

:: Close this window
exit
