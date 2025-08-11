# 🔐 Panduan Keamanan - MySQL SSH Connection

## ⚠️ PENTING: Keamanan Kredensial

**JANGAN PERNAH** commit file dengan kredensial asli ke repository public!

## 🛡️ Metode Keamanan

### 1. **Config Local (Development)**
```bash
# Copy template dan edit dengan kredensial asli
cp config/config.py config/config_local.py
# Edit config_local.py dengan kredensial asli
# File ini sudah ada di .gitignore
```

### 2. **Environment Variables (Production)**
```bash
# Buat file .env dari template
cp .env.template .env
# Edit .env dengan kredensial asli
# File ini sudah ada di .gitignore
```

### 3. **SSH Private Key (Paling Aman)**
```python
# Gunakan private key instead of password
SSH_CONFIG = {
    'host': 'your-server.com',
    'username': 'your-user',
    'private_key_path': '/path/to/private/key',
    'private_key_password': 'key_password_if_any'
}
```

## 📁 File yang Aman untuk GitHub

### ✅ Boleh di-commit:
- `config/config.py` (template dengan placeholder)
- `.env.template` (template environment variables)
- Semua file dokumentasi
- Source code tanpa kredensial

### ❌ JANGAN di-commit:
- `config/config_local.py` (kredensial asli)
- `.env` (environment variables asli)
- File dengan suffix `*_credentials.py`, `*_secrets.py`
- File dengan kredensial hardcoded

## 🔍 Cek Keamanan Sebelum Push

```bash
# Cek apakah ada file sensitif yang akan di-commit
git status

# Cek isi file yang akan di-commit
git diff --cached

# Pastikan .gitignore sudah benar
cat .gitignore | grep -E "(config_local|\.env|credentials|secrets)"
```

## 🚨 Jika Kredensial Sudah Ter-commit

1. **SEGERA ganti semua password/key**
2. **Hapus dari git history:**
   ```bash
   # Hapus file dari history
   git filter-branch --force --index-filter \
   'git rm --cached --ignore-unmatch config/config_local.py' \
   --prune-empty --tag-name-filter cat -- --all
   
   # Force push
   git push --force --all
   ```

## 🔄 Best Practices

1. **Gunakan SSH Key Authentication** (lebih aman dari password)
2. **Rotate credentials** secara berkala
3. **Gunakan environment variables** di production
4. **Audit git log** sebelum push ke public repo
5. **Setup branch protection** di GitHub

## 📝 Contoh Setup untuk Tim

```bash
# Setiap developer membuat config_local.py sendiri
echo "config/config_local.py" >> .gitignore
echo ".env" >> .gitignore

# Bagikan template via dokumentasi, bukan file
# Developer setup sendiri dengan kredensial mereka
```

---
**Catatan**: File ini hanya panduan. Selalu ikuti security policy organisasi Anda.
