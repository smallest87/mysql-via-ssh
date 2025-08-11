# Dokumentasi MySQL SSH Connection

## 📚 Daftar Dokumentasi

### 📖 **Dokumentasi Utama**
- [README.md](../README.md) - Dokumentasi utama proyek
- [STORY.md](../STORY.md) - **Cerita di balik proyek dan sustainabilitas**
- [STRUCTURE.md](STRUCTURE.md) - Struktur folder dan organisasi proyek

### 🔧 **Setup dan Development**
- [BUILD_SETUP.md](BUILD_SETUP.md) - Setup system, build tools, dan packaging
- [IMPORT_SOLUTION.md](IMPORT_SOLUTION.md) - Solusi masalah import dan Pylance

### 🤝 **Community dan Support**
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Guidelines untuk kontributor
- [SUPPORT.md](../SUPPORT.md) - **Cara mendukung proyek ini**
- [AUTHORS.md](../AUTHORS.md) - Daftar kontributor

### 📁 **Struktur Dokumentasi**

```
docs/
├── README.md                 # Index dokumentasi (file ini)
├── STRUCTURE.md             # Struktur proyek
├── BUILD_SETUP.md           # Setup dan build system
└── IMPORT_SOLUTION.md       # Solusi masalah import
```

### 🚀 **Quick Start**

1. **Setup Environment**:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Konfigurasi**:
   - Edit `config/config.py` dengan detail server Anda

3. **Menjalankan**:
   ```bash
   python main.py              # Entry point utama
   python run_example.py       # Contoh penggunaan
   ```

4. **Development**:
   ```bash
   pip install -e .            # Install development mode
   python -m unittest discover tests  # Run tests
   ```

### 📋 **Troubleshooting**

- **Import Issues**: Lihat [IMPORT_SOLUTION.md](IMPORT_SOLUTION.md)
- **Build Problems**: Lihat [BUILD_SETUP.md](BUILD_SETUP.md)  
- **Structure Questions**: Lihat [STRUCTURE.md](STRUCTURE.md)

### 🔗 **Links**

- **Main README**: [../README.md](../README.md)
- **Configuration**: [../config/config.py](../config/config.py)
- **Examples**: [../examples/](../examples/)
- **Tests**: [../tests/](../tests/)
