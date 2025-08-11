"""
Database Explorer untuk Admin Users
Menampilkan semua data admin dalam database SQLite

Author: Julian Sukrisna
Organization: Javasatu.com
"""

import sqlite3
import os
from datetime import datetime

def explore_admin_database():
    """Explore dan tampilkan data dari admin database"""
    
    # Path ke database
    db_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'admin_users.db')
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            print("=" * 60)
            print("🗄️  ADMIN DATABASE EXPLORER")
            print("=" * 60)
            
            # Check if database exists and has tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            if not tables:
                print("❌ Database kosong atau tidak ditemukan!")
                return
            
            print(f"📁 Database Location: {db_path}")
            print(f"📊 Tables Found: {[table[0] for table in tables]}")
            print()
            
            # EXPLORE ADMIN_USERS TABLE
            print("👥 ADMIN USERS TABLE")
            print("-" * 60)
            
            cursor.execute('''
                SELECT id, username, email, full_name, role, is_active, 
                       created_at, last_login, login_count
                FROM admin_users 
                ORDER BY created_at DESC
            ''')
            
            admin_users = cursor.fetchall()
            
            if admin_users:
                print(f"📈 Total Admin Users: {len(admin_users)}")
                print()
                
                # Header
                print(f"{'ID':<3} {'Username':<15} {'Full Name':<20} {'Email':<25} {'Role':<12} {'Active':<8} {'Created':<12} {'Last Login':<12} {'Count':<5}")
                print("-" * 120)
                
                # Data rows
                for admin in admin_users:
                    id_val = admin[0]
                    username = admin[1][:14] if admin[1] else 'N/A'
                    full_name = admin[3][:19] if admin[3] else 'N/A'
                    email = admin[2][:24] if admin[2] else 'N/A'
                    role = admin[4] or 'admin'
                    is_active = '✅ Yes' if admin[5] else '❌ No'
                    created = admin[6].split(' ')[0] if admin[6] else 'N/A'
                    last_login = admin[7].split(' ')[0] if admin[7] else 'Never'
                    login_count = admin[8] or 0
                    
                    print(f"{id_val:<3} {username:<15} {full_name:<20} {email:<25} {role:<12} {is_active:<8} {created:<12} {last_login:<12} {login_count:<5}")
                
                print()
                
                # Statistics
                active_count = sum(1 for admin in admin_users if admin[5])
                inactive_count = len(admin_users) - active_count
                super_admin_count = sum(1 for admin in admin_users if admin[4] == 'super_admin' and admin[5])
                
                print("📊 STATISTICS:")
                print(f"   • Total Admins: {len(admin_users)}")
                print(f"   • Active: {active_count}")
                print(f"   • Inactive: {inactive_count}")
                print(f"   • Super Admins: {super_admin_count}")
                
            else:
                print("📭 No admin users found!")
            
            print()
            
            # EXPLORE ADMIN_SESSIONS TABLE (if exists)
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='admin_sessions';")
            if cursor.fetchone():
                print("🔐 ADMIN SESSIONS TABLE")
                print("-" * 60)
                
                cursor.execute('''
                    SELECT COUNT(*) as total_sessions,
                           COUNT(CASE WHEN is_active = 1 THEN 1 END) as active_sessions
                    FROM admin_sessions
                ''')
                
                session_stats = cursor.fetchone()
                if session_stats:
                    print(f"📈 Total Sessions: {session_stats[0]}")
                    print(f"🔄 Active Sessions: {session_stats[1]}")
                
                # Recent sessions
                cursor.execute('''
                    SELECT s.id, u.username, s.ip_address, s.created_at, s.is_active
                    FROM admin_sessions s
                    JOIN admin_users u ON s.admin_id = u.id
                    ORDER BY s.created_at DESC
                    LIMIT 5
                ''')
                
                recent_sessions = cursor.fetchall()
                if recent_sessions:
                    print()
                    print("🕒 Recent Sessions (Last 5):")
                    print(f"{'ID':<5} {'Username':<15} {'IP Address':<15} {'Created':<20} {'Active':<8}")
                    print("-" * 70)
                    
                    for session in recent_sessions:
                        session_id = session[0]
                        username = session[1][:14]
                        ip_addr = session[2][:14] if session[2] else 'N/A'
                        created = session[3][:19] if session[3] else 'N/A'
                        is_active = '✅ Yes' if session[4] else '❌ No'
                        
                        print(f"{session_id:<5} {username:<15} {ip_addr:<15} {created:<20} {is_active:<8}")
            
            print()
            print("=" * 60)
            print("✅ Database exploration completed!")
            
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def search_admin_by_username(username):
    """Cari admin berdasarkan username"""
    
    db_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'admin_users.db')
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, username, email, full_name, role, is_active, 
                       created_at, last_login, login_count
                FROM admin_users 
                WHERE username LIKE ?
            ''', (f'%{username}%',))
            
            results = cursor.fetchall()
            
            if results:
                print(f"🔍 Search Results for '{username}':")
                print("-" * 60)
                
                for admin in results:
                    print(f"ID: {admin[0]}")
                    print(f"Username: {admin[1]}")
                    print(f"Email: {admin[2]}")
                    print(f"Full Name: {admin[3]}")
                    print(f"Role: {admin[4]}")
                    print(f"Active: {'Yes' if admin[5] else 'No'}")
                    print(f"Created: {admin[6]}")
                    print(f"Last Login: {admin[7] or 'Never'}")
                    print(f"Login Count: {admin[8] or 0}")
                    print("-" * 40)
            else:
                print(f"❌ No admin found with username containing '{username}'")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Admin Database Explorer")
    print("=" * 40)
    
    while True:
        print("\nChoose option:")
        print("1. Show all admin users")
        print("2. Search admin by username")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            explore_admin_database()
        elif choice == "2":
            username = input("Enter username to search: ").strip()
            if username:
                search_admin_by_username(username)
            else:
                print("❌ Username cannot be empty!")
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please enter 1, 2, or 3.")
