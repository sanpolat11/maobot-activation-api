@echo off
title MaoBot API Durdur
color 0C
echo ================================
echo   MaoBot API Durduruluyor...
echo ================================
echo.

taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM pythonw.exe >nul 2>&1

echo.
echo ================================
echo   API DURDURULDU!
echo ================================
echo.
pause
