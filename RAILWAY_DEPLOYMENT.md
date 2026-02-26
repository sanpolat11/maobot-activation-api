# MaoBot API - Railway.app Deployment

## 🚀 Neden Railway?

- ✅ **5 dakikada kurulum**
- ✅ **Ücretsiz başlangıç** (500 saat/ay)
- ✅ **Garantili dışarıdan erişim** (port forwarding sorunu yok)
- ✅ **Otomatik HTTPS**
- ✅ **7/24 çalışır**

---

## 📋 ADIM 1: Railway Hesabı Oluştur

1. Git: https://railway.app
2. **"Start a New Project"** tıkla
3. **GitHub ile giriş yap** (veya email)
4. Hesap oluştur (ücretsiz)

---

## 📋 ADIM 2: Proje Oluştur

1. Railway dashboard'da **"New Project"** tıkla
2. **"Deploy from GitHub repo"** seç
3. **"Configure GitHub App"** tıkla
4. Repository'ni seç veya **"Empty Project"** seç

---

## 📋 ADIM 3: Dosyaları Hazırla

Railway için gerekli dosyalar zaten hazır:

### ✅ `Procfile` (Zaten var)
```
web: python app.py
```

### ✅ `requirements.txt` (Zaten var)
```
flask==3.0.0
flask-cors==4.0.0
```

### ✅ `runtime.txt` (Zaten var)
```
python-3.11.7
```

---

## 📋 ADIM 4: Deploy Et

### Yöntem A: GitHub ile (Önerilen)

1. **GitHub'a push et:**
```bash
cd ActivationAPI
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/KULLANICI_ADIN/maobot-api.git
git push -u origin main
```

2. **Railway'de:**
   - "Deploy from GitHub repo" seç
   - Repository'ni seç
   - "Deploy Now" tıkla

### Yöntem B: Railway CLI ile

1. **Railway CLI kur:**
```bash
npm i -g @railway/cli
```

2. **Login:**
```bash
railway login
```

3. **Deploy:**
```bash
cd ActivationAPI
railway init
railway up
```

---

## 📋 ADIM 5: Environment Variables Ayarla

Railway dashboard'da:

1. **"Variables"** sekmesine git
2. Şu değişkenleri ekle:

```
PORT=8080
API_SECRET=maobot-secret-2026
```

3. **"Deploy"** tıkla (otomatik restart olur)

---

## 📋 ADIM 6: URL'i Al

1. Railway dashboard'da **"Settings"** sekmesine git
2. **"Generate Domain"** tıkla
3. URL'i kopyala (örnek: `maobot-api-production.up.railway.app`)

---

## 📋 ADIM 7: Bot'u Güncelle

`Library/RSBot.Core/Components/LicenseManager.cs` dosyasında:

```csharp
// Eski (local)
private static readonly string API_URL = "http://88.250.60.205:8080";

// Yeni (Railway)
private static readonly string API_URL = "https://maobot-api-production.up.railway.app";
```

Projeyi yeniden derle:
```bash
dotnet build Library/RSBot.Core/RSBot.Core.csproj -c Release
Copy-Item "Library\RSBot.Core\bin\Release\RSBot.Core.dll" -Destination "Build\" -Force
```

---

## 📋 ADIM 8: Test Et

PowerShell'de:

```powershell
Invoke-WebRequest -Uri "https://maobot-api-production.up.railway.app/health" -UseBasicParsing
```

Yanıt:
```json
{
  "status": "ok",
  "message": "MaoBot Activation API is running",
  "version": "2.0"
}
```

✅ **BAŞARILI!** API artık dışarıdan erişilebilir!

---

## 🔄 Güncelleme Yapmak

### GitHub ile:
```bash
git add .
git commit -m "Update"
git push
```
Railway otomatik deploy eder.

### Railway CLI ile:
```bash
railway up
```

---

## 📊 Kullanım Takibi

Railway dashboard'da:

- **Metrics:** CPU, RAM, Network kullanımı
- **Logs:** API logları (gerçek zamanlı)
- **Deployments:** Deploy geçmişi

---

## 💰 Maliyet

### Ücretsiz Plan
- **500 saat/ay** (yaklaşık 20 gün)
- **100 GB network**
- **1 GB RAM**

### Hobby Plan ($5/ay)
- **Sınırsız saat**
- **100 GB network**
- **8 GB RAM**

---

## 🚨 Sorun Giderme

### "Application failed to respond"

**Sebep:** PORT environment variable yanlış

**Çözüm:**
```python
# app.py'de
port = int(os.environ.get('PORT', 8080))
app.run(host='0.0.0.0', port=port)
```

### "Module not found"

**Sebep:** requirements.txt eksik

**Çözüm:**
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Logları Görme

Railway dashboard'da:
1. "Deployments" sekmesi
2. Son deployment'a tıkla
3. "View Logs" tıkla

---

## ✅ Avantajlar

| Özellik | Local (Kendi PC) | Railway |
|---------|------------------|---------|
| Port forwarding | ❌ Gerekli | ✅ Yok |
| ISP bloke | ❌ Sorun | ✅ Yok |
| 7/24 çalışma | ❌ PC açık olmalı | ✅ Her zaman |
| HTTPS | ❌ Yok | ✅ Otomatik |
| Bakım | ❌ Manuel | ✅ Otomatik |

---

## 🎯 Özet

1. Railway hesabı oluştur
2. Proje oluştur
3. GitHub'a push et veya Railway CLI kullan
4. Environment variables ayarla
5. URL'i al
6. Bot'u güncelle
7. Test et
8. Müşterilere ver!

**Toplam süre: 5-10 dakika** 🚀
