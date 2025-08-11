# Struktur Project

Struktur folder project ini mengikuti konvensi umum dalam pemrograman Python:

```
mysql-via-ssh/
├── src/                          # Source code utama
│   ├── __init__.py              # Package initializer
│   └── database/                # Module database
│       ├── __init__.py          # Database package initializer
│       └── mysql_ssh_connection.py  # Class utama untuk koneksi
├── config/                      # File konfigurasi
│   ├── __init__.py              # Config package initializer
│   └── config.py                # Konfigurasi SSH dan MySQL
├── examples/                    # Contoh penggunaan
│   └── example_usage.py         # Contoh lengkap dengan CRUD
├── tests/                       # Unit tests
│   ├── __init__.py              # Test package initializer
│   └── test_mysql_ssh_connection.py  # Test cases
├── .venv/                       # Virtual environment
├── main.py                      # Entry point utama
├── setup.py                     # Setup script untuk instalasi
├── requirements.txt             # Dependencies
├── README.md                    # Dokumentasi utama
├── STRUCTURE.md                 # Dokumentasi struktur (file ini)
└── .gitignore                   # Git ignore rules
```

## Penjelasan Folder

### 📁 **src/** - Source Code
Folder utama yang berisi kode aplikasi:
- `__init__.py`: Membuat folder menjadi Python package
- `database/`: Module untuk semua operasi database
  - `mysql_ssh_connection.py`: Class utama untuk koneksi MySQL via SSH

### 📁 **config/** - Konfigurasi
Berisi file-file konfigurasi:
- `config.py`: Konfigurasi SSH server dan MySQL database

### 📁 **examples/** - Contoh Penggunaan
Berisi file-file contoh:
- `example_usage.py`: Contoh penggunaan lengkap dengan operasi CRUD

### 📁 **tests/** - Unit Tests
Berisi file-file testing:
- `test_mysql_ssh_connection.py`: Unit tests untuk class utama

### 📄 **Root Files**
- `main.py`: Entry point utama aplikasi
- `setup.py`: Script untuk instalasi package
- `requirements.txt`: Daftar dependencies
- `README.md`: Dokumentasi utama

## Cara Menjalankan

### 🚀 **Metode 1: Langsung dari main.py**
```bash
python main.py
```

### 🚀 **Metode 2: Dari examples**
```bash
cd examples
python example_usage.py
```

### 🧪 **Menjalankan Tests**
```bash
cd tests
python -m unittest test_mysql_ssh_connection.py
```

## Keuntungan Struktur Ini

1. **Separation of Concerns**: Setiap folder memiliki tujuan yang jelas
2. **Maintainability**: Mudah untuk maintenance dan development
3. **Testability**: Struktur yang mendukung unit testing
4. **Reusability**: Source code bisa dijadikan package
5. **Professional**: Mengikuti best practices Python development
