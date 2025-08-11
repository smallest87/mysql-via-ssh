#!/usr/bin/env python3
"""
Script untuk debug admin session dan workspace

Author: AI Assistant
Date: 2025-08-11
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.admin_db import admin_db

def debug_admin_session():
    """Debug admin users dan authentication"""
    print("🔍 Debug Admin Session & Authentication")
    print("=" * 50)
    
    # 1. Check admin users
    print("📋 Current admin users:")
    all_admins = admin_db.get_all_admins()
    
    if isinstance(all_admins, list) and len(all_admins) > 0:
        for admin in all_admins:
            print(f"  ID: {admin['id']}, Username: {admin['username']}, Active: {admin['is_active']}")
    else:
        print(f"  ❌ No admins found or error occurred")
    
    # 2. Test authentication
    print("\n🔐 Testing authentication:")
    test_users = [
        ('admin', 'admin'),
        ('Julian', 'password')
    ]
    
    for username, password in test_users:
        print(f"\n  Testing {username}...")
        auth_result = admin_db.authenticate_admin(username, password)
        
        if auth_result:
            print(f"    ✅ Success! User ID: {auth_result['id']}")
            print(f"    Details: {auth_result}")
            
            # Test save query dengan admin ID ini
            print(f"    🧪 Testing save query...")
            query_result = admin_db.save_custom_query(
                admin_id=auth_result['id'],
                query_name="Test Debug Query",
                sql_query="SELECT 1 as test",
                description="Debug test query",
                category="debug"
            )
            print(f"    Query save result: {query_result}")
            
        else:
            print(f"    ❌ Authentication failed")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    debug_admin_session()
