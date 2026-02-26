@echo off
title MaoBot API Kontrol
color 0B
echo ================================
echo   MaoBot API Kontrol
echo ================================
echo.

curl -s http://192.168.1.178:8080/health >nul 2>&1

if %errorlevel% equ 0 (
    echo [OK] API CALISIYOR!
    echo.
    echo API Adresi: http://192.168.1.178:8080
    echo Durum: Aktif
    echo.
    echo Bot'u baslatabilirsin!
) else (
    echo [HATA] API CALISMIYOR!
    echo.
    echo API'yi baslatmak icin "API_BASLAT.bat" dosyasina cift tikla.
)

echo.
echo ================================
pause
