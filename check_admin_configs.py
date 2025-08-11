#!/usr/bin/env python3
"""
Test untuk melihat SSH configs di database admin
"""
import sys
import os
sys.path.append('h:/proyek_claude_sonnet/mysql-via-ssh')

from src.database.admin_db import admin_db

def check_admin_ssh_configs():
    """Check SSH configs untuk admin"""
    print("=" * 50)
    print("CHECKING ADMIN SSH CONFIGS")
    print("=" * 50)
    
    # List all admins first
    try:
        import sqlite3
        with sqlite3.connect(admin_db.db_path) as conn:
            cursor = conn.cursor()
            
            # Get admin info
            cursor.execute('SELECT id, username FROM admin_users')
            admins = cursor.fetchall()
            
            print(f"Found {len(admins)} admin(s):")
            for admin_id, username in admins:
                print(f"  Admin ID: {admin_id}, Username: {username}")
                
                # Get SSH configs for this admin
                ssh_configs = admin_db.get_admin_ssh_configs(admin_id)
                print(f"  SSH Configs: {len(ssh_configs)}")
                
                for config in ssh_configs:
                    print(f"    - ID: {config.get('id')}, Name: {config.get('name')}, Last Used: {config.get('last_used')}")
                
                # Check active config
                active_config = admin_db.get_active_ssh_config(admin_id)
                if active_config:
                    print(f"  Active Config: {active_config.get('name')} (ID: {active_config.get('id')})")
                else:
                    print(f"  Active Config: None")
                    
                print()
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_admin_ssh_configs()
