# Ngrok ile API'yi İnternete Aç

## 1. Ngrok İndir
https://ngrok.com/download

## 2. Ngrok Başlat
```powershell
ngrok http 5000
```

## 3. URL'i Kopyala
Ngrok şöyle bir URL verecek:
```
https://abc123.ngrok.io
```

## 4. Bot'u Güncelle
`LicenseManager.cs` dosyasında:
```csharp
private static readonly string ActivationApiUrl = "https://abc123.ngrok.io";
```

## 5. Build ve Test
```powershell
dotnet build Application/RSBot/RSBot.csproj --configuration Release
```

Artık başka PC'den de çalışacak!

**NOT**: Ngrok ücretsiz versiyonu her seferinde farklı URL verir. Production için Railway/Heroku kullan!
