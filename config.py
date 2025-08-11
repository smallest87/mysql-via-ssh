"""
Konfigurasi untuk koneksi MySQL via SSH
Pisahkan konfigurasi dari kode utama untuk keamanan
"""

# Konfigurasi SSH Server
SSH_CONFIG = {
    'host': 'your-server.com',           # IP atau hostname server SSH
    'port': 22,                          # Port SSH (default: 22)
    'username': 'your_ssh_username',     # Username SSH
    'password': 'your_ssh_password',     # Password SSH
    
    # Alternatif: gunakan private key (lebih aman)
    # 'private_key_path': '/path/to/your/private/key',
    # 'private_key_password': 'your_key_password',  # jika private key punya password
}

# Konfigurasi MySQL Database
MYSQL_CONFIG = {
    'host': 'localhost',                 # Host MySQL di server remote (biasanya localhost)
    'port': 3306,                        # Port MySQL (default: 3306)
    'username': 'your_mysql_username',   # Username MySQL
    'password': 'your_mysql_password',   # Password MySQL
    'database': 'your_database_name',    # Nama database
}

# Konfigurasi logging
LOGGING_CONFIG = {
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}
