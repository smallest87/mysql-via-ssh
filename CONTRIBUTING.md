# Contributing Guidelines

## 🤝 Cara Berkontribusi

### 📋 **Prerequisites**

- Python 3.8 atau lebih tinggi
- Git untuk version control
- Akses ke server SSH dan MySQL untuk testing

### 🛠️ **Setup Development Environment**

1. **Fork dan Clone Repository**
   ```bash
   git clone <your-fork-url>
   cd mysql-ssh-connection
   ```

2. **Setup Virtual Environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .\.venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .  # Install dalam development mode
   ```

### 📝 **Development Workflow**

#### **1. Sebelum Coding**
- Buat branch baru untuk fitur/fix: `git checkout -b feature/nama-fitur`
- Update konfigurasi di `config/config.py` dengan detail server testing Anda

#### **2. Coding Standards**
- Ikuti PEP 8 untuk Python coding style
- Gunakan docstring untuk semua function dan class
- Tambahkan type hints where appropriate
- Gunakan meaningful variable dan function names

#### **3. Testing**
```bash
# Run unit tests
python -m unittest discover tests

# Test manual dengan contoh
python main.py
python run_example.py

# Test specific functionality
cd examples && python example_usage.py
```

#### **4. Documentation**
- Update README.md jika ada perubahan usage
- Tambah dokumentasi di folder `docs/` jika perlu
- Update docstring untuk function/class yang dimodifikasi

### 🧪 **Testing Guidelines**

#### **Unit Tests**
- Letakkan test files di folder `tests/`
- Naming convention: `test_*.py`
- Setiap module harus memiliki test coverage

#### **Integration Tests**
- Test koneksi SSH dan MySQL
- Test dengan berbagai skenario error
- Pastikan cleanup yang proper (tutup koneksi)

#### **Manual Testing**
```bash
# Test berbagai skenario
python main.py                    # Basic functionality
python run_example.py             # Example usage
cd examples && python example_usage.py  # Direct example
```

### 📁 **Struktur Kode**

```
mysql-ssh-connection/
├── src/                    # Source code utama
│   └── database/          # Database modules
├── config/                # Configuration files
├── examples/              # Contoh penggunaan
├── tests/                 # Unit tests
├── docs/                  # Dokumentasi
└── [root files]           # Setup, README, etc.
```

### 🔧 **Build dan Package**

```bash
# Build package
python -m build

# Test package installation
pip install dist/*.whl

# Clean build artifacts
rm -rf build/ dist/ src/*.egg-info/
```

### 📤 **Submit Changes**

#### **1. Pre-submission Checklist**
- [ ] Code mengikuti style guidelines
- [ ] Tests berjalan dengan baik
- [ ] Documentation sudah update
- [ ] No sensitive data dalam commit

#### **2. Commit Guidelines**
```bash
# Commit message format
git commit -m "type: description

Detailed explanation if needed"

# Types: feat, fix, docs, style, refactor, test, chore
```

#### **3. Pull Request**
- Buat PR dari branch feature ke main
- Isi description yang jelas
- Link ke issue yang relevan
- Include screenshots jika ada UI changes

### 🚨 **Security Guidelines**

- **NEVER commit** credentials atau sensitive data
- Gunakan environment variables untuk production config
- Review code untuk potential security issues
- Use secure connection practices

### 🐛 **Bug Reports**

#### **Template Issue**
```markdown
**Bug Description**
Clear description of the issue

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected vs Actual**
- Expected: [description]
- Actual: [description]

**Environment**
- OS: [e.g., Windows 10]
- Python version: [e.g., 3.11.0]
- Package version: [e.g., 1.0.0]

**Additional Context**
Any other relevant information
```

### 💡 **Feature Requests**

#### **Template**
```markdown
**Feature Description**
Clear description of the requested feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How do you envision this working?

**Alternatives Considered**
Other solutions you've considered
```

### ❓ **Questions?**

- Check existing [documentation](docs/)
- Search existing issues
- Create new issue with question label

### 🙏 **Thanks**

Thank you for contributing to MySQL SSH Connection! Your help makes this project better for everyone.

---

**Happy Coding!** 🚀
