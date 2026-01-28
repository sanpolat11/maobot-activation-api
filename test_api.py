import requests
import json

API_URL = "http://localhost:5000"
API_SECRET = "maobot-secret-2026"

def test_health():
    """Health check testi"""
    print("\n=== HEALTH CHECK ===")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_activate(key, hardware_id):
    """Aktivasyon testi"""
    print(f"\n=== ACTIVATE: {key} ===")
    data = {
        "key": key,
        "hardware_id": hardware_id,
        "secret": API_SECRET
    }
    response = requests.post(f"{API_URL}/activate", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_validate(key, hardware_id):
    """Doğrulama testi"""
    print(f"\n=== VALIDATE: {key} ===")
    data = {
        "key": key,
        "hardware_id": hardware_id,
        "secret": API_SECRET
    }
    response = requests.post(f"{API_URL}/validate", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

if __name__ == "__main__":
    print("=" * 50)
    print("MaoBot Activation API Test")
    print("=" * 50)
    
    # Test 1: Health check
    if not test_health():
        print("\n❌ API çalışmıyor! Önce 'python app.py' ile başlat.")
        exit(1)
    
    # Test 2: İlk aktivasyon
    test_activate("DEMO-3DAY-001", "TEST-HARDWARE-ID-PC-A")
    
    # Test 3: Aynı PC'de tekrar
    test_activate("DEMO-3DAY-001", "TEST-HARDWARE-ID-PC-A")
    
    # Test 4: Farklı PC'de deneme (başarısız olmalı)
    test_activate("DEMO-3DAY-001", "TEST-HARDWARE-ID-PC-B")
    
    # Test 5: Validate
    test_validate("DEMO-3DAY-001", "TEST-HARDWARE-ID-PC-A")
    
    print("\n" + "=" * 50)
    print("Test tamamlandı!")
    print("=" * 50)
