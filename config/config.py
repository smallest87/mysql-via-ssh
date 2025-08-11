"""
Konfigurasi untuk koneksi MySQL via SSH
Pisahkan konfigurasi dari kode utama untuk keamanan
"""

# Konfigurasi SSH Server
SSH_CONFIG = {
    'host': '148.230.96.48',           # IP atau hostname server SSH
    'port': 22,                          # Port SSH (default: 22)
    'username': 'root',     # Username SSH
    'password': 'ManganBeras12##',     # Password SSH
    
    # Alternatif: gunakan private key (lebih aman)
    # 'private_key_path': '/path/to/your/private/key',
    # 'private_key_password': 'your_key_password',  # jika private key punya password
}

# Konfigurasi MySQL Database
MYSQL_CONFIG = {
    'host': 'localhost',                 # Host MySQL di server remote (biasanya localhost)
    'port': 3306,                        # Port MySQL (default: 3306)
    'username': 'smallest87',   # Username MySQL
    'password': 'Rekues76#@Yes',   # Password MySQL
    'database': 'insanpersdb',    # Nama database
}

# Konfigurasi logging
LOGGING_CONFIG = {
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}
