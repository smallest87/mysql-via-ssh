# MySQL via SSH Tunnel - Python

Script Python untuk koneksi ke database MySQL melalui SSH tunnel. Berguna ketika database MySQL tidak dapat diakses langsung dari internet dan hanya bisa diakses melalui SSH server.

## Fitur

- Koneksi aman ke MySQL melalui SSH tunnel
- Support autentikasi SSH dengan password atau private key
- Class wrapper yang mudah digunakan
- Logging yang informatif
- Contoh operasi CRUD
- Penanganan error yang baik

## Instalasi

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Konfigurasi

Edit file `config.py` dengan detail koneksi Anda:

### SSH Configuration
```python
SSH_CONFIG = {
    'host': 'your-server.com',           # IP atau hostname server SSH
    'port': 22,                          # Port SSH
    'username': 'your_ssh_username',     # Username SSH
    'password': 'your_ssh_password',     # Password SSH
}
```

### MySQL Configuration
```python
MYSQL_CONFIG = {
    'host': 'localhost',                 # Host MySQL di server remote
    'port': 3306,                        # Port MySQL
    'username': 'your_mysql_username',   # Username MySQL
    'password': 'your_mysql_password',   # Password MySQL
    'database': 'your_database_name',    # Nama database
}
```

### Menggunakan Private Key (Lebih Aman)
```python
SSH_CONFIG = {
    'host': 'your-server.com',
    'port': 22,
    'username': 'your_ssh_username',
    'private_key_path': '/path/to/your/private/key',
    'private_key_password': 'your_key_password',  # jika private key punya password
}
```

## Penggunaan

### Basic Usage
```python
from mysql_ssh_connection import MySQLSSHConnection
from config import SSH_CONFIG, MYSQL_CONFIG

# Buat koneksi
mysql_ssh = MySQLSSHConnection(SSH_CONFIG, MYSQL_CONFIG)

if mysql_ssh.connect():
    # Jalankan query
    result = mysql_ssh.execute_query("SELECT * FROM users")
    print(result)
    
    # Tutup koneksi
    mysql_ssh.close()
```

### Menjalankan Contoh
```bash
python example_usage.py
```

## File Structure

- `mysql_ssh_connection.py` - Class utama untuk koneksi
- `config.py` - Konfigurasi SSH dan MySQL
- `example_usage.py` - Contoh penggunaan dan test
- `requirements.txt` - Dependencies yang dibutuhkan

## Operasi yang Didukung

### SELECT
```python
result = mysql_ssh.execute_query("SELECT * FROM users WHERE id = %s", (1,))
```

### INSERT
```python
mysql_ssh.execute_query(
    "INSERT INTO users (name, email) VALUES (%s, %s)",
    ('John Doe', 'john@example.com')
)
```

### UPDATE
```python
mysql_ssh.execute_query(
    "UPDATE users SET name = %s WHERE id = %s",
    ('New Name', 1)
)
```

### DELETE
```python
mysql_ssh.execute_query("DELETE FROM users WHERE id = %s", (1,))
```

## Security Tips

1. **Gunakan Private Key**: Lebih aman dari password
2. **Environment Variables**: Simpan kredensial di environment variables
3. **Firewall**: Pastikan server SSH dan MySQL dikonfigurasi dengan benar
4. **VPN**: Pertimbangkan menggunakan VPN untuk keamanan ekstra

## Troubleshooting

### SSH Connection Failed
- Periksa hostname/IP dan port SSH
- Pastikan username dan password/private key benar
- Periksa firewall dan network connectivity

### MySQL Connection Failed
- Pastikan MySQL service berjalan di server
- Periksa username dan password MySQL
- Pastikan user MySQL memiliki permission yang cukup

### Permission Denied
- Periksa permission private key file (chmod 600)
- Pastikan user SSH memiliki akses ke server

## Example Output
```
2024-01-01 10:00:00 - mysql_ssh_connection - INFO - Membuat SSH tunnel...
2024-01-01 10:00:01 - mysql_ssh_connection - INFO - SSH tunnel berhasil dibuat di port lokal: 55432
2024-01-01 10:00:02 - mysql_ssh_connection - INFO - Menghubungkan ke MySQL database...
2024-01-01 10:00:03 - mysql_ssh_connection - INFO - Koneksi MySQL berhasil!
```
