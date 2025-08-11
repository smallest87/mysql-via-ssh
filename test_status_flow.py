"""
Test script untuk debug notifikasi status koneksi MySQL SSH
"""

import urllib.request
import urllib.error
import json
import time

def test_connection_status_flow():
    """Test complete flow dari connect hingga status check"""
    base_url = "http://127.0.0.1:5000"
    
    print("🔄 Testing MySQL SSH Connection Status Flow")
    print("=" * 50)
    
    # 1. Initial status check
    print("\n1️⃣ Initial status check:")
    check_status(base_url)
    
    print("\n2️⃣ Instructions for manual testing:")
    print("   ✅ Open browser to: http://127.0.0.1:5000/")
    print("   ✅ Look at the status badge in navbar (should show 'Disconnected')")
    print("   ✅ Make a MySQL SSH connection using the form")
    print("   ✅ Watch the status badge - it should change to 'Connected'")
    print("   ✅ If it shows yellow 'Error' badge, check browser console")
    
    print("\n3️⃣ Common issues and solutions:")
    print("   🔍 Yellow 'Error' badge causes:")
    print("      - API endpoint returning 500 error")
    print("      - is_connected() method throwing exception")
    print("      - JavaScript fetch() network error")
    print("      - CORS or session issues")
    
    print("\n   🔧 Debugging steps:")
    print("      1. Open browser Developer Tools (F12)")
    print("      2. Go to Console tab")
    print("      3. Look for 'Connection status response:' logs")
    print("      4. Check Network tab for failed /api/connection/status requests")
    print("      5. Check server terminal for error logs")
    
    print("\n   ✅ Expected behavior:")
    print("      - Without connection: Gray 'Disconnected' badge")
    print("      - With active connection: Green 'Connected' badge")
    print("      - On connection error: Yellow 'Error' badge")
    
    # 4. Monitor status API
    print("\n4️⃣ Monitoring API endpoint (press Ctrl+C to stop):")
    try:
        while True:
            print(f"\n[{time.strftime('%H:%M:%S')}] Checking status...")
            result = check_status(base_url)
            
            if result and result.get('connected'):
                print("   🎉 Connection detected! Check browser for green badge.")
                break
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n\n👋 Monitoring stopped by user")
    except Exception as e:
        print(f"\n❌ Monitoring error: {e}")

def check_status(base_url):
    """Helper function to check status API"""
    try:
        url = f"{base_url}/api/connection/status"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        print(f"   Status: {data.get('connected', 'Unknown')}")
        print(f"   Message: {data.get('message', 'No message')}")
        
        if data.get('connection_info'):
            info = data['connection_info']
            print(f"   Connection: {info.get('host')}/{info.get('database')}")
            
        return data
        
    except Exception as e:
        print(f"   ❌ API check failed: {e}")
        return None

if __name__ == "__main__":
    test_connection_status_flow()
