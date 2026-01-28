# MaoBot Activation API

GitHub'daki lisans dosyasını otomatik güncelleyen activation API.

## 🚀 Kurulum

### 1. Python Kurulumu
```bash
python -m pip install -r requirements.txt
```

### 2. GitHub Token Oluştur

1. GitHub'a git: https://github.com/settings/tokens
2. **Generate new token (classic)** tıkla
3. İsim ver: `maobot-activation-api`
4. **repo** yetkisini seç (tüm repo yetkisi)
5. Token'ı kopyala

### 3. Environment Variables

Windows CMD:
```cmd
set GITHUB_TOKEN=ghp_your_token_here
set API_SECRET=your-secret-key-here
```

Windows PowerShell:
```powershell
$env:GITHUB_TOKEN="ghp_your_token_here"
$env:API_SECRET="your-secret-key-here"
```

Linux/Mac:
```bash
export GITHUB_TOKEN=ghp_your_token_here
export API_SECRET=your-secret-key-here
```

### 4. API'yi Başlat

```bash
python app.py
```

API şu adreste çalışacak: `http://localhost:5000`

## 📡 API Endpoints

### 1. Health Check
```
GET /health
```

Response:
```json
{
  "status": "ok",
  "message": "MaoBot Activation API is running"
}
```

### 2. Activate Key
```
POST /activate
Content-Type: application/json

{
  "key": "DEMO-3DAY-001",
  "hardware_id": "1A2B3C4D5E6F7G8H9I0J1K2L3M4N5O6P",
  "secret": "your-secret-key-here"
}
```

Response (İlk aktivasyon):
```json
{
  "success": true,
  "message": "Key activated successfully",
  "first_activation": true
}
```

Response (Aynı PC):
```json
{
  "success": true,
  "message": "Key validated successfully",
  "first_activation": false
}
```

Response (Farklı PC):
```json
{
  "success": false,
  "message": "Key is already bound to another PC",
  "bound_hwid": "1A2B3C4D..."
}
```

### 3. Validate Key
```
POST /validate
Content-Type: application/json

{
  "key": "DEMO-3DAY-001",
  "hardware_id": "1A2B3C4D5E6F7G8H9I0J1K2L3M4N5O6P",
  "secret": "your-secret-key-here"
}
```

Response:
```json
{
  "success": true,
  "message": "Key is valid",
  "expires": "2026-02-28",
  "type": "demo"
}
```

### 4. Deactivate Key (Admin)
```
POST /deactivate
Content-Type: application/json

{
  "key": "DEMO-3DAY-001",
  "secret": "your-secret-key-here",
  "admin_password": "admin123"
}
```

Response:
```json
{
  "success": true,
  "message": "Key deactivated successfully"
}
```

## 🔒 Güvenlik

1. **API_SECRET**: Her istekte gönderilmeli
2. **GITHUB_TOKEN**: Sadece sunucuda saklanmalı
3. **admin_password**: Deactivation için gerekli (değiştir!)

## 🌐 Production Deployment

### Heroku
```bash
heroku create maobot-activation-api
heroku config:set GITHUB_TOKEN=ghp_your_token_here
heroku config:set API_SECRET=your-secret-key-here
git push heroku main
```

### Railway
1. Railway.app'e git
2. New Project → Deploy from GitHub
3. Environment Variables ekle:
   - `GITHUB_TOKEN`
   - `API_SECRET`

### Render
1. Render.com'a git
2. New Web Service
3. Environment Variables ekle

## 🧪 Test

```bash
# Health check
curl http://localhost:5000/health

# Activate
curl -X POST http://localhost:5000/activate \
  -H "Content-Type: application/json" \
  -d '{
    "key": "DEMO-3DAY-001",
    "hardware_id": "TEST123456789",
    "secret": "your-secret-key-here"
  }'
```

## 📝 Notlar

- API GitHub'ı otomatik günceller
- İlk aktivasyonda `hardware_id` kaydedilir
- Farklı PC'de aktivasyon engellenir
- Admin deactivation ile `hardware_id` temizlenebilir
