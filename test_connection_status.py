import urllib.request
import json

def test_connection_status():
    """Test connection status API endpoint"""
    try:
        url = "http://127.0.0.1:5000/api/connection/status"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        print("📡 Connection Status API Test:")
        print(f"   Connected: {data.get('connected', 'Unknown')}")
        print(f"   Message: {data.get('message', 'No message')}")
        
        if data.get('connection_info'):
            conn_info = data['connection_info']
            print("   Connection Info:")
            print(f"     Host: {conn_info.get('host', 'Unknown')}")
            print(f"     Database: {conn_info.get('database', 'Unknown')}")
            print(f"     Created: {conn_info.get('created_at', 'Unknown')}")
        
        return data
        
    except Exception as e:
        print(f"❌ Error testing connection status: {e}")
        return None

if __name__ == "__main__":
    result = test_connection_status()
    if result:
        print(f"\n✅ API response received successfully")
    else:
        print(f"\n❌ Failed to get API response")
