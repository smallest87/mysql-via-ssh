#!/usr/bin/env python3
"""
Force update database schema untuk workspace tables

Author: AI Assistant
Date: 2025-08-11
"""

import sys
import os
import sqlite3

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.admin_db import admin_db

def force_create_workspace_tables():
    """Force create workspace tables"""
    print("🔧 Force creating workspace tables...")
    
    try:
        with sqlite3.connect(admin_db.db_path) as conn:
            cursor = conn.cursor()
            
            # Create admin_custom_queries table
            print("📝 Creating admin_custom_queries table...")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS admin_custom_queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    admin_id INTEGER NOT NULL,
                    query_name TEXT NOT NULL,
                    query_description TEXT,
                    sql_query TEXT NOT NULL,
                    query_category TEXT DEFAULT 'general',
                    is_favorite BOOLEAN DEFAULT 0,
                    execution_count INTEGER DEFAULT 0,
                    last_executed TIMESTAMP NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (admin_id) REFERENCES admin_users(id),
                    UNIQUE(admin_id, query_name)
                )
            ''')
            
            # Create admin_workspace_settings table
            print("⚙️ Creating admin_workspace_settings table...")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS admin_workspace_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    admin_id INTEGER NOT NULL,
                    setting_key TEXT NOT NULL,
                    setting_value TEXT,
                    setting_type TEXT DEFAULT 'string',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (admin_id) REFERENCES admin_users(id),
                    UNIQUE(admin_id, setting_key)
                )
            ''')
            
            # Create admin_query_history table
            print("📊 Creating admin_query_history table...")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS admin_query_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    admin_id INTEGER NOT NULL,
                    query_id INTEGER,
                    query_name TEXT,
                    sql_query TEXT NOT NULL,
                    execution_status TEXT DEFAULT 'success',
                    execution_time_ms INTEGER,
                    rows_affected INTEGER,
                    error_message TEXT,
                    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (admin_id) REFERENCES admin_users(id),
                    FOREIGN KEY (query_id) REFERENCES admin_custom_queries(id)
                )
            ''')
            
            conn.commit()
            print("✅ All workspace tables created successfully!")
            
            # Verify tables exist
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name LIKE 'admin_%'
                ORDER BY name
            """)
            
            tables = cursor.fetchall()
            print(f"\n📋 Current admin tables ({len(tables)}):")
            for table in tables:
                print(f"  ✅ {table[0]}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Force Update Database Schema")
    print("=" * 40)
    
    if force_create_workspace_tables():
        print("\n🎉 Schema update completed!")
        print("Now run: python test_workspace.py")
    else:
        print("\n❌ Schema update failed!")
