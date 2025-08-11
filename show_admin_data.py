import sqlite3
import os

# Path ke database admin
db_path = r"h:\proyek_claude_sonnet\mysql-via-ssh\config\admin_users.db"

print("🗄️ ADMIN DATABASE CONTENT")
print("=" * 50)

try:
    if os.path.exists(db_path):
        print(f"📁 Database found at: {db_path}")
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Get all admin users
            cursor.execute('''
                SELECT id, username, email, full_name, role, is_active, 
                       created_at, last_login, login_count
                FROM admin_users 
                ORDER BY id
            ''')
            
            admins = cursor.fetchall()
            
            if admins:
                print(f"\n👥 Total Admin Users: {len(admins)}")
                print("-" * 80)
                print(f"{'ID':<3} {'Username':<12} {'Email':<20} {'Full Name':<15} {'Role':<10} {'Active':<7} {'Login Count':<11}")
                print("-" * 80)
                
                for admin in admins:
                    id_val = admin[0]
                    username = admin[1] or 'N/A'
                    email = admin[2] or 'N/A'
                    full_name = admin[3] or 'N/A'
                    role = admin[4] or 'admin'
                    is_active = 'Yes' if admin[5] else 'No'
                    login_count = admin[8] or 0
                    
                    print(f"{id_val:<3} {username:<12} {email:<20} {full_name:<15} {role:<10} {is_active:<7} {login_count:<11}")
                
                print("\n📊 SUMMARY:")
                active_count = sum(1 for admin in admins if admin[5])
                print(f"   • Active Admins: {active_count}")
                print(f"   • Inactive Admins: {len(admins) - active_count}")
                
                # Show detailed info for each admin
                print("\n📝 DETAILED INFO:")
                print("-" * 50)
                for admin in admins:
                    print(f"\n🔹 Admin ID: {admin[0]}")
                    print(f"   Username: {admin[1]}")
                    print(f"   Email: {admin[2]}")
                    print(f"   Full Name: {admin[3]}")
                    print(f"   Role: {admin[4]}")
                    print(f"   Status: {'Active' if admin[5] else 'Inactive'}")
                    print(f"   Created: {admin[6]}")
                    print(f"   Last Login: {admin[7] or 'Never'}")
                    print(f"   Login Count: {admin[8] or 0}")
                    
            else:
                print("\n❌ No admin users found in database!")
                
    else:
        print(f"❌ Database file not found at: {db_path}")
        print("\n💡 Database will be created when you first run the Flask app.")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 50)
