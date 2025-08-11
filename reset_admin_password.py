#!/usr/bin/env python3
"""
Reset admin password untuk debugging

Author: AI Assistant
Date: 2025-08-11
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.admin_db import admin_db
import sqlite3
import hashlib

def reset_admin_passwords():
    """Reset password admin untuk debugging"""
    print("🔧 Resetting admin passwords...")
    
    salt = "mysql_ssh_admin_salt_2025"
    
    # Reset password untuk admin
    admin_password = "admin"
    admin_hash = hashlib.sha256((admin_password + salt).encode()).hexdigest()
    
    # Reset password untuk Julian  
    julian_password = "password"
    julian_hash = hashlib.sha256((julian_password + salt).encode()).hexdigest()
    
    try:
        with sqlite3.connect(admin_db.db_path) as conn:
            cursor = conn.cursor()
            
            # Update admin password
            cursor.execute('''
                UPDATE admin_users 
                SET password_hash = ? 
                WHERE username = 'admin'
            ''', (admin_hash,))
            
            # Update Julian password
            cursor.execute('''
                UPDATE admin_users 
                SET password_hash = ? 
                WHERE username = 'Julian'
            ''', (julian_hash,))
            
            conn.commit()
            print("✅ Admin passwords reset successfully!")
            print(f"  admin: {admin_password}")
            print(f"  Julian: {julian_password}")
            
            # Test authentication
            print("\n🧪 Testing authentication:")
            auth1 = admin_db.authenticate_admin('admin', 'admin')
            auth2 = admin_db.authenticate_admin('Julian', 'password')
            
            print(f"  admin auth: {'✅ Success' if auth1 else '❌ Failed'}")
            print(f"  Julian auth: {'✅ Success' if auth2 else '❌ Failed'}")
            
            if auth1:
                print(f"  admin ID: {auth1['id']}")
            if auth2:
                print(f"  Julian ID: {auth2['id']}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    reset_admin_passwords()
