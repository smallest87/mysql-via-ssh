# Flask Web UI - MySQL SSH Connection

## 🌐 **Web Interface untuk MySQL SSH Connection**

Flask Web UI menyediakan antarmuka web yang user-friendly untuk mengelola koneksi MySQL melalui SSH tunnel tanpa perlu command line.

### 🎯 **Fitur Utama**

#### 🔗 **Connection Management**
- Form input untuk SSH dan MySQL credentials
- Secure session management
- Real-time connection status
- Auto-disconnect safety

#### 📊 **Database Operations**
- Interactive SQL query executor
- Database and table browser
- Query result visualization
- Query templates for common operations

#### 🎨 **User Experience**
- Responsive Bootstrap UI
- Real-time validation
- Loading states dan progress indicators
- Error handling dengan friendly messages

#### 🛡️ **Security Features**
- Session-based credential storage (tidak persistent)
- Input validation dan sanitization
- CSRF protection ready
- Secure credential handling

## 🚀 **Quick Start**

### 1. Install Dependencies
```bash
# Pastikan Flask dependencies terinstall
pip install flask jinja2 werkzeug

# Atau install semua requirements
pip install -r requirements.txt
```

### 2. Run Flask UI
```bash
# Method 1: Menggunakan runner script
python run_flask_ui.py

# Method 2: Direct Flask app
cd flask_ui
python app.py

# Method 3: Flask command
flask --app flask_ui.app run
```

### 3. Access Web Interface
- **URL**: http://127.0.0.1:5000
- **Browser**: Otomatis terbuka setelah server start
- **Development**: Debug mode enabled untuk development

## 📁 **Struktur Flask UI**

```
flask_ui/
├── app.py                 # Main Flask application
├── templates/             # Jinja2 templates
│   ├── base.html         # Base layout template
│   ├── index.html        # Homepage dengan form koneksi
│   ├── dashboard.html    # Dashboard utama
│   ├── query.html        # SQL query executor
│   └── error.html        # Error pages
└── static/               # Static assets
    ├── css/
    │   └── style.css     # Custom CSS styling
    └── js/
        └── app.js        # JavaScript functionality
```

## 🔧 **Configuration**

### Environment Variables
```bash
# Optional Flask configuration
export FLASK_SECRET_KEY="your-secret-key-for-production"
export FLASK_ENV="development"  # atau "production"
export FLASK_DEBUG=1            # untuk development
```

### Production Deployment
```python
# app.py - Production settings
app.config.update(
    SECRET_KEY=os.environ.get('FLASK_SECRET_KEY', 'change-in-production'),
    SESSION_COOKIE_SECURE=True,    # HTTPS only
    SESSION_COOKIE_HTTPONLY=True,  # Prevent XSS
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1)
)
```

## 🎮 **Usage Guide**

### 1. **Homepage (Connection Form)**
- Input SSH server details (host, port, username, password)
- Input MySQL database details (host, port, username, password, database)
- Click "Buat Koneksi" untuk establish connection
- Validasi otomatis untuk semua input fields

### 2. **Dashboard**
- Overview koneksi yang aktif
- Quick actions (Query, Show Databases, Show Tables)
- Connection information display
- Disconnect option

### 3. **Query Executor**
- SQL query input dengan syntax highlighting
- Query templates untuk common operations
- Real-time query execution
- Tabular result display
- Error handling dan troubleshooting

### 4. **Navigation**
- Persistent navigation bar
- Connection status indicator
- Quick access ke semua features
- About dan support links

## 🔌 **API Endpoints**

### Public Routes
- `GET /` - Homepage dengan connection form
- `POST /connect` - Establish SSH + MySQL connection
- `GET /dashboard` - Main dashboard (requires active connection)
- `GET /query` - SQL query page (requires active connection)
- `GET /disconnect` - Close connections dan redirect to home

### API Routes (AJAX)
- `POST /api/execute_query` - Execute SQL query
- `GET /api/get_databases` - List all databases
- `GET /api/get_tables` - List all tables in current database
- `GET /api/status` - Check connection status

## 🔒 **Security Considerations**

### 📋 **Current Security Measures**
1. **Session-based Storage**: Credentials tidak disimpan di file
2. **Input Validation**: Server-side dan client-side validation
3. **Error Handling**: Prevent information leakage
4. **Secure Headers**: Basic security headers implemented

### ⚠️ **Production Recommendations**
```python
# Additional security for production
app.config.update(
    # HTTPS enforcement
    SESSION_COOKIE_SECURE=True,
    
    # XSS protection
    SESSION_COOKIE_HTTPONLY=True,
    
    # CSRF protection
    WTF_CSRF_ENABLED=True,
    
    # Session timeout
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30)
)

# Rate limiting
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/execute_query', methods=['POST'])
@limiter.limit("10 per minute")
def execute_query():
    # Implementation
```

## 🎨 **UI Components**

### **Bootstrap 5 Framework**
- Responsive grid system
- Modern component library
- Dark/light theme support
- Mobile-first design

### **Font Awesome Icons**
- Consistent iconography
- Professional visual indicators
- Status dan action icons

### **Custom CSS Features**
- Brand-consistent colors
- Smooth animations
- Loading states
- Error states
- Success indicators

### **JavaScript Functionality**
- Form validation
- AJAX operations
- Real-time updates
- Error handling
- User experience enhancements

## 🚀 **Development**

### **Local Development Setup**
```bash
# 1. Activate virtual environment
.venv\Scripts\activate

# 2. Install development dependencies
pip install flask jinja2 werkzeug

# 3. Run dengan debug mode
python run_flask_ui.py

# 4. Access di browser
# http://127.0.0.1:5000
```

### **Code Structure**
```python
# flask_ui/app.py - Main application class
class MySQLSSHFlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.active_connections = {}
    
    def setup_routes(self):
        # Route definitions
        
    def run(self, host='127.0.0.1', port=5000, debug=True):
        # Server startup
```

## 🔄 **Integration dengan Core Library**

### **Seamless Integration**
```python
# Menggunakan core MySQLSSHConnection class
from database.mysql_ssh_connection import MySQLSSHConnection

# Dalam Flask route
mysql_ssh = MySQLSSHConnection(ssh_config, mysql_config)
if mysql_ssh.connect():
    # Store dalam session
    self.active_connections[connection_id] = mysql_ssh
```

### **Shared Configuration**
- Menggunakan config structure yang sama
- Kompatibel dengan existing credential management
- Seamless transition antara CLI dan Web UI

## 📊 **Performance & Scalability**

### **Current Limitations**
- Single-user sessions (1 connection per browser session)
- Memory-based connection storage
- Development server (tidak untuk production scale)

### **Future Enhancements**
- Multi-user support dengan authentication
- Redis session storage untuk scalability
- Connection pooling
- WebSocket untuk real-time updates
- Production WSGI deployment

## 🤝 **Contributing**

### **Adding New Features**
1. Extend `MySQLSSHFlaskApp` class di `app.py`
2. Add new templates di `templates/`
3. Update CSS/JS di `static/`
4. Test dengan development server
5. Update dokumentasi

### **UI Improvements**
1. Modify `templates/base.html` untuk layout changes
2. Update `static/css/style.css` untuk styling
3. Enhance `static/js/app.js` untuk functionality

---

## 👨‍💻 **Author & Support**

**Created by Julian Sukrisna**
- 📧 Email: smallest87@gmail.com
- 🐙 GitHub: [@smallest87](https://github.com/smallest87)
- 🏢 Organization: Javasatu.com

### 💝 **Support This Project**
- ⭐ Star the repository
- 🐛 Report bugs atau request features
- 💰 Donate untuk sustainability
- 📢 Share dengan developer lain

**Flask Web UI memberikan cara yang mudah dan aman untuk menggunakan MySQL SSH Connection tanpa command line!** 🌐✨
