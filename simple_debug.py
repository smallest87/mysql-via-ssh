import urllib.request
import urllib.error
import json

def debug_status_api():
    """Debug status API tanpa external dependencies"""
    base_url = "http://127.0.0.1:5000"
    
    print("🔧 Debugging Connection Status API")
    print("=" * 40)
    
    try:
        # Test API endpoint langsung
        print("\n1️⃣ Testing /api/connection/status directly:")
        
        url = f"{base_url}/api/connection/status"
        request = urllib.request.Request(url)
        request.add_header('User-Agent', 'Python-Debug-Tool')
        
        with urllib.request.urlopen(request) as response:
            status_code = response.getcode()
            content = response.read().decode('utf-8')
            
            print(f"   Status Code: {status_code}")
            print(f"   Raw Response: {content}")
            
            try:
                data = json.loads(content)
                print(f"   Parsed JSON: {json.dumps(data, indent=4)}")
                
                if status_code == 200:
                    print("   ✅ API responding correctly")
                    if data.get('connected') is False:
                        print("   ✅ Correctly shows no connection")
                else:
                    print(f"   ❌ Unexpected status code: {status_code}")
                    
            except json.JSONDecodeError as e:
                print(f"   ❌ Invalid JSON response: {e}")
                
    except urllib.error.HTTPError as e:
        print(f"   ❌ HTTP Error {e.code}: {e.reason}")
        try:
            error_content = e.read().decode('utf-8')
            print(f"   Error content: {error_content}")
        except:
            pass
            
    except Exception as e:
        print(f"   ❌ Request failed: {e}")
    
    print("\n🔍 Possible causes of yellow error badge:")
    print("   1. JavaScript fetch() CORS issue")
    print("   2. API endpoint returning non-200 status")
    print("   3. API returning invalid JSON")
    print("   4. Network connectivity issue")
    print("   5. Server error in connection health check")
    
    print("\n💡 Check browser console for:")
    print("   - 'Connection status response:' log")
    print("   - Any fetch errors or exceptions")
    print("   - Network tab for failed requests")

if __name__ == "__main__":
    debug_status_api()
