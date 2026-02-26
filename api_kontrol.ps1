# API Kontrol ve Başlatma Scripti
# Kullanım: PowerShell'de sağ tık -> "Run with PowerShell"

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  MaoBot API Kontrol Scripti" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# API'nin çalışıp çalışmadığını kontrol et
Write-Host "[1/3] API durumu kontrol ediliyor..." -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri "http://192.168.1.178:8080/health" -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
    
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ API ÇALIŞIYOR!" -ForegroundColor Green
        Write-Host ""
        Write-Host "API Bilgileri:" -ForegroundColor Cyan
        Write-Host "  - URL: http://192.168.1.178:8080" -ForegroundColor White
        Write-Host "  - Durum: Aktif" -ForegroundColor Green
        Write-Host "  - Port: 8080" -ForegroundColor White
        Write-Host ""
        Write-Host "Bot'u başlatabilirsin!" -ForegroundColor Green
        
        # Python process bilgisi
        $pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
        if ($pythonProcesses) {
            Write-Host ""
            Write-Host "Çalışan Python Process'leri:" -ForegroundColor Cyan
            $pythonProcesses | ForEach-Object {
                Write-Host "  - PID: $($_.Id) | Memory: $([math]::Round($_.WorkingSet64/1MB, 2)) MB" -ForegroundColor White
            }
        }
    }
}
catch {
    Write-Host "❌ API ÇALIŞMIYOR!" -ForegroundColor Red
    Write-Host ""
    Write-Host "[2/3] API başlatılıyor..." -ForegroundColor Yellow
    
    # API'yi başlat
    try {
        $scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
        $vbsPath = Join-Path $scriptPath "start_api_background.vbs"
        
        if (Test-Path $vbsPath) {
            Start-Process -FilePath "wscript.exe" -ArgumentList "`"$vbsPath`"" -WindowStyle Hidden
            Write-Host "✅ API başlatma komutu gönderildi!" -ForegroundColor Green
            Write-Host ""
            Write-Host "[3/3] API'nin başlaması bekleniyor (5 saniye)..." -ForegroundColor Yellow
            Start-Sleep -Seconds 5
            
            # Tekrar kontrol et
            try {
                $response2 = Invoke-WebRequest -Uri "http://192.168.1.178:8080/health" -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
                if ($response2.StatusCode -eq 200) {
                    Write-Host "✅ API BAŞARIYLA BAŞLATILDI!" -ForegroundColor Green
                    Write-Host ""
                    Write-Host "Bot'u başlatabilirsin!" -ForegroundColor Green
                }
            }
            catch {
                Write-Host "⚠️ API başlatıldı ama henüz hazır değil." -ForegroundColor Yellow
                Write-Host "10 saniye daha bekle ve tekrar dene." -ForegroundColor Yellow
            }
        }
        else {
            Write-Host "❌ start_api_background.vbs bulunamadı!" -ForegroundColor Red
            Write-Host ""
            Write-Host "Manuel başlatma:" -ForegroundColor Yellow
            Write-Host "  1. ActivationAPI klasörüne git" -ForegroundColor White
            Write-Host "  2. start_api_background.vbs dosyasına çift tıkla" -ForegroundColor White
        }
    }
    catch {
        Write-Host "❌ API başlatılamadı: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host ""
        Write-Host "Manuel başlatma:" -ForegroundColor Yellow
        Write-Host "  cd ActivationAPI" -ForegroundColor White
        Write-Host "  python app.py" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Pencereyi kapatmak için bir tuşa bas..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
