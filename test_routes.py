import urllib.request
import urllib.error
import sys

def test_url(url):
    try:
        with urllib.request.urlopen(url) as response:
            status_code = response.getcode()
            content = response.read().decode('utf-8')
            print(f"✅ {url}")
            print(f"   Status: {status_code}")
            print(f"   Content length: {len(content)} characters")
            if 'redirect' in content.lower() or status_code in [301, 302]:
                print("   ↳ Appears to be a redirect")
            return True
    except urllib.error.HTTPError as e:
        print(f"❌ {url}")
        print(f"   HTTP Error: {e.code} - {e.reason}")
        return False
    except Exception as e:
        print(f"❌ {url}")
        print(f"   Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔄 Testing Flask routes...")
    
    test_urls = [
        "http://127.0.0.1:5000/",
        "http://127.0.0.1:5000/admin",
        "http://127.0.0.1:5000/admin/login",
        "http://127.0.0.1:5000/admin/dashboard"
    ]
    
    results = []
    for url in test_urls:
        result = test_url(url)
        results.append(result)
        print()
    
    success_count = sum(results)
    print(f"📊 Results: {success_count}/{len(test_urls)} routes accessible")
    
    if success_count == len(test_urls):
        print("🎉 All routes working!")
    else:
        print("⚠️ Some routes have issues")
