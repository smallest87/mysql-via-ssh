import sqlite3
import os

print("Database Recreation Script")
print("=" * 30)

db_path = 'config/admin_users.db'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Drop existing table if it has wrong structure
    print("Dropping old admin_custom_queries table...")
    cursor.execute('DROP TABLE IF EXISTS admin_custom_queries')
    
    # Create new table with correct structure
    print("Creating new admin_custom_queries table...")
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
    
    conn.commit()
    
    # Verify schema
    cursor.execute('PRAGMA table_info(admin_custom_queries)')
    columns = cursor.fetchall()
    print("New table columns:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    conn.close()
    print("Database recreation completed!")
else:
    print("Database not found!")
