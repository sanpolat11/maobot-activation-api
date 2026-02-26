@echo off
title MaoBot API (CALISIYOR - BU PENCEREYI KAPATMA!)
color 0A
cd /d "%~dp0\.."

echo ================================
echo   MaoBot API BASLATILIYOR...
echo ================================
echo.
echo API Adresi: http://192.168.1.178:8080
echo.
echo ONEMLI: Bu pencereyi KAPATMA!
echo API bu pencerede calisacak.
echo.
echo ================================
echo.

python app.py

pause
