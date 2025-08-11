"""
Script untuk menjalankan contoh penggunaan MySQL SSH Connection
Mengatasi masalah import path dengan struktur folder yang terorganisir
"""

import sys
import os

# Tambahkan src ke Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
config_path = os.path.join(current_dir, 'config')

if src_path not in sys.path:
    sys.path.insert(0, src_path)
if config_path not in sys.path:
    sys.path.insert(0, config_path)

# Import dan jalankan contoh
if __name__ == "__main__":
    # Import contoh usage dari examples
    sys.path.insert(0, os.path.join(current_dir, 'examples'))
    
    # Override import di example_usage
    import database.mysql_ssh_connection
    import config
    
    # Import dan jalankan example
    try:
        from examples.example_usage import test_connection, example_crud_operations
        import logging
        
        logger = logging.getLogger(__name__)
        
        print("🚀 Menjalankan contoh penggunaan MySQL SSH Connection...")
        print("="*60)
        
        # Jalankan test koneksi
        test_connection()
        
        print("\n" + "="*60)
        print("📝 Untuk menjalankan contoh CRUD, uncomment bagian CRUD di example_usage.py")
        print("="*60)
        
    except ImportError as e:
        print(f"❌ Error import: {e}")
        print("💡 Pastikan semua dependencies sudah terinstall dengan: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error: {e}")
