"""
Contoh penggunaan MySQL SSH Connection

Untuk menjalankan file ini dari folder examples:
1. cd examples
2. python example_usage.py

Atau jalankan dari root directory:
python -m examples.example_usage
"""

import sys
import os
import logging

# Setup path untuk import
def setup_paths():
    """Setup Python path untuk import modules"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Jika dijalankan dari folder examples
    if os.path.basename(current_dir) == 'examples':
        project_root = os.path.dirname(current_dir)
    else:
        # Jika dijalankan dari root project
        project_root = current_dir
    
    src_path = os.path.join(project_root, 'src')
    config_path = os.path.join(project_root, 'config')
    
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    if config_path not in sys.path:
        sys.path.insert(0, config_path)

# Setup paths before importing
setup_paths()

# Import modules
try:
    from database.mysql_ssh_connection import MySQLSSHConnection
    
    # Import konfigurasi dengan prioritas config_local
    try:
        # Coba import config_local terlebih dahulu (untuk development)
        from config.config_local import SSH_CONFIG, MYSQL_CONFIG, LOGGING_CONFIG
        print("✅ Using local configuration...")
    except ImportError:
        # Fallback ke config template (untuk production/demo)
        from config.config import SSH_CONFIG, MYSQL_CONFIG, LOGGING_CONFIG
        print("⚠️  Using template configuration. Please set environment variables or create config_local.py")
        
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("💡 Pastikan Anda menjalankan script dari folder yang benar:")
    print("   - Dari folder examples: cd examples && python example_usage.py")
    print("   - Dari root project: python run_example.py")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG['level']),
    format=LOGGING_CONFIG['format']
)
logger = logging.getLogger(__name__)

def test_connection():
    """Test koneksi dan operasi dasar database"""
    
    # Buat instance koneksi
    mysql_ssh = MySQLSSHConnection(SSH_CONFIG, MYSQL_CONFIG)
    
    try:
        # Coba koneksi
        if not mysql_ssh.connect():
            logger.error("Gagal membuat koneksi")
            return
            
        logger.info("Koneksi berhasil! Menjalankan test query...")
        
        # Test 1: Lihat versi MySQL
        result = mysql_ssh.execute_query("SELECT VERSION() as version")
        if result:
            logger.info(f"MySQL Version: {result[0]['version']}")
        
        # Test 2: Lihat daftar database
        result = mysql_ssh.execute_query("SHOW DATABASES")
        if result and isinstance(result, list):
            logger.info("Daftar database:")
            for db in result:
                logger.info(f"  - {db['Database']}")
        else:
            logger.info(f"Result type: {type(result)}, Value: {result}")
        
        # Test 3: Lihat daftar tabel (jika database sudah dipilih)
        result = mysql_ssh.execute_query("SHOW TABLES")
        if result and isinstance(result, list):
            logger.info("Daftar tabel:")
            for table in result:
                # Key bisa berbeda tergantung nama database
                table_name = list(table.values())[0]
                logger.info(f"  - {table_name}")
        else:
            logger.info("Tidak ada tabel atau database belum dipilih")
            
    except Exception as e:
        logger.error(f"Error during testing: {str(e)}")
    
    finally:
        # Selalu tutup koneksi
        mysql_ssh.close()

def example_crud_operations():
    """Contoh operasi CRUD (Create, Read, Update, Delete)"""
    
    mysql_ssh = MySQLSSHConnection(SSH_CONFIG, MYSQL_CONFIG)
    
    try:
        if not mysql_ssh.connect():
            logger.error("Gagal membuat koneksi")
            return
            
        # CREATE: Buat tabel contoh (jika belum ada)
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        mysql_ssh.execute_query(create_table_query)
        logger.info("Tabel 'users' sudah siap")
        
        # INSERT: Tambah data
        insert_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        mysql_ssh.execute_query(insert_query, ('John Doe', 'john@example.com'))
        mysql_ssh.execute_query(insert_query, ('Jane Smith', 'jane@example.com'))
        logger.info("Data berhasil ditambahkan")
        
        # SELECT: Baca data
        select_query = "SELECT * FROM users ORDER BY id DESC LIMIT 5"
        users = mysql_ssh.execute_query(select_query)
        if users:
            logger.info("Data users:")
            for user in users:
                logger.info(f"  ID: {user['id']}, Name: {user['name']}, Email: {user['email']}")
        
        # UPDATE: Update data
        update_query = "UPDATE users SET name = %s WHERE email = %s"
        mysql_ssh.execute_query(update_query, ('John Updated', 'john@example.com'))
        logger.info("Data berhasil diupdate")
        
        # DELETE: Hapus data (hati-hati!)
        # delete_query = "DELETE FROM users WHERE email = %s"
        # mysql_ssh.execute_query(delete_query, ('jane@example.com',))
        # logger.info("Data berhasil dihapus")
        
    except Exception as e:
        logger.error(f"Error during CRUD operations: {str(e)}")
    
    finally:
        mysql_ssh.close()

if __name__ == "__main__":
    logger.info("=== Test Koneksi MySQL via SSH ===")
    test_connection()
    
    logger.info("\n=== Contoh Operasi CRUD ===")
    # Uncomment baris berikut untuk menjalankan contoh CRUD
    # example_crud_operations()
