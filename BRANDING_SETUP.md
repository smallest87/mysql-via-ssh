# Personal Branding Setup

Ganti semua placeholder berikut dengan informasi Anda:

## 🔧 Find and Replace All

### Identitas Personal
```
[YOUR_FULL_NAME]          → Nama lengkap Anda
[YOUR_EMAIL@domain.com]   → Email Anda
[YOUR_GITHUB_USERNAME]    → Username GitHub Anda
```

### File yang Perlu Diupdate
- `pyproject.toml` - Author dan maintainer info
- `AUTHORS.md` - Detail kontributor utama
- `README.md` - Author section
- `LICENSE` - Copyright holder
- `src/database/mysql_ssh_connection.py` - Header copyright
- `main.py` - Author comment
- `config/config.py` - Author comment

### Contoh Penggunaan
```bash
# Jika nama Anda "John Doe" dengan email "john.doe@example.com" dan GitHub "johndoe"
[YOUR_FULL_NAME] → John Doe
[YOUR_EMAIL@domain.com] → john.doe@example.com  
[YOUR_GITHUB_USERNAME] → johndoe
```

### Script Otomatis (Opsional)
Buat script PowerShell untuk replace semua sekaligus:

```powershell
$files = @(
    "pyproject.toml",
    "AUTHORS.md", 
    "README.md",
    "LICENSE",
    "src\database\mysql_ssh_connection.py",
    "main.py",
    "config\config.py"
)

$name = "John Doe"  # Ganti dengan nama Anda
$email = "john.doe@example.com"  # Ganti dengan email Anda  
$github = "johndoe"  # Ganti dengan username GitHub Anda

foreach ($file in $files) {
    if (Test-Path $file) {
        (Get-Content $file) | 
        ForEach-Object { $_ -replace '\[YOUR_FULL_NAME\]', $name } |
        ForEach-Object { $_ -replace '\[YOUR_EMAIL@domain\.com\]', $email } |
        ForEach-Object { $_ -replace '\[YOUR_GITHUB_USERNAME\]', $github } |
        Set-Content $file
        Write-Host "Updated: $file"
    }
}
```

## 🎯 Result

Setelah update, identitas Anda akan tercatat di:
1. **Package Metadata** (pyproject.toml)
2. **Copyright License** (LICENSE)
3. **Documentation** (README.md, AUTHORS.md)
4. **Source Code Headers** (semua file .py)
5. **Git History** (commit messages)

Ini memastikan kontribusi Anda terdokumentasi dengan baik untuk profesional portfolio! 🚀
