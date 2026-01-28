from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
import requests
from github import Github
import hashlib

app = Flask(__name__)
CORS(app)

# GitHub Configuration
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', 'YOUR_GITHUB_TOKEN_HERE')
GITHUB_REPO = 'sanpolat11/maobot-licenses'
GITHUB_FILE = 'licenses.json'

# API Secret Key (basit güvenlik)
API_SECRET = os.environ.get('API_SECRET', 'your-secret-key-here')

def get_github_client():
    """GitHub client oluştur"""
    return Github(GITHUB_TOKEN)

def get_license_data():
    """GitHub'dan lisans verilerini çek"""
    try:
        g = get_github_client()
        repo = g.get_repo(GITHUB_REPO)
        file_content = repo.get_contents(GITHUB_FILE)
        data = json.loads(file_content.decoded_content.decode())
        return data, file_content
    except Exception as e:
        print(f"GitHub okuma hatası: {e}")
        return None, None

def update_github_license(key, hardware_id):
    """GitHub'daki lisansı güncelle"""
    try:
        g = get_github_client()
        repo = g.get_repo(GITHUB_REPO)
        file_content = repo.get_contents(GITHUB_FILE)
        
        # Mevcut veriyi oku
        data = json.loads(file_content.decoded_content.decode())
        
        # Key'i güncelle
        if key in data['keys']:
            data['keys'][key]['hardware_id'] = hardware_id
            data['last_updated'] = datetime.utcnow().strftime('%Y-%m-%d')
            
            # GitHub'a yaz
            message = f"Activate key: {key} with hardware_id: {hardware_id[:8]}..."
            repo.update_file(
                GITHUB_FILE,
                message,
                json.dumps(data, indent=2),
                file_content.sha
            )
            return True
        else:
            print(f"Key bulunamadı: {key}")
            return False
            
    except Exception as e:
        print(f"GitHub yazma hatası: {e}")
        return False

@app.route('/health', methods=['GET'])
def health():
    """API sağlık kontrolü"""
    return jsonify({
        'status': 'ok',
        'message': 'MaoBot Activation API is running'
    })

@app.route('/activate', methods=['POST'])
def activate():
    """Key aktivasyonu"""
    try:
        data = request.get_json()
        
        # Parametreleri kontrol et
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
            
        key = data.get('key')
        hardware_id = data.get('hardware_id')
        secret = data.get('secret')
        
        if not key or not hardware_id:
            return jsonify({'success': False, 'message': 'Missing key or hardware_id'}), 400
        
        # Basit güvenlik kontrolü
        if secret != API_SECRET:
            return jsonify({'success': False, 'message': 'Invalid secret'}), 401
        
        print(f"[ACTIVATE] Key: {key}, Hardware ID: {hardware_id[:8]}...")
        
        # GitHub'dan lisans verilerini çek
        license_data, _ = get_license_data()
        if not license_data:
            return jsonify({'success': False, 'message': 'Failed to fetch license data'}), 500
        
        # Key var mı kontrol et
        if key not in license_data['keys']:
            return jsonify({'success': False, 'message': 'Key not found'}), 404
        
        key_info = license_data['keys'][key]
        
        # Key aktif mi?
        if not key_info.get('active', False):
            return jsonify({'success': False, 'message': 'Key is not active'}), 403
        
        # Key süresi dolmuş mu?
        expires = datetime.strptime(key_info['expires'], '%Y-%m-%d')
        if expires < datetime.utcnow():
            return jsonify({'success': False, 'message': 'Key has expired'}), 403
        
        # Hardware ID kontrolü
        existing_hwid = key_info.get('hardware_id', '')
        
        if existing_hwid and existing_hwid != hardware_id:
            # Key başka bir PC'ye bağlı
            return jsonify({
                'success': False,
                'message': 'Key is already bound to another PC',
                'bound_hwid': existing_hwid[:8] + '...'
            }), 409
        
        if not existing_hwid:
            # İlk aktivasyon - GitHub'ı güncelle
            print(f"[ACTIVATE] İlk aktivasyon - GitHub güncelleniyor...")
            if update_github_license(key, hardware_id):
                return jsonify({
                    'success': True,
                    'message': 'Key activated successfully',
                    'first_activation': True
                })
            else:
                return jsonify({'success': False, 'message': 'Failed to update GitHub'}), 500
        else:
            # Aynı PC - başarılı
            return jsonify({
                'success': True,
                'message': 'Key validated successfully',
                'first_activation': False
            })
            
    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/validate', methods=['POST'])
def validate():
    """Key doğrulama (aktivasyon yapmadan)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
            
        key = data.get('key')
        hardware_id = data.get('hardware_id')
        secret = data.get('secret')
        
        if not key or not hardware_id:
            return jsonify({'success': False, 'message': 'Missing key or hardware_id'}), 400
        
        if secret != API_SECRET:
            return jsonify({'success': False, 'message': 'Invalid secret'}), 401
        
        # GitHub'dan lisans verilerini çek
        license_data, _ = get_license_data()
        if not license_data:
            return jsonify({'success': False, 'message': 'Failed to fetch license data'}), 500
        
        # Key var mı kontrol et
        if key not in license_data['keys']:
            return jsonify({'success': False, 'message': 'Key not found'}), 404
        
        key_info = license_data['keys'][key]
        
        # Key aktif mi?
        if not key_info.get('active', False):
            return jsonify({'success': False, 'message': 'Key is not active'}), 403
        
        # Key süresi dolmuş mu?
        expires = datetime.strptime(key_info['expires'], '%Y-%m-%d')
        if expires < datetime.utcnow():
            return jsonify({'success': False, 'message': 'Key has expired'}), 403
        
        # Hardware ID kontrolü
        existing_hwid = key_info.get('hardware_id', '')
        
        if existing_hwid and existing_hwid != hardware_id:
            return jsonify({
                'success': False,
                'message': 'Key is bound to another PC'
            }), 409
        
        return jsonify({
            'success': True,
            'message': 'Key is valid',
            'expires': key_info['expires'],
            'type': key_info['type']
        })
            
    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/deactivate', methods=['POST'])
def deactivate():
    """Key'i deaktive et (hardware_id'yi temizle)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
            
        key = data.get('key')
        secret = data.get('secret')
        admin_password = data.get('admin_password')
        
        if not key:
            return jsonify({'success': False, 'message': 'Missing key'}), 400
        
        if secret != API_SECRET:
            return jsonify({'success': False, 'message': 'Invalid secret'}), 401
        
        # Admin şifresi kontrolü (ekstra güvenlik)
        if admin_password != 'admin123':  # Değiştir!
            return jsonify({'success': False, 'message': 'Invalid admin password'}), 401
        
        # GitHub'ı güncelle (hardware_id'yi temizle)
        if update_github_license(key, ''):
            return jsonify({
                'success': True,
                'message': 'Key deactivated successfully'
            })
        else:
            return jsonify({'success': False, 'message': 'Failed to update GitHub'}), 500
            
    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("MaoBot Activation API")
    print("=" * 50)
    print(f"GitHub Repo: {GITHUB_REPO}")
    print(f"API Secret: {API_SECRET}")
    print("=" * 50)
    app.run(host='0.0.0.0', port=8080, debug=True)
