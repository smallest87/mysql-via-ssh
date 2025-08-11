#!/usr/bin/env python3
"""
Flask UI Runner untuk MySQL SSH Connection

Author: Julian Sukrisna
Organization: Javasatu.com
Created: August 2025
License: MIT

Script untuk menjalankan Flask web interface
"""

import os
import sys
import webbrowser
from threading import Timer

# Tambahkan path untuk import
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, '..'))

def open_browser():
    """Buka browser setelah server Flask siap"""
    webbrowser.open('http://127.0.0.1:5000')

def main():
    """Main function untuk menjalankan Flask UI"""
    
    print("=" * 60)
    print("🚀 MySQL SSH Connection - Web UI")
    print("📧 Author: Julian Sukrisna (smallest87@gmail.com)")
    print("🏢 Organization: Javasatu.com")
    print("=" * 60)
    print()
    
    try:
        # Import Flask app
        from flask_ui.app import MySQLSSHFlaskApp
        
        # Buat instance aplikasi
        app_instance = MySQLSSHFlaskApp()
        
        print("🌐 Starting Flask development server...")
        print("📡 URL: http://127.0.0.1:5000")
        print("🔒 Security: Credentials are not stored permanently")
        print("⚠️  Warning: Development server - not for production!")
        print()
        print("Press Ctrl+C to stop the server")
        print("-" * 60)
        
        # Buka browser setelah 1.5 detik
        Timer(1.5, open_browser).start()
        
        # Jalankan Flask app
        app_instance.run(
            host='127.0.0.1',
            port=5000,
            debug=True
        )
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print()
        print("💡 Pastikan Flask sudah terinstall:")
        print("   pip install flask")
        print()
        print("💡 Atau install semua dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("👋 Thank you for using MySQL SSH Connection UI!")
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 For help, visit:")
        print("   https://github.com/smallest87/mysql-ssh-connection")
        sys.exit(1)

if __name__ == '__main__':
    main()
