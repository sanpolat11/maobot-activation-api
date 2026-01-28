# MaoBot Activation API Başlatma Scripti

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  MaoBot Activation API" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Python kontrolü
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python bulundu: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python bulunamadı!" -ForegroundColor Red
    Write-Host "Python 3.8+ kurulu olmalı: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Requirements kontrolü
Write-Host ""
Write-Host "📦 Paketler kontrol ediliyor..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

# Environment variables
$env:GITHUB_TOKEN = "YOUR_GITHUB_TOKEN_HERE"
$env:API_SECRET = "maobot-secret-2026"

Write-Host "✅ Environment variables ayarlandı" -ForegroundColor Green
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  API Başlatılıyor..." -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "API URL: http://localhost:5000" -ForegroundColor Yellow
Write-Host "API Secret: maobot-secret-2026" -ForegroundColor Yellow
Write-Host ""
Write-Host "Test için yeni terminal aç ve çalıştır:" -ForegroundColor Cyan
Write-Host "  python test_api.py" -ForegroundColor White
Write-Host ""

# API'yi başlat
python app.py
