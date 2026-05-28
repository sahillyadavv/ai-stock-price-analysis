@echo off
title InvestIQ - Rebuilding...
color 0B
echo.
echo  Rebuilding InvestIQ frontend...
echo  (Run this whenever you make changes to frontend files)
echo.
cd /d C:\pollin-ai\frontend
call npm run build
echo.
echo  Done! Restart InvestIQ to see changes.
pause
