@echo off
title TalentPulse AI — Local Server (Port 5000)
echo =======================================================
echo   TalentPulse AI: Starting Local Server on Port 5000...
echo   Open: http://localhost:5000/ui
echo =======================================================
echo.
cd /d "%~dp0"
python run.py %*
pause
