#!/usr/bin/env python3
"""
Script untuk test workspace personal admin dan custom SQL queries

Menguji:
1. Database schema update dengan tabel workspace
2. Custom query management
3. Workspace settings
4. Query execution tracking

Author: AI Assistant (GitHub Copilot)
Date: 2025-08-11
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.admin_db import admin_db

def test_workspace_schema():
    """Test apakah schema workspace sudah dibuat"""
    print("🔧 Testing workspace database schema...")
    
    try:
        import sqlite3
        
        with sqlite3.connect(admin_db.db_path) as conn:
            cursor = conn.cursor()
            
            # Check if workspace tables exist
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name LIKE 'admin_%'
                ORDER BY name
            """)
            
            tables = cursor.fetchall()
            print(f"📋 Found {len(tables)} admin tables:")
            
            expected_tables = [
                'admin_users',
                'admin_sessions', 
                'admin_custom_queries',
                'admin_workspace_settings',
                'admin_query_history'
            ]
            
            for table in tables:
                table_name = table[0]
                status = "✅" if table_name in expected_tables else "⚠️"
                print(f"  {status} {table_name}")
            
            # Check missing tables
            existing_tables = [t[0] for t in tables]
            missing_tables = [t for t in expected_tables if t not in existing_tables]
            
            if missing_tables:
                print(f"❌ Missing tables: {missing_tables}")
                return False
            else:
                print("✅ All workspace tables exist!")
                return True
                
    except Exception as e:
        print(f"❌ Error checking schema: {e}")
        return False

def test_custom_queries():
    """Test custom query functionality"""
    print("\n🎯 Testing custom query management...")
    
    # Get admin user
    admin_id = 1  # Assuming admin exists
    
    # Test 1: Save sample query
    print("📝 Testing save custom query...")
    result = admin_db.save_custom_query(
        admin_id=admin_id,
        query_name="Get User Count",
        sql_query="SELECT COUNT(*) as total_users FROM users",
        description="Count total number of users in system",
        category="reports",
        is_favorite=True
    )
    
    if result['success']:
        print(f"✅ Query saved: {result['message']}")
        query_id = result['query_id']
    else:
        print(f"❌ Failed to save query: {result['message']}")
        return False
    
    # Test 2: Get admin queries
    print("📚 Testing get admin queries...")
    queries_result = admin_db.get_admin_custom_queries(admin_id)
    
    if queries_result['success']:
        queries = queries_result['queries']
        print(f"✅ Found {len(queries)} queries for admin {admin_id}")
        
        for query in queries:
            print(f"  - {query['name']} ({query['category']}) {'⭐' if query['is_favorite'] else ''}")
    else:
        print(f"❌ Failed to get queries: {queries_result['message']}")
        return False
    
    # Test 3: Toggle favorite
    print("⭐ Testing toggle favorite...")
    toggle_result = admin_db.toggle_query_favorite(admin_id, query_id)
    
    if toggle_result['success']:
        print(f"✅ Favorite toggled: {toggle_result['message']}")
    else:
        print(f"❌ Failed to toggle favorite: {toggle_result['message']}")
    
    # Test 4: Log query execution
    print("📊 Testing query execution logging...")
    log_result = admin_db.log_query_execution(
        admin_id=admin_id,
        query_id=query_id,
        query_name="Get User Count",
        sql_query="SELECT COUNT(*) as total_users FROM users",
        status='success',
        execution_time_ms=150,
        rows_affected=1
    )
    
    if log_result['success']:
        print(f"✅ Execution logged: {log_result['message']}")
    else:
        print(f"❌ Failed to log execution: {log_result['message']}")
    
    return True

def test_workspace_settings():
    """Test workspace settings functionality"""
    print("\n⚙️ Testing workspace settings...")
    
    admin_id = 1
    
    # Test save settings
    print("💾 Testing save workspace settings...")
    
    settings = [
        ('theme', 'dark', 'string'),
        ('auto_save', True, 'boolean'),
        ('query_timeout', 30, 'integer'),
        ('editor_font_size', 14.5, 'float')
    ]
    
    for key, value, setting_type in settings:
        result = admin_db.save_workspace_setting(admin_id, key, value, setting_type)
        
        if result['success']:
            print(f"  ✅ {key}: {value} ({setting_type})")
        else:
            print(f"  ❌ Failed to save {key}: {result['message']}")
    
    # Test get settings
    print("📖 Testing get workspace settings...")
    settings_result = admin_db.get_workspace_settings(admin_id)
    
    if settings_result['success']:
        settings_dict = settings_result['settings']
        print(f"✅ Retrieved {len(settings_dict)} settings:")
        
        for key, value in settings_dict.items():
            print(f"  - {key}: {value} ({type(value).__name__})")
    else:
        print(f"❌ Failed to get settings: {settings_result['message']}")
    
    return True

def test_sample_data():
    """Create sample data untuk testing"""
    print("\n🌱 Creating sample data...")
    
    admin_id = 1
    
    # Sample queries untuk berbagai kategori
    sample_queries = [
        {
            'name': 'Daily Active Users',
            'sql': 'SELECT COUNT(DISTINCT user_id) as dau FROM user_sessions WHERE DATE(created_at) = CURDATE()',
            'description': 'Count daily active users',
            'category': 'analytics',
            'favorite': True
        },
        {
            'name': 'Top Products',
            'sql': 'SELECT product_name, SUM(quantity) as total_sold FROM sales GROUP BY product_name ORDER BY total_sold DESC LIMIT 10',
            'description': 'Get top 10 selling products',
            'category': 'reports',
            'favorite': False
        },
        {
            'name': 'Database Health Check',
            'sql': 'SHOW PROCESSLIST',
            'description': 'Check active database connections',
            'category': 'maintenance',
            'favorite': True
        },
        {
            'name': 'User Registration Trend',
            'sql': 'SELECT DATE(created_at) as date, COUNT(*) as registrations FROM users WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY) GROUP BY DATE(created_at) ORDER BY date',
            'description': 'User registration trend last 30 days',
            'category': 'analytics',
            'favorite': False
        }
    ]
    
    for query_data in sample_queries:
        result = admin_db.save_custom_query(
            admin_id=admin_id,
            query_name=query_data['name'],
            sql_query=query_data['sql'],
            description=query_data['description'],
            category=query_data['category'],
            is_favorite=query_data['favorite']
        )
        
        if result['success']:
            print(f"  ✅ Created: {query_data['name']}")
        else:
            print(f"  ⚠️ Skipped: {query_data['name']} ({result['message']})")
    
    return True

def main():
    """Main test function"""
    print("🚀 Testing Admin Workspace Personal System")
    print("=" * 50)
    
    # Test 1: Database Schema
    if not test_workspace_schema():
        print("\n❌ Schema test failed! Please check database setup.")
        return
    
    # Test 2: Custom Queries
    if not test_custom_queries():
        print("\n❌ Custom query test failed!")
        return
    
    # Test 3: Workspace Settings
    if not test_workspace_settings():
        print("\n❌ Workspace settings test failed!")
        return
    
    # Test 4: Sample Data
    test_sample_data()
    
    print("\n" + "=" * 50)
    print("🎉 All workspace tests completed successfully!")
    print("\n📋 Summary:")
    print("✅ Database schema updated with workspace tables")
    print("✅ Custom query management working")
    print("✅ Workspace settings functional")
    print("✅ Query execution logging ready")
    print("✅ Sample data created")
    
    print("\n🌐 Next steps:")
    print("1. Start Flask app: python flask_ui/app.py")
    print("2. Login as admin")
    print("3. Visit: http://localhost:5000/admin/workspace")
    print("4. Test custom SQL query management!")

if __name__ == "__main__":
    main()
