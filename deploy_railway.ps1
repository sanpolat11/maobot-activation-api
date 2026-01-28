# Railway Deployment Script
# Bu script ActivationAPI'yi Railway'e deploy etmek için gerekli adımları yapar

Write-Host "=" -ForegroundColor Cyan
Write-Host "MaoBot Activation API - Railway Deployment" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Git kontrolü
Write-Host "[1/5] Git kontrolü yapılıyor..." -ForegroundColor Yellow
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "HATA: Git yüklü değil!" -ForegroundColor Red
    Write-Host "Git'i buradan indir: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ Git bulundu" -ForegroundColor Green

# 2. Git repository başlat
Write-Host ""
Write-Host "[2/5] Git repository başlatılıyor..." -ForegroundColor Yellow

if (Test-Path ".git") {
    Write-Host "✓ Git repository zaten mevcut" -ForegroundColor Green
} else {
    git init
    Write-Host "✓ Git repository oluşturuldu" -ForegroundColor Green
}

# 3. .gitignore kontrolü
Write-Host ""
Write-Host "[3/5] .gitignore kontrolü..." -ForegroundColor Yellow
if (Test-Path ".gitignore") {
    Write-Host "✓ .gitignore mevcut" -ForegroundColor Green
} else {
    Write-Host "UYARI: .gitignore bulunamadı!" -ForegroundColor Red
}

# 4. Dosyaları stage'e al
Write-Host ""
Write-Host "[4/5] Dosyalar commit ediliyor..." -ForegroundColor Yellow
git add .
git commit -m "Initial commit - MaoBot Activation API"
Write-Host "✓ Commit tamamlandı" -ForegroundColor Green

# 5. GitHub remote bilgisi
Write-Host ""
Write-Host "[5/5] GitHub Remote Ayarları" -ForegroundColor Yellow
Write-Host ""
Write-Host "Şimdi GitHub'da yeni bir repository oluştur:" -ForegroundColor Cyan
Write-Host "1. https://github.com/new adresine git" -ForegroundColor White
Write-Host "2. Repository adı: maobot-activation-api" -ForegroundColor White
Write-Host "3. Public veya Private seç" -ForegroundColor White
Write-Host "4. README EKLEME!" -ForegroundColor Red
Write-Host "5. Create repository'ye tıkla" -ForegroundColor White
Write-Host ""

$repoUrl = Read-Host "GitHub repository URL'ini gir (örn: https://github.com/sanpolat11/maobot-activation-api.git)"

if ($repoUrl) {
    git remote remove origin 2>$null
    git remote add origin $repoUrl
    git branch -M main
    
    Write-Host ""
    Write-Host "GitHub'a push yapılıyor..." -ForegroundColor Yellow
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ GitHub'a başarıyla yüklendi!" -ForegroundColor Green
    } else {
        Write-Host "HATA: Push başarısız!" -ForegroundColor Red
        Write-Host "GitHub'da authentication gerekebilir." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Sonraki Adımlar:" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Railway'e git: https://railway.app" -ForegroundColor White
Write-Host "2. GitHub ile giriş yap" -ForegroundColor White
Write-Host "3. 'New Project' → 'Deploy from GitHub repo'" -ForegroundColor White
Write-Host "4. 'maobot-activation-api' repository'sini seç" -ForegroundColor White
Write-Host "5. Variables sekmesine git ve ekle:" -ForegroundColor White
Write-Host "   GITHUB_TOKEN=YOUR_GITHUB_TOKEN" -ForegroundColor Yellow
Write-Host "   API_SECRET=maobot-secret-2026" -ForegroundColor Yellow
Write-Host "6. Settings → Generate Domain" -ForegroundColor White
Write-Host "7. Domain URL'ini kopyala!" -ForegroundColor White
Write-Host ""
Write-Host "Detaylı rehber için: RAILWAY_KURULUM.md" -ForegroundColor Cyan
Write-Host ""
