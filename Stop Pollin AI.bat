@echo off
title Pollin AI - Stopping...
color 0C

echo.
echo  Stopping Pollin AI servers...
echo.

:: Kill uvicorn (backend)
taskkill /f /im uvicorn.exe > nul 2>&1
taskkill /f /fi "WINDOWTITLE eq Pollin AI - Backend" > nul 2>&1

:: Kill node (frontend)
taskkill /f /fi "WINDOWTITLE eq Pollin AI - Frontend" > nul 2>&1

echo  All servers stopped!
echo.
timeout /t 2 /nobreak > nul
