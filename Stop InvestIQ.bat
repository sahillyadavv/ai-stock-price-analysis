@echo off
title InvestIQ - Stopping...
color 0C
echo.
echo  Stopping InvestIQ...
taskkill /f /im uvicorn.exe > nul 2>&1
taskkill /f /fi "WINDOWTITLE eq InvestIQ" > nul 2>&1
echo  InvestIQ stopped!
timeout /t 2 /nobreak > nul
