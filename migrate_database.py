"""
Database Migration Script - Add missing columns to admin_custom_queries
"""

import sqlite3
import os

def migrate_database():
    print("🔧 Database Migration - admin_custom_queries")
    print("=" * 50)
    
    db_path = 'config/admin_users.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database tidak ditemukan: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check existing tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in cursor.fetchall()]
        print(f"📋 Tables ditemukan: {tables}")
        
        if 'admin_custom_queries' not in tables:
            print("❌ Tabel admin_custom_queries tidak ditemukan, membuat ulang...")
            
            # Create admin_custom_queries table with all required columns
            cursor.execute('''
                CREATE TABLE admin_custom_queries (
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
            print("✅ Tabel admin_custom_queries dibuat dengan lengkap")
        else:
            # Check current schema
            cursor.execute('PRAGMA table_info(admin_custom_queries)')
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            print(f"📋 Kolom saat ini: {column_names}")
            
            # Check if query_category exists
            if 'query_category' not in column_names:
                print("🔧 Menambah kolom query_category...")
                cursor.execute('ALTER TABLE admin_custom_queries ADD COLUMN query_category TEXT DEFAULT "general"')
                print("✅ Kolom query_category ditambahkan")
            else:
                print("✅ Kolom query_category sudah ada")
            
            # Check other missing columns
            required_columns = [
                ('query_description', 'TEXT'),
                ('is_favorite', 'BOOLEAN DEFAULT 0'),
                ('execution_count', 'INTEGER DEFAULT 0'),
                ('last_executed', 'TIMESTAMP NULL'),
                ('created_at', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'),
                ('updated_at', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
            ]
            
            for col_name, col_type in required_columns:
                if col_name not in column_names:
                    print(f"🔧 Menambah kolom {col_name}...")
                    cursor.execute(f'ALTER TABLE admin_custom_queries ADD COLUMN {col_name} {col_type}')
                    print(f"✅ Kolom {col_name} ditambahkan")
        
        # Commit changes
        conn.commit()
        
        # Verify final schema
        cursor.execute('PRAGMA table_info(admin_custom_queries)')
        final_columns = cursor.fetchall()
        print("\n📋 Schema Final:")
        for col in final_columns:
            print(f"  • {col[1]} ({col[2]}) {'NOT NULL' if col[3] else 'NULL'}")
        
        conn.close()
        print("\n🎉 Database migration completed!")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")

if __name__ == "__main__":
    migrate_database()
