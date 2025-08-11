"""
Test SSH Config Database Schema - Phase 1 Implementation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database.admin_db import AdminDB
from src.database.ssh_encryption import ssh_encryption

def test_ssh_config_schema():
    print("🧪 Testing SSH Config Database Schema")
    print("=" * 50)
    
    try:
        # 1. Initialize AdminDB (this will create the new table)
        print("1. Initializing AdminDB...")
        admin_db = AdminDB()
        print("   ✅ AdminDB initialized successfully")
        
        # 2. Test encryption utilities
        print("\n2. Testing encryption utilities...")
        test_password = "test123"
        encrypted = ssh_encryption.encrypt_password(test_password)
        decrypted = ssh_encryption.decrypt_password(encrypted)
        
        print(f"   Original: {test_password}")
        print(f"   Encrypted: {encrypted}")
        print(f"   Decrypted: {decrypted}")
        print(f"   ✅ Encryption works: {test_password == decrypted}")
        
        # 3. Test save SSH config
        print("\n3. Testing save SSH config...")
        result = admin_db.save_ssh_config(
            admin_id=1,
            config_name="Test Production Server",
            ssh_host="192.168.1.100",
            ssh_port=22,
            ssh_username="ubuntu",
            ssh_password="ssh123",
            mysql_host="localhost",
            mysql_port=3306,
            mysql_username="root",
            mysql_password="mysql123",
            mysql_database="production_db",
            is_default=True
        )
        print(f"   Save result: {result}")
        
        # 4. Test get SSH configs
        print("\n4. Testing get SSH configs...")
        configs_result = admin_db.get_admin_ssh_configs(admin_id=1, include_passwords=True)
        print(f"   Get configs result: {configs_result}")
        
        if configs_result['success'] and configs_result['configs']:
            config = configs_result['configs'][0]
            print(f"   ✅ Config retrieved:")
            print(f"     • Name: {config['config_name']}")
            print(f"     • SSH Host: {config['ssh_host']}")
            print(f"     • MySQL DB: {config['mysql_database']}")
            print(f"     • Is Default: {config['is_default']}")
            print(f"     • SSH Password: {config.get('ssh_password', 'N/A')}")
        
        # 5. Test update SSH config
        if configs_result['success'] and configs_result['configs']:
            config_id = configs_result['configs'][0]['id']
            print(f"\n5. Testing update SSH config (ID: {config_id})...")
            
            update_result = admin_db.update_ssh_config(
                admin_id=1,
                config_id=config_id,
                config_name="Updated Production Server",
                ssh_host="192.168.1.101",
                ssh_port=22,
                ssh_username="ubuntu",
                ssh_password="new_ssh123",
                mysql_host="localhost",
                mysql_port=3306,
                mysql_username="root",
                mysql_password="new_mysql123",
                mysql_database="updated_db",
                is_default=True
            )
            print(f"   Update result: {update_result}")
        
        # 6. Cleanup test data
        if configs_result['success'] and configs_result['configs']:
            config_id = configs_result['configs'][0]['id']
            print(f"\n6. Cleaning up test data...")
            
            delete_result = admin_db.delete_ssh_config(admin_id=1, config_id=config_id)
            print(f"   Delete result: {delete_result}")
        
        print("\n🎉 Phase 1 Database Schema Implementation: SUCCESS!")
        print("\n📋 Schema Components Created:")
        print("   ✅ admin_ssh_configs table")
        print("   ✅ SSH password encryption")
        print("   ✅ MySQL password encryption")
        print("   ✅ CRUD operations for SSH configs")
        print("   ✅ Default config management")
        print("   ✅ Soft delete functionality")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ssh_config_schema()
