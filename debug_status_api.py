import requests
import json
import time

def test_status_api_with_session():
    """Test connection status API dengan session"""
    session = requests.Session()
    base_url = "http://127.0.0.1:5000"
    
    print("🔧 Testing Connection Status API with Debug Info")
    print("=" * 55)
    
    # 1. Test status tanpa koneksi
    print("\n1️⃣ Testing status without connection:")
    try:
        response = session.get(f"{base_url}/api/connection/status")
        data = response.json()
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {json.dumps(data, indent=4)}")
        
        if response.status_code != 200:
            print(f"   ❌ HTTP Error: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"   ❌ Request failed: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"   ❌ Invalid JSON response: {e}")
        return False
    
    # 2. Test membuat koneksi dummy (simulasi)
    print("\n2️⃣ Simulating connection creation:")
    
    # Coba akses halaman utama untuk init session
    try:
        home_response = session.get(f"{base_url}/")
        print(f"   Home page status: {home_response.status_code}")
        
        # Check cookies/session
        print(f"   Session cookies: {dict(session.cookies)}")
        
    except Exception as e:
        print(f"   ❌ Failed to access home page: {e}")
    
    # 3. Test API status lagi setelah init session
    print("\n3️⃣ Testing status after session init:")
    try:
        response = session.get(f"{base_url}/api/connection/status")
        data = response.json()
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {json.dumps(data, indent=4)}")
        
        # Check jika masih error
        if data.get('connected') is False:
            print(f"   ✅ Correctly shows disconnected: {data.get('message')}")
        
    except Exception as e:
        print(f"   ❌ Second status check failed: {e}")
    
    print("\n📊 Summary:")
    print("   - If you see 'Error checking status' in browser,")
    print("     check browser console for detailed error messages")
    print("   - Server logs will show detailed connection checking")
    print("   - Yellow badge usually means JavaScript fetch error")
    
    return True

if __name__ == "__main__":
    test_status_api_with_session()
