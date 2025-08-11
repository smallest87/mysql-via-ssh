"""
Konfigurasi untuk koneksi MySQL via SSH
Pisahkan konfigurasi dari kode utama untuk keamanan

Author: Julian Sukrisna
Created: August 2025
License: MIT

PENTING: Jangan pernah commit kredensial asli ke GitHub!
- Copy file ini ke config_local.py
- Edit config_local.py dengan kredensial asli
- config_local.py sudah ada di .gitignore
"""

import os
from typing import Dict, Any

# Template konfigurasi SSH Server
SSH_CONFIG = {
    'host': os.getenv('SSH_HOST', 'your-ssh-server.com'),
    'port': int(os.getenv('SSH_PORT', '22')),
    'username': os.getenv('SSH_USERNAME', 'your-ssh-username'),
    'password': os.getenv('SSH_PASSWORD', 'your-ssh-password'),
    
    # Alternatif: gunakan private key (lebih aman)
    # 'private_key_path': os.getenv('SSH_PRIVATE_KEY_PATH', '/path/to/your/private/key'),
    # 'private_key_password': os.getenv('SSH_PRIVATE_KEY_PASSWORD', 'your_key_password'),
}

# Template konfigurasi MySQL Database
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'port': int(os.getenv('MYSQL_PORT', '3306')),
    'username': os.getenv('MYSQL_USERNAME', 'your-mysql-username'),
    'password': os.getenv('MYSQL_PASSWORD', 'your-mysql-password'),
    'database': os.getenv('MYSQL_DATABASE', 'your-database-name'),
}

# Konfigurasi logging
LOGGING_CONFIG = {
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}