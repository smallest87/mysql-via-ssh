import requests
import json
import sys

# Base URL
BASE_URL = "http://127.0.0.1:5000"
session = requests.Session()

def login_admin():
    """Login sebagai admin"""
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    response = session.post(f"{BASE_URL}/admin/login", data=login_data)
    if response.status_code == 200 and 'dashboard' in response.text:
        print("✅ Login berhasil")
        return True
    else:
        print("❌ Login gagal")
        print("Response:", response.text[:200])
        return False

def create_test_query():
    """Buat query test"""
    query_data = {
        'query_name': 'Test Query for Buttons',
        'sql_query': 'SELECT * FROM users LIMIT 5;',
        'category': 'testing',
        'description': 'Query untuk test fungsi tombol edit/execute/delete'
    }
    
    response = session.post(
        f"{BASE_URL}/admin/api/workspace/queries/save", 
        json=query_data,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print("✅ Query test berhasil dibuat")
            return result
        else:
            print("❌ Error creating query:", result.get('message'))
    else:
        print("❌ HTTP Error:", response.status_code)
        print("Response:", response.text[:200])
    
    return None

def get_queries():
    """Ambil semua queries"""
    response = session.get(f"{BASE_URL}/admin/api/workspace/queries")
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            queries = result.get('queries', [])
            print(f"✅ Berhasil mengambil {len(queries)} queries")
            for query in queries:
                print(f"  - ID: {query['id']}, Name: {query['name']}")
            return queries
        else:
            print("❌ Error getting queries:", result.get('message'))
    else:
        print("❌ HTTP Error:", response.status_code)
    
    return []

def test_edit_query(query_id):
    """Test endpoint update query"""
    update_data = {
        'query_id': query_id,
        'query_name': 'Updated Test Query',
        'sql_query': 'SELECT * FROM users WHERE id > 0 LIMIT 5;',
        'category': 'testing',
        'description': 'Updated description'
    }
    
    response = session.post(
        f"{BASE_URL}/admin/api/workspace/queries/update",
        json=update_data,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print("✅ Query berhasil diupdate")
            return True
        else:
            print("❌ Error updating query:", result.get('message'))
    else:
        print("❌ HTTP Error:", response.status_code)
    
    return False

def test_delete_query(query_id):
    """Test endpoint delete query"""
    delete_data = {'query_id': query_id}
    
    response = session.delete(
        f"{BASE_URL}/admin/api/workspace/queries/delete",
        json=delete_data,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print("✅ Query berhasil dihapus")
            return True
        else:
            print("❌ Error deleting query:", result.get('message'))
    else:
        print("❌ HTTP Error:", response.status_code)
    
    return False

if __name__ == "__main__":
    print("🔄 Testing CRUD functionality...")
    
    # Step 1: Login
    if not login_admin():
        sys.exit(1)
    
    # Step 2: Create test query
    create_result = create_test_query()
    if not create_result:
        sys.exit(1)
    
    # Step 3: Get queries to verify
    queries = get_queries()
    if not queries:
        print("❌ No queries found")
        sys.exit(1)
    
    # Step 4: Test edit functionality
    test_query_id = queries[0]['id']
    print(f"\n🔄 Testing edit functionality with query ID: {test_query_id}")
    test_edit_query(test_query_id)
    
    # Step 5: Verify updated query
    print("\n🔄 Verifying updated query...")
    get_queries()
    
    # Step 6: Test delete functionality  
    print(f"\n🔄 Testing delete functionality with query ID: {test_query_id}")
    test_delete_query(test_query_id)
    
    # Step 7: Verify deletion
    print("\n🔄 Verifying deletion...")
    final_queries = get_queries()
    
    print(f"\n✅ Testing completed!")
    print(f"Final query count: {len(final_queries)}")
