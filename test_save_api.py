"""
Test Save Query - After Database Fix
"""

import requests
import json

def test_save_query_api():
    print("🧪 Testing Save Query API")
    print("=" * 30)
    
    # Test data
    test_query = {
        "name": "Test Query 2024",
        "category": "testing",
        "description": "Test query after database fix",
        "sql_query": "SELECT * FROM users LIMIT 5"
    }
    
    url = "http://127.0.0.1:5000/admin/api/workspace/queries/save"
    
    try:
        # Make POST request with JSON data
        response = requests.post(
            url,
            json=test_query,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Data: {response.json()}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Save Query berhasil!")
            else:
                print(f"❌ Save Query gagal: {result.get('message')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure Flask app is running.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_save_query_api()
