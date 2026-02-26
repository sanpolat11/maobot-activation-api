@echo off
title MaoBot API Baslat
color 0A
echo ================================
echo   MaoBot API Baslatiliyor...
echo ================================
echo.

cd /d "%~dp0\.."
start /B pythonw app.py

timeout /t 5 /nobreak >nul

echo.
echo ================================
echo   API BASLATILDI!
echo ================================
echo.
echo API Adresi: http://192.168.1.178:8080
echo.
echo 5 saniye bekle, sonra bot'u baslat!
echo Bu pencereyi kapatabilirsin.
echo.
pause
