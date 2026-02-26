from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
import hashlib

app = Flask(__name__)
CORS(app)

# Basit JSON veritabanı
LICENSE_DB = 'licenses.json'
API_SECRET = os.environ.get('API_SECRET', 'maobot-secret-2026')

def load_licenses():
    """Lisansları yükle"""
    if not os.path.exists(LICENSE_DB):
        return {'keys': {}, 'last_updated': datetime.utcnow().isoformat()}
    
    with open(LICENSE_DB, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_licenses(data):
    """Lisansları kaydet"""
    data['last_updated'] = datetime.utcnow().isoformat()
    with open(LICENSE_DB, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def parse_key_type(key):
    """Key tipini belirle"""
    if key.startswith('5M-'):
        return '5 Dakika', 5 / (24 * 60)  # 5 dakika = gün cinsinden
    elif key.startswith('1M-'):
        return '1 Dakika', 1 / (24 * 60)
    elif key.startswith('10D-'):
        return '10 Gün', 10
    elif key.startswith('15D-'):
        return '15 Gün', 15
    elif key.startswith('30D-'):
        return '30 Gün', 30
    else:
        return 'Bilinmeyen', 0

@app.route('/health', methods=['GET'])
def health():
    """API sağlık kontrolü"""
    return jsonify({
        'status': 'ok',
        'message': 'MaoBot Activation API is running',
        'version': '2.0'
    })

@app.route('/activate', methods=['POST'])
def activate():
    """Key aktivasyonu"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'Veri gönderilmedi'}), 400
            
        key = data.get('key')
        hardware_id = data.get('hardware_id')
        secret = data.get('secret')
        
        if not key or not hardware_id:
            return jsonify({'success': False, 'message': 'Key veya hardware_id eksik'}), 400
        
        if secret != API_SECRET:
            return jsonify({'success': False, 'message': 'Geçersiz secret'}), 401
        
        print(f"[ACTIVATE] Key: {key}, HWID: {hardware_id[:8]}...")
        
        # Lisansları yükle
        licenses = load_licenses()
        
        # Key var mı kontrol et
        if key in licenses['keys']:
            key_info = licenses['keys'][key]
            
            # Süre kontrolü
            expires = datetime.fromisoformat(key_info['expires'])
            if expires < datetime.utcnow():
                return jsonify({'success': False, 'message': 'Key süresi dolmuş'}), 403
            
            # Hardware ID kontrolü
            existing_hwid = key_info.get('hardware_id', '')
            
            if existing_hwid and existing_hwid != hardware_id:
                return jsonify({
                    'success': False,
                    'message': 'Key başka bir bilgisayara bağlı'
                }), 409
            
            if not existing_hwid:
                # İlk aktivasyon
                key_info['hardware_id'] = hardware_id
                key_info['activated_at'] = datetime.utcnow().isoformat()
                save_licenses(licenses)
                print(f"[ACTIVATE] ✅ İlk aktivasyon: {key}")
            
            return jsonify({
                'success': True,
                'message': 'Key aktif',
                'expires': key_info['expires'],
                'type': key_info['type']
            })
        else:
            # Yeni key - otomatik ekle
            key_type, duration_days = parse_key_type(key)
            
            if duration_days == 0:
                return jsonify({'success': False, 'message': 'Geçersiz key formatı'}), 400
            
            activation_date = datetime.utcnow()
            expiration_date = activation_date + timedelta(days=duration_days)
            
            licenses['keys'][key] = {
                'type': key_type,
                'hardware_id': hardware_id,
                'activated_at': activation_date.isoformat(),
                'expires': expiration_date.isoformat(),
                'active': True
            }
            
            save_licenses(licenses)
            print(f"[ACTIVATE] ✅ Yeni key eklendi: {key} ({key_type})")
            
            return jsonify({
                'success': True,
                'message': 'Key aktive edildi',
                'expires': expiration_date.isoformat(),
                'type': key_type
            })
            
    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/validate', methods=['POST'])
def validate():
    """Key doğrulama"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'Veri gönderilmedi'}), 400
            
        key = data.get('key')
        hardware_id = data.get('hardware_id')
        secret = data.get('secret')
        
        if not key or not hardware_id:
            return jsonify({'success': False, 'message': 'Key veya hardware_id eksik'}), 400
        
        if secret != API_SECRET:
            return jsonify({'success': False, 'message': 'Geçersiz secret'}), 401
        
        licenses = load_licenses()
        
        if key not in licenses['keys']:
            return jsonify({'success': False, 'message': 'Key bulunamadı'}), 404
        
        key_info = licenses['keys'][key]
        
        # Süre kontrolü
        expires = datetime.fromisoformat(key_info['expires'])
        if expires < datetime.utcnow():
            return jsonify({'success': False, 'message': 'Key süresi dolmuş'}), 403
        
        # Hardware ID kontrolü
        existing_hwid = key_info.get('hardware_id', '')
        
        if existing_hwid and existing_hwid != hardware_id:
            return jsonify({'success': False, 'message': 'Key başka bir bilgisayara bağlı'}), 409
        
        return jsonify({
            'success': True,
            'message': 'Key geçerli',
            'expires': key_info['expires'],
            'type': key_info['type']
        })
            
    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    # Port'u environment variable'dan al, yoksa 8080 kullan
    port = int(os.environ.get('PORT', 8080))
    
    print("=" * 50)
    print("MaoBot Activation API v2.0")
    print("=" * 50)
    print(f"License DB: {LICENSE_DB}")
    print(f"API Secret: {API_SECRET}")
    print(f"Port: {port}")
    print("=" * 50)
    app.run(host='0.0.0.0', port=port, debug=True)
