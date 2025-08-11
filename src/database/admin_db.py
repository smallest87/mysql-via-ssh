"""
Admin Database Management untuk MySQL SSH Connection

A                # Create admin_sessions table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS admin_sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        admin_id INTEGER NOT NULL,
                        session_token TEXT UNIQUE NOT NULL,
                        ip_address TEXT,
                        user_agent TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        expires_at TIMESTAMP NOT NULL,
                        is_active BOOLEAN DEFAULT 1,
                        FOREIGN KEY (admin_id) REFERENCES admin_users(id)
                    )
                ''')
                
                # Create admin_custom_queries table untuk workspace personal
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS admin_custom_queries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        admin_id INTEGER NOT NULL,
                        query_name TEXT NOT NULL,
                        query_description TEXT,
                        sql_query TEXT NOT NULL,
                        query_category TEXT DEFAULT 'general',
                        is_favorite BOOLEAN DEFAULT 0,
                        execution_count INTEGER DEFAULT 0,
                        last_executed TIMESTAMP NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (admin_id) REFERENCES admin_users(id),
                        UNIQUE(admin_id, query_name)
                    )
                ''')
                
                # Create admin_workspace_settings table untuk konfigurasi personal
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS admin_workspace_settings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        admin_id INTEGER NOT NULL,
                        setting_key TEXT NOT NULL,
                        setting_value TEXT,
                        setting_type TEXT DEFAULT 'string',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (admin_id) REFERENCES admin_users(id),
                        UNIQUE(admin_id, setting_key)
                    )
                ''')
                
                # Create admin_query_history table untuk tracking eksekusi
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS admin_query_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        admin_id INTEGER NOT NULL,
                        query_id INTEGER,
                        query_name TEXT,
                        sql_query TEXT NOT NULL,
                        execution_status TEXT DEFAULT 'success',
                        execution_time_ms INTEGER,
                        rows_affected INTEGER,
                        error_message TEXT,
                        executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (admin_id) REFERENCES admin_users(id),
                        FOREIGN KEY (query_id) REFERENCES admin_custom_queries(id)
                    )
                ''')Sukrisna
Organization: Javasatu.com
Created: August 2025

Mengelola database SQLite untuk admin users dengan password hashing
dan validasi credentials yang aman.
"""

import sqlite3
import hashlib
import os
from datetime import datetime
import logging
from typing import Optional, List, Dict, Any

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdminDB:
    def __init__(self, db_path: str = None):
        """
        Initialize Admin Database
        
        Args:
            db_path: Path ke database SQLite. Jika None, gunakan default path.
        """
        if db_path is None:
            # Default path di config directory
            config_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'config')
            os.makedirs(config_dir, exist_ok=True)
            db_path = os.path.join(config_dir, 'admin_users.db')
        
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Inisialisasi database dan tabel admin users"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create admin_users table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS admin_users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        full_name TEXT NOT NULL,
                        role TEXT DEFAULT 'admin',
                        is_active BOOLEAN DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP NULL,
                        login_count INTEGER DEFAULT 0
                    )
                ''')
                
                # Create admin_sessions table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS admin_sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        admin_id INTEGER NOT NULL,
                        session_token TEXT UNIQUE NOT NULL,
                        ip_address TEXT,
                        user_agent TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        expires_at TIMESTAMP NOT NULL,
                        is_active BOOLEAN DEFAULT 1,
                        FOREIGN KEY (admin_id) REFERENCES admin_users (id)
                    )
                ''')
                
                # Create default admin if not exists
                self._create_default_admin()
                
                conn.commit()
                logger.info("Database admin users berhasil diinisialisasi")
                
        except Exception as e:
            logger.error(f"Error inisialisasi database: {e}")
            raise
    
    def _hash_password(self, password: str) -> str:
        """Hash password menggunakan SHA-256 dengan salt"""
        salt = "mysql_ssh_admin_salt_2025"  # Dalam produksi, gunakan salt random per user
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def _create_default_admin(self):
        """Buat admin default jika belum ada"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if default admin exists
                cursor.execute("SELECT id FROM admin_users WHERE username = ?", ("admin",))
                if cursor.fetchone() is None:
                    # Create default admin
                    password_hash = self._hash_password("admin123")
                    cursor.execute('''
                        INSERT INTO admin_users 
                        (username, email, password_hash, full_name, role)
                        VALUES (?, ?, ?, ?, ?)
                    ''', ("admin", "admin@javasatu.com", password_hash, "Default Administrator", "super_admin"))
                    
                    logger.info("Default admin user berhasil dibuat")
                    
        except Exception as e:
            logger.error(f"Error membuat default admin: {e}")
    
    def create_admin(self, username: str, email: str, password: str, 
                     full_name: str, role: str = "admin") -> bool:
        """
        Buat admin user baru
        
        Args:
            username: Username unik
            email: Email unik
            password: Password plain text (akan di-hash)
            full_name: Nama lengkap
            role: Role admin (admin/super_admin)
            
        Returns:
            bool: True jika berhasil, False jika gagal
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Hash password
                password_hash = self._hash_password(password)
                
                # Insert new admin
                cursor.execute('''
                    INSERT INTO admin_users 
                    (username, email, password_hash, full_name, role)
                    VALUES (?, ?, ?, ?, ?)
                ''', (username, email, password_hash, full_name, role))
                
                conn.commit()
                logger.info(f"Admin user '{username}' berhasil dibuat")
                return True
                
        except sqlite3.IntegrityError as e:
            if "username" in str(e):
                logger.error(f"Username '{username}' sudah digunakan")
            elif "email" in str(e):
                logger.error(f"Email '{email}' sudah digunakan")
            else:
                logger.error(f"Integrity error: {e}")
            return False
        except Exception as e:
            logger.error(f"Error membuat admin: {e}")
            return False
    
    def authenticate_admin(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Autentikasi admin user
        
        Args:
            username: Username
            password: Password plain text
            
        Returns:
            Dict dengan data admin jika berhasil, None jika gagal
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Hash password yang diberikan
                password_hash = self._hash_password(password)
                
                # Query admin dengan username dan password hash
                cursor.execute('''
                    SELECT id, username, email, full_name, role, is_active, 
                           created_at, last_login, login_count
                    FROM admin_users 
                    WHERE username = ? AND password_hash = ? AND is_active = 1
                ''', (username, password_hash))
                
                result = cursor.fetchone()
                if result:
                    # Update last login dan login count
                    admin_id = result[0]
                    cursor.execute('''
                        UPDATE admin_users 
                        SET last_login = CURRENT_TIMESTAMP, 
                            login_count = login_count + 1
                        WHERE id = ?
                    ''', (admin_id,))
                    
                    conn.commit()
                    
                    # Return admin data
                    return {
                        'id': result[0],
                        'username': result[1],
                        'email': result[2],
                        'full_name': result[3],
                        'role': result[4],
                        'is_active': result[5],
                        'created_at': result[6],
                        'last_login': result[7],
                        'login_count': result[8] + 1  # Include the current login
                    }
                else:
                    logger.warning(f"Login gagal untuk username: {username}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error autentikasi admin: {e}")
            return None
    
    def get_all_admins(self) -> List[Dict[str, Any]]:
        """Ambil semua admin users yang aktif (tanpa password hash)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT id, username, email, full_name, role, is_active,
                           created_at, last_login, login_count
                    FROM admin_users 
                    WHERE is_active = 1
                    ORDER BY created_at DESC
                ''')
                
                results = cursor.fetchall()
                admins = []
                
                for row in results:
                    admins.append({
                        'id': row[0],
                        'username': row[1],
                        'email': row[2],
                        'full_name': row[3],
                        'role': row[4],
                        'is_active': row[5],
                        'created_at': row[6],
                        'last_login': row[7],
                        'login_count': row[8]
                    })
                
                return admins
                
        except Exception as e:
            logger.error(f"Error mengambil data admin: {e}")
            return []
    
    def update_admin_status(self, admin_id: int, is_active: bool) -> bool:
        """Update status aktif admin"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE admin_users 
                    SET is_active = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (is_active, admin_id))
                
                conn.commit()
                logger.info(f"Status admin ID {admin_id} berhasil diupdate ke {is_active}")
                return True
                
        except Exception as e:
            logger.error(f"Error update status admin: {e}")
            return False
    
    def delete_admin(self, admin_id: int) -> bool:
        """Hapus admin user (soft delete dengan set is_active = 0)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Cek apakah admin yang akan dihapus adalah super_admin terakhir
                cursor.execute('''
                    SELECT COUNT(*) FROM admin_users 
                    WHERE role = 'super_admin' AND is_active = 1 AND id != ?
                ''', (admin_id,))
                
                super_admin_count = cursor.fetchone()[0]
                
                # Cek role admin yang akan dihapus
                cursor.execute('SELECT role FROM admin_users WHERE id = ?', (admin_id,))
                admin_role = cursor.fetchone()
                
                if admin_role and admin_role[0] == 'super_admin' and super_admin_count == 0:
                    logger.error("Tidak dapat menghapus super admin terakhir")
                    return False
                
                # Soft delete
                cursor.execute('''
                    UPDATE admin_users 
                    SET is_active = 0, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (admin_id,))
                
                conn.commit()
                logger.info(f"Admin ID {admin_id} berhasil dihapus (soft delete)")
                return True
                
        except Exception as e:
            logger.error(f"Error hapus admin: {e}")
            return False
    
    def get_admin_stats(self) -> Dict[str, Any]:
        """Ambil statistik admin users"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total admin aktif
                cursor.execute('SELECT COUNT(*) FROM admin_users WHERE is_active = 1')
                total_active = cursor.fetchone()[0]
                
                # Total admin tidak aktif
                cursor.execute('SELECT COUNT(*) FROM admin_users WHERE is_active = 0')
                total_inactive = cursor.fetchone()[0]
                
                # Admin dengan login terakhir (7 hari)
                cursor.execute('''
                    SELECT COUNT(*) FROM admin_users 
                    WHERE last_login >= datetime('now', '-7 days') AND is_active = 1
                ''')
                recent_logins = cursor.fetchone()[0]
                
                return {
                    'total_active': total_active,
                    'total_inactive': total_inactive,
                    'total_all': total_active + total_inactive,
                    'recent_logins': recent_logins
                }
                
        except Exception as e:
            logger.error(f"Error mengambil stats admin: {e}")
            return {
                'total_active': 0,
                'total_inactive': 0, 
                'total_all': 0,
                'recent_logins': 0
            }
    
    # ============= WORKSPACE MANAGEMENT METHODS =============
    
    def save_custom_query(self, admin_id, query_name, sql_query, description=None, category='general', is_favorite=False):
        """Simpan custom query untuk admin workspace"""
        try:
            if not admin_id:
                return {'success': False, 'message': 'Admin ID is required'}
                
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO admin_custom_queries 
                    (admin_id, query_name, query_description, sql_query, query_category, is_favorite, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ''', (admin_id, query_name, description, sql_query, category, is_favorite))
                
                query_id = cursor.lastrowid
                logger.info(f"Custom query '{query_name}' saved for admin {admin_id}")
                return {'success': True, 'query_id': query_id, 'message': 'Query berhasil disimpan'}
                
        except sqlite3.IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                return {'success': False, 'message': f'Query dengan nama "{query_name}" sudah ada'}
            return {'success': False, 'message': f'Error database: {e}'}
        except Exception as e:
            logger.error(f"Error menyimpan custom query: {e}")
            return {'success': False, 'message': f'Error: {e}'}
    
    def get_admin_custom_queries(self, admin_id, category=None, favorites_only=False):
        """Ambil semua custom queries untuk admin"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = '''
                    SELECT id, query_name, query_description, sql_query, query_category, 
                           is_favorite, execution_count, last_executed, created_at, updated_at
                    FROM admin_custom_queries 
                    WHERE admin_id = ?
                '''
                params = [admin_id]
                
                if category:
                    query += ' AND query_category = ?'
                    params.append(category)
                
                if favorites_only:
                    query += ' AND is_favorite = 1'
                
                query += ' ORDER BY is_favorite DESC, query_name ASC'
                
                cursor.execute(query, params)
                queries = []
                
                for row in cursor.fetchall():
                    queries.append({
                        'id': row[0],
                        'name': row[1],
                        'description': row[2],
                        'sql_query': row[3],
                        'category': row[4],
                        'is_favorite': bool(row[5]),
                        'execution_count': row[6],
                        'last_executed': row[7],
                        'created_at': row[8],
                        'updated_at': row[9]
                    })
                
                return {'success': True, 'queries': queries}
                
        except Exception as e:
            logger.error(f"Error mengambil custom queries: {e}")
            return {'success': False, 'message': f'Error: {e}', 'queries': []}
    
    def delete_custom_query(self, admin_id, query_id):
        """Hapus custom query"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Pastikan query milik admin yang benar
                cursor.execute('''
                    DELETE FROM admin_custom_queries 
                    WHERE id = ? AND admin_id = ?
                ''', (query_id, admin_id))
                
                if cursor.rowcount > 0:
                    logger.info(f"Custom query {query_id} deleted by admin {admin_id}")
                    return {'success': True, 'message': 'Query berhasil dihapus'}
                else:
                    return {'success': False, 'message': 'Query tidak ditemukan atau bukan milik Anda'}
                    
        except Exception as e:
            logger.error(f"Error menghapus custom query: {e}")
            return {'success': False, 'message': f'Error: {e}'}
    
    def update_custom_query(self, admin_id, query_id, query_name, sql_query, category='uncategorized', description=''):
        """Update custom query yang sudah ada"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Pastikan query milik admin yang benar
                cursor.execute('''
                    SELECT id FROM admin_custom_queries 
                    WHERE id = ? AND admin_id = ?
                ''', (query_id, admin_id))
                
                if not cursor.fetchone():
                    return {'success': False, 'message': 'Query tidak ditemukan atau bukan milik Anda'}
                
                # Update query
                cursor.execute('''
                    UPDATE admin_custom_queries 
                    SET query_name = ?, sql_query = ?, query_category = ?, query_description = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ? AND admin_id = ?
                ''', (query_name, sql_query, category, description, query_id, admin_id))
                
                logger.info(f"Custom query '{query_name}' updated by admin {admin_id}")
                return {'success': True, 'message': 'Query berhasil diperbarui', 'query_id': query_id}
                
        except Exception as e:
            logger.error(f"Error mengupdate custom query: {e}")
            return {'success': False, 'message': f'Error: {e}'}
    
    def toggle_query_favorite(self, admin_id, query_id):
        """Toggle status favorite query"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Ambil status favorite saat ini
                cursor.execute('''
                    SELECT is_favorite FROM admin_custom_queries 
                    WHERE id = ? AND admin_id = ?
                ''', (query_id, admin_id))
                
                result = cursor.fetchone()
                if not result:
                    return {'success': False, 'message': 'Query tidak ditemukan'}
                
                new_favorite = not bool(result[0])
                
                cursor.execute('''
                    UPDATE admin_custom_queries 
                    SET is_favorite = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ? AND admin_id = ?
                ''', (new_favorite, query_id, admin_id))
                
                status = "ditambahkan ke" if new_favorite else "dihapus dari"
                return {'success': True, 'message': f'Query {status} favorites', 'is_favorite': new_favorite}
                
        except Exception as e:
            logger.error(f"Error toggle favorite: {e}")
            return {'success': False, 'message': f'Error: {e}'}
    
    def log_query_execution(self, admin_id, query_id, query_name, sql_query, status='success', 
                           execution_time_ms=None, rows_affected=None, error_message=None):
        """Log eksekusi query untuk tracking"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Log ke history
                cursor.execute('''
                    INSERT INTO admin_query_history 
                    (admin_id, query_id, query_name, sql_query, execution_status, 
                     execution_time_ms, rows_affected, error_message)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (admin_id, query_id, query_name, sql_query, status, 
                      execution_time_ms, rows_affected, error_message))
                
                # Update execution count jika query berhasil
                if status == 'success' and query_id:
                    cursor.execute('''
                        UPDATE admin_custom_queries 
                        SET execution_count = execution_count + 1, 
                            last_executed = CURRENT_TIMESTAMP
                        WHERE id = ?
                    ''', (query_id,))
                
                return {'success': True, 'message': 'Execution logged'}
                
        except Exception as e:
            logger.error(f"Error logging query execution: {e}")
            return {'success': False, 'message': f'Error: {e}'}
    
    def get_workspace_settings(self, admin_id):
        """Ambil workspace settings untuk admin"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT setting_key, setting_value, setting_type 
                    FROM admin_workspace_settings 
                    WHERE admin_id = ?
                ''', (admin_id,))
                
                settings = {}
                for row in cursor.fetchall():
                    key, value, setting_type = row
                    
                    # Convert berdasarkan type
                    if setting_type == 'boolean':
                        settings[key] = value.lower() == 'true'
                    elif setting_type == 'integer':
                        settings[key] = int(value)
                    elif setting_type == 'float':
                        settings[key] = float(value)
                    else:
                        settings[key] = value
                
                return {'success': True, 'settings': settings}
                
        except Exception as e:
            logger.error(f"Error mengambil workspace settings: {e}")
            return {'success': False, 'message': f'Error: {e}', 'settings': {}}
    
    def save_workspace_setting(self, admin_id, setting_key, setting_value, setting_type='string'):
        """Simpan workspace setting"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO admin_workspace_settings 
                    (admin_id, setting_key, setting_value, setting_type, updated_at)
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                ''', (admin_id, setting_key, str(setting_value), setting_type))
                
                return {'success': True, 'message': 'Setting berhasil disimpan'}
                
        except Exception as e:
            logger.error(f"Error menyimpan workspace setting: {e}")
            return {'success': False, 'message': f'Error: {e}'}

# Global instance
admin_db = AdminDB()
