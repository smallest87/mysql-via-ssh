"""
Manual Database Initialization - Force update admin_custom_queries table
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database.admin_db import AdminDB

def force_init_database():
    print("🔧 Force Database Initialization")
    print("=" * 40)
    
    try:
        # Initialize AdminDB (this will create/update tables)
        admin_db = AdminDB()
        print("✅ AdminDB initialized successfully")
        
        # Test creating a sample query to verify database structure
        result = admin_db.save_custom_query(
            admin_id=1,
            query_name="Test Query",
            sql_query="SELECT 1",
            description="Test description",
            category="test",
            is_favorite=False
        )
        
        print(f"📝 Test query save result: {result}")
        
        if result['success']:
            print("✅ Database structure verified - category column works!")
            
            # Clean up test query
            queries = admin_db.get_admin_custom_queries(1)
            if queries['success'] and queries['queries']:
                for query in queries['queries']:
                    if query['name'] == "Test Query":
                        delete_result = admin_db.delete_custom_query(1, query['id'])
                        print(f"🗑️ Test query deleted: {delete_result}")
        else:
            print(f"❌ Database structure issue: {result['message']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    force_init_database()
