# 🚀 Activation API Nasıl Başlatılır?

## ⚡ HIZLI BAŞLATMA (En Kolay Yöntem)

### Windows'ta Çift Tıklama ile Başlat:

1. **Dosya Gezgini'ni aç**
2. **Bu klasöre git**: `C:\Users\barba\OneDrive\Masaüstü\Rsbot1011\ActivationAPI`
3. **`start_api_background.vbs`** dosyasına **ÇİFT TIKLA**
4. ✅ **Bitti!** API arka planda çalışmaya başladı (pencere açılmaz)

---

## 🔍 API Çalışıyor mu Kontrol Et

### Yöntem 1: Tarayıcıdan Kontrol
1. **Chrome/Edge/Firefox** aç
2. Adres çubuğuna yaz: `http://192.168.1.178:8080/health`
3. Şunu görmelisin:
```json
{
  "message": "MaoBot Activation API is running",
  "status": "ok"
}
```

### Yöntem 2: PowerShell'den Kontrol
```powershell
curl http://192.168.1.178:8080/health
```
- **200 OK** görürsen → ✅ Çalışıyor
- **Bağlantı hatası** alırsan → ❌ Kapalı

---

## 🛑 API'yi Durdurma

### Yöntem 1: Task Manager
1. **Ctrl + Shift + Esc** bas (Task Manager açılır)
2. **Details** sekmesine git
3. **python.exe** bul
4. Sağ tık → **End Task**

### Yöntem 2: PowerShell
```powershell
Get-Process python | Stop-Process -Force
```

---

## 🔄 API'yi Yeniden Başlatma

1. **Önce durdur** (yukarıdaki yöntemlerden biri)
2. **Sonra başlat** (`start_api_background.vbs` çift tıkla)

---

## ⚠️ SORUN GİDERME

### Problem 1: "API'ye bağlanılamıyor" hatası

**Çözüm:**
1. API çalışıyor mu kontrol et (yukarıdaki yöntemlerle)
2. Çalışmıyorsa → `start_api_background.vbs` çift tıkla
3. Hala çalışmıyorsa → PowerShell'den manuel başlat:

```powershell
cd C:\Users\barba\OneDrive\Masaüstü\Rsbot1011\ActivationAPI
python app.py
```

### Problem 2: "Port 8080 kullanımda" hatası

**Çözüm:**
```powershell
# Port'u kullanan programı bul:
netstat -ano | findstr :8080

# Çıkan PID numarasını kullanarak kapat:
taskkill /PID NUMARA /F
```

### Problem 3: IP adresi değişti

**Kontrol et:**
```powershell
ipconfig
```

**IPv4 Address** satırına bak. Eğer `192.168.1.178` değilse:

1. Yeni IP'yi not al (örnek: `192.168.1.200`)
2. Bana söyle, kodu güncelleyeyim

---

## 🖥️ BİLGİSAYAR AÇILINCA OTOMATİK BAŞLATMA

### Windows Başlangıç Klasörüne Ekle:

1. **Windows + R** bas
2. Yaz: `shell:startup` → Enter
3. **Başlangıç klasörü** açılır
4. `start_api_background.vbs` dosyasının **kısayolunu** buraya kopyala

**Artık bilgisayar her açıldığında API otomatik başlayacak!**

---

## 📋 ÖZET - HIZLI KOMUTLAR

| Ne Yapmak İstiyorsun? | Nasıl Yapılır? |
|----------------------|----------------|
| **API'yi Başlat** | `start_api_background.vbs` çift tıkla |
| **API Çalışıyor mu?** | Tarayıcıda: `http://192.168.1.178:8080/health` |
| **API'yi Durdur** | Task Manager → python.exe → End Task |
| **IP Adresimi Öğren** | PowerShell: `ipconfig` |
| **Port 8080 Meşgul** | PowerShell: `netstat -ano \| findstr :8080` |

---

## 🆘 ACİL YARDIM

Eğer hiçbir şey çalışmıyorsa:

1. **PowerShell aç** (Yönetici olarak)
2. Şunu çalıştır:
```powershell
cd C:\Users\barba\OneDrive\Masaüstü\Rsbot1011\ActivationAPI
python app.py
```
3. Hata mesajını oku ve bana göster

---

## 📞 İLETİŞİM BİLGİLERİ

- **GitHub Repo**: https://github.com/sanpolat11/maobot-licenses
- **API Port**: 8080
- **API Secret**: maobot-secret-2026
