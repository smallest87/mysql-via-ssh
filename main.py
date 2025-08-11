"""
Main entry point untuk MySQL SSH Connection

Author: Julian Sukrisna
Created: August 2025
License: MIT
"""

import sys
import os
import logging

# Tambahkan path src dan config ke Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'src'))
sys.path.append(os.path.join(current_dir, 'config'))

from src.database.mysql_ssh_connection import MySQLSSHConnection

# Import konfigurasi dengan prioritas config_local
try:
    # Coba import config_local terlebih dahulu (untuk development)
    from config.config_local import SSH_CONFIG, MYSQL_CONFIG, LOGGING_CONFIG
    print("✅ Using local configuration...")
except ImportError:
    # Fallback ke config template (untuk production/demo)
    from config.config import SSH_CONFIG, MYSQL_CONFIG, LOGGING_CONFIG
    print("⚠️  Using template configuration. Please set environment variables or create config_local.py")

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG['level']),
    format=LOGGING_CONFIG['format']
)
logger = logging.getLogger(__name__)

def main():
    """Fungsi utama untuk menjalankan aplikasi"""
    
    logger.info("=== MySQL SSH Connection Application ===")
    
    # Buat instance koneksi
    mysql_ssh = MySQLSSHConnection(SSH_CONFIG, MYSQL_CONFIG)
    
    try:
        # Coba koneksi
        if not mysql_ssh.connect():
            logger.error("Gagal membuat koneksi")
            return False
            
        logger.info("Koneksi berhasil! Menjalankan test query...")
        
        # Test query
        result = mysql_ssh.execute_query("SELECT VERSION() as version")
        if result:
            logger.info(f"MySQL Version: {result[0]['version']}")
        
        # Lihat daftar database
        result = mysql_ssh.execute_query("SHOW DATABASES")
        if result and isinstance(result, list):
            logger.info("Daftar database:")
            for db in result:
                logger.info(f"  - {db['Database']}")
        
        # Lihat daftar tabel
        result = mysql_ssh.execute_query("SHOW TABLES")
        if result and isinstance(result, list):
            logger.info("Daftar tabel:")
            for table in result:
                table_name = list(table.values())[0]
                logger.info(f"  - {table_name}")
        else:
            logger.info("Tidak ada tabel atau database belum dipilih")
            
        return True
            
    except Exception as e:
        logger.error(f"Error during operation: {str(e)}")
        return False
    
    finally:
        # Selalu tutup koneksi
        mysql_ssh.close()

if __name__ == "__main__":
    success = main()
    if success:
        logger.info("Aplikasi selesai dengan sukses")
    else:
        logger.error("Aplikasi selesai dengan error")
        sys.exit(1)
