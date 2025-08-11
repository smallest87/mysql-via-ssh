"""
MySQL Connection via SSH Tunnel
Script untuk koneksi ke database MySQL melalui SSH tunnel
"""

import pymysql
import sshtunnel
from sshtunnel import SSHTunnelForwarder
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MySQLSSHConnection:
    def __init__(self, ssh_config, mysql_config):
        """
        Inisialisasi koneksi MySQL via SSH
        
        Args:
            ssh_config (dict): Konfigurasi SSH server
            mysql_config (dict): Konfigurasi MySQL database
            
        Raises:
            TypeError: Jika ssh_config atau mysql_config bukan dict atau None
            ValueError: Jika konfigurasi tidak lengkap
        """
        # Validasi input
        if ssh_config is None or mysql_config is None:
            raise TypeError("ssh_config dan mysql_config tidak boleh None")
            
        if not isinstance(ssh_config, dict) or not isinstance(mysql_config, dict):
            raise TypeError("ssh_config dan mysql_config harus berupa dictionary")
            
        # Validasi field yang wajib ada
        required_ssh_fields = ['host', 'port', 'username']
        required_mysql_fields = ['host', 'port', 'username', 'password', 'database']
        
        for field in required_ssh_fields:
            if field not in ssh_config:
                raise ValueError(f"Field '{field}' wajib ada di ssh_config")
                
        for field in required_mysql_fields:
            if field not in mysql_config:
                raise ValueError(f"Field '{field}' wajib ada di mysql_config")
        
        self.ssh_config = ssh_config
        self.mysql_config = mysql_config
        self.tunnel = None
        self.connection = None
        
    def connect(self):
        """Membuat koneksi SSH tunnel dan MySQL"""
        try:
            # Membuat SSH tunnel
            logger.info("Membuat SSH tunnel...")
            self.tunnel = SSHTunnelForwarder(
                (self.ssh_config['host'], self.ssh_config['port']),
                ssh_username=self.ssh_config['username'],
                ssh_password=self.ssh_config.get('password'),
                ssh_pkey=self.ssh_config.get('private_key_path'),
                ssh_private_key_password=self.ssh_config.get('private_key_password'),
                remote_bind_address=(self.mysql_config['host'], self.mysql_config['port']),
                local_bind_address=('127.0.0.1', 0)  # 0 untuk auto-assign port
            )
            
            self.tunnel.start()
            logger.info(f"SSH tunnel berhasil dibuat di port lokal: {self.tunnel.local_bind_port}")
            
            # Membuat koneksi MySQL
            logger.info("Menghubungkan ke MySQL database...")
            self.connection = pymysql.connect(
                host='127.0.0.1',
                port=self.tunnel.local_bind_port,
                user=self.mysql_config['username'],
                password=self.mysql_config['password'],
                database=self.mysql_config['database'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            
            logger.info("Koneksi MySQL berhasil!")
            return True
            
        except Exception as e:
            logger.error(f"Error saat koneksi: {str(e)}")
            self.close()
            return False
    
    def execute_query(self, query, params=None):
        """
        Eksekusi query SQL
        
        Args:
            query (str): Query SQL
            params (tuple): Parameter untuk query (optional)
            
        Returns:
            list: Hasil query
        """
        if not self.connection:
            logger.error("Tidak ada koneksi aktif")
            return None
            
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                # Check if query returns results (SELECT, SHOW, DESCRIBE, EXPLAIN, etc.)
                query_type = query.strip().upper()
                if any(query_type.startswith(cmd) for cmd in ['SELECT', 'SHOW', 'DESCRIBE', 'DESC', 'EXPLAIN']):
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
                    return cursor.rowcount
                    
        except Exception as e:
            logger.error(f"Error saat eksekusi query: {str(e)}")
            self.connection.rollback()
            return None
    
    def close(self):
        """Menutup koneksi MySQL dan SSH tunnel"""
        if self.connection:
            self.connection.close()
            logger.info("Koneksi MySQL ditutup")
            
        if self.tunnel and self.tunnel.is_active:
            self.tunnel.stop()
            logger.info("SSH tunnel ditutup")

def main():
    """Contoh penggunaan"""
    
    # Konfigurasi SSH Server
    ssh_config = {
        'host': 'your-server.com',          # Ganti dengan IP/hostname SSH server
        'port': 22,                         # Port SSH (default: 22)
        'username': 'your_ssh_username',    # Username SSH
        'password': 'your_ssh_password',    # Password SSH (opsional jika pakai key)
        # 'private_key_path': '/path/to/private/key',  # Path ke private key (opsional)
        # 'private_key_password': 'key_password',      # Password private key (opsional)
    }
    
    # Konfigurasi MySQL Database
    mysql_config = {
        'host': 'localhost',                # Host MySQL di server remote (biasanya localhost)
        'port': 3306,                       # Port MySQL (default: 3306)
        'username': 'your_mysql_username',  # Username MySQL
        'password': 'your_mysql_password',  # Password MySQL
        'database': 'your_database_name',   # Nama database
    }
    
    # Membuat koneksi
    mysql_ssh = MySQLSSHConnection(ssh_config, mysql_config)
    
    if mysql_ssh.connect():
        try:
            # Contoh query SELECT
            logger.info("Menjalankan query SELECT...")
            result = mysql_ssh.execute_query("SHOW TABLES")
            if result:
                logger.info(f"Daftar tabel: {result}")
            
            # Contoh query dengan parameter
            # result = mysql_ssh.execute_query(
            #     "SELECT * FROM users WHERE id = %s", 
            #     (1,)
            # )
            
            # Contoh INSERT
            # mysql_ssh.execute_query(
            #     "INSERT INTO users (name, email) VALUES (%s, %s)",
            #     ('John Doe', 'john@example.com')
            # )
            
        except Exception as e:
            logger.error(f"Error saat menjalankan operasi database: {str(e)}")
        
        finally:
            # Selalu tutup koneksi
            mysql_ssh.close()
    else:
        logger.error("Gagal membuat koneksi")

if __name__ == "__main__":
    main()
