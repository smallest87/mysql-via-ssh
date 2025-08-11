"""
Test Update Query - Fix "no such column: category" pada Edit Query
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database.admin_db import AdminDB

def test_update_query():
    print("🔧 Testing Update Query Function")
    print("=" * 40)
    
    try:
        admin_db = AdminDB()
        
        # 1. Create a test query first
        print("1. Creating test query...")
        create_result = admin_db.save_custom_query(
            admin_id=1,
            query_name="Test Update Query",
            sql_query="SELECT 1",
            description="Original description",
            category="general",
            is_favorite=False
        )
        print(f"   Create result: {create_result}")
        
        if not create_result['success']:
            print("❌ Failed to create test query")
            return
            
        query_id = create_result['query_id']
        
        # 2. Test update query
        print(f"2. Updating query ID {query_id}...")
        update_result = admin_db.update_custom_query(
            admin_id=1,
            query_id=query_id,
            query_name="Updated Test Query",
            sql_query="SELECT 2",
            category="reports",  # Change category
            description="Updated description"
        )
        print(f"   Update result: {update_result}")
        
        if update_result['success']:
            print("✅ Update query berhasil!")
            
            # 3. Verify the update
            print("3. Verifying update...")
            queries = admin_db.get_admin_custom_queries(1)
            if queries['success']:
                for query in queries['queries']:
                    if query['id'] == query_id:
                        print(f"   Updated query: {query}")
                        print(f"   ✅ Name: {query['name']}")
                        print(f"   ✅ Category: {query['category']}")
                        print(f"   ✅ Description: {query['description']}")
                        print(f"   ✅ SQL: {query['sql_query']}")
                        break
            
            # 4. Clean up
            print("4. Cleaning up...")
            delete_result = admin_db.delete_custom_query(1, query_id)
            print(f"   Delete result: {delete_result}")
            
        else:
            print(f"❌ Update failed: {update_result['message']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_update_query()
