"""
Check Database Schema - admin_custom_queries table
"""

import sqlite3
import os

def check_database_schema():
    db_path = 'config/admin_users.db'
    
    print("🔍 Database Schema Check")
    print("=" * 40)
    
    if not os.path.exists(db_path):
        print(f"❌ Database tidak ditemukan: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='admin_custom_queries'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("❌ Tabel admin_custom_queries tidak ditemukan!")
            print("📋 Tabel yang ada:")
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            for table in tables:
                print(f"  • {table[0]}")
        else:
            print("✅ Tabel admin_custom_queries ditemukan")
            
            # Get table schema
            cursor.execute('PRAGMA table_info(admin_custom_queries)')
            columns = cursor.fetchall()
            
            print("\n📋 Struktur Kolom:")
            for col in columns:
                print(f"  • {col[1]} ({col[2]}) {'NOT NULL' if col[3] else 'NULL'}")
            
            # Check if query_category column exists
            column_names = [col[1] for col in columns]
            if 'query_category' in column_names:
                print("\n✅ Kolom 'query_category' ada!")
            else:
                print("\n❌ Kolom 'query_category' TIDAK ada!")
                print("🔧 Perlu ALTER TABLE untuk menambah kolom")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_database_schema()
