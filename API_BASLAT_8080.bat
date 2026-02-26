@echo off
title MaoBot Activation API - Port 8080
color 0A

echo ========================================
echo MaoBot Activation API
echo Port: 8080
echo ========================================
echo.

cd /d "%~dp0"

set PORT=8080
python app.py

pause
