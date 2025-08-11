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

## 🔐 Konfigurasi Keamanan

**⚠️ PENTING: Jangan pernah commit kredensial asli ke repository!**

### Setup Kredensial

**Option A: Local Config File (Development)**
```bash
# Copy template dan edit dengan kredensial asli
cp config/config.py config/config_local.py
# Edit config_local.py dengan kredensial asli
# File ini sudah ada di .gitignore
```

**Option B: Environment Variables (Production)**
```bash
# Copy template dan edit dengan kredensial asli
cp .env.template .env
# Edit .env dengan kredensial asli  
# File ini sudah ada di .gitignore
```

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

## 🚀 Penggunaan

### 🌐 Flask Web UI (Recommended)
```bash
# 1. Setup environment
.venv\Scripts\activate    # Windows
pip install -r requirements.txt

# 2. Setup kredensial (untuk development)
cp config/config.py config/config_local.py    # Edit dengan kredensial asli

# 3. Start Flask Web Interface
python run_flask_ui.py

# Browser akan otomatis terbuka ke http://127.0.0.1:5000
# Interface web yang user-friendly untuk MySQL SSH connections!
```

### 💻 Command Line Interface
```bash
# 1. Setup environment  
.venv\Scripts\activate    # Windows
pip install -r requirements.txt

# 2. Setup kredensial (pilih salah satu)
cp config/config.py config/config_local.py    # Edit dengan kredensial asli
cp .env.template .env                          # Edit dengan kredensial asli

# 3. Run aplikasi
python main.py
```

### Menjalankan Contoh
```bash
# Metode 1: Entry point utama
python main.py

# Metode 2: Alternative runner
python run_example.py

# Metode 3: Dari folder examples
cd examples && python example_usage.py
```

### Development
```bash
# Install dalam development mode
pip install -e .

# Run tests
python -m unittest discover tests

# Build package
python -m build
```

### Basic Usage
```python
from src.database.mysql_ssh_connection import MySQLSSHConnection
from config.config import SSH_CONFIG, MYSQL_CONFIG

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

- `src/database/mysql_ssh_connection.py` - Class utama untuk koneksi
- `config/config.py` - Konfigurasi SSH dan MySQL
- `examples/example_usage.py` - Contoh penggunaan dan test
- `tests/test_mysql_ssh_connection.py` - Unit tests
- `docs/` - Dokumentasi lengkap
- `main.py` - Entry point utama
- `run_example.py` - Alternative runner untuk examples

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

## 🔐 Security Tips

**📖 Baca panduan lengkap: [SECURITY.md](docs/SECURITY.md)**

1. **Gunakan Private Key**: Lebih aman dari password
2. **Environment Variables**: Simpan kredensial di environment variables  
3. **Config Local**: Gunakan `config_local.py` untuk development
4. **Never Commit Credentials**: Jangan pernah commit kredensial ke repository
5. **Firewall**: Pastikan server SSH dan MySQL dikonfigurasi dengan benar
6. **VPN**: Pertimbangkan menggunakan VPN untuk keamanan ekstra

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

## 📚 Documentation

Dokumentasi lengkap tersedia di folder [`docs/`](docs/):

- [🔐 Security Guide](docs/SECURITY.md) - **Panduan keamanan kredensial**
- [📁 Structure Guide](docs/STRUCTURE.md) - Struktur proyek dan organisasi
- [🔧 Build Setup](docs/BUILD_SETUP.md) - Setup system dan build tools  
- [🔧 Import Solutions](docs/IMPORT_SOLUTION.md) - Solusi masalah import

## 👨‍💻 Author

**Created by Julian Sukrisna**
- 📧 Email: smallest87@gmail.com
- 🐙 GitHub: [@smallest87](https://github.com/smallest87)
- 🏢 Organization: Javasatu.com
- 📅 Created: August 2025

## 📖 Project Story

Baca cerita lengkap di balik pengembangan proyek ini di [STORY.md](STORY.md) - perjalanan profesional, tantangan ekonomi, dan visi masa depan proyek ini.

## 💝 Support This Project

Proyek ini dikembangkan dengan dedikasi tinggi untuk memberikan solusi koneksi database yang aman dan profesional. Dalam masa ekonomi yang menantang, dukungan Anda sangat berarti untuk keberlanjutan pengembangan.

### 🎯 **Mengapa Mendukung Proyek Ini?**
- Memastikan pemeliharaan dan keamanan berkelanjutan
- Mendukung pengembangan fitur-fitur baru
- Membantu stabilitas ekonomi developer di masa sulit
- Berkontribusi pada ekosistem open source Indonesia

### 💰 **Cara Mendukung:**
- 💳 **Donasi**: Lihat detail di [SUPPORT.md](SUPPORT.md)
- ⭐ **GitHub Star**: Berikan star pada repository ini
- 📢 **Share**: Bagikan ke developer lain
- 🤝 **Contribute**: Lihat [CONTRIBUTING.md](CONTRIBUTING.md)

**Setiap dukungan, sekecil apapun, sangat berarti untuk keberlanjutan proyek ini.** 🙏

## 🤝 Contributing

Ingin berkontribusi? Silakan baca [CONTRIBUTING.md](CONTRIBUTING.md) untuk guidelines development.

Lihat juga [AUTHORS.md](AUTHORS.md) untuk daftar lengkap kontributor.

## 📄 License

Project ini menggunakan [MIT License](LICENSE).

---

**Happy Coding!** 🚀
