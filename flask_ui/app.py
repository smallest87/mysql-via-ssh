"""
Flask Web UI untuk MySQL SSH Connection

Author: Julian Sukrisna
Organization: Javasatu.com
Created: August 2025
License: MIT

Web interface untuk mengelola koneksi MySQL melalui SSH tunnel
dengan antarmuka yang user-friendly dan secure.
"""

import os
import sys
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask import session
import json
from datetime import datetime
import traceback

# Import core MySQL SSH Connection
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from database.mysql_ssh_connection import MySQLSSHConnection
from database.admin_db import admin_db

class MySQLSSHFlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'mysql-ssh-ui-key-change-in-production')
        
        # Setup routes
        self.setup_routes()
        
        # Active connections storage
        self.active_connections = {}
    
    def setup_routes(self):
        """Setup all Flask routes"""
        
        @self.app.route('/')
        def index():
            """Homepage dengan form koneksi"""
            return render_template('index.html')
        
        @self.app.route('/connect', methods=['POST'])
        def connect():
            """Endpoint untuk membuat koneksi SSH + MySQL"""
            try:
                # Ambil data dari form
                ssh_config = {
                    'host': request.form.get('ssh_host'),
                    'port': int(request.form.get('ssh_port', 22)),
                    'username': request.form.get('ssh_username'),
                    'password': request.form.get('ssh_password'),
                }
                
                mysql_config = {
                    'host': request.form.get('mysql_host', 'localhost'),
                    'port': int(request.form.get('mysql_port', 3306)),
                    'username': request.form.get('mysql_username'),
                    'password': request.form.get('mysql_password'),
                    'database': request.form.get('mysql_database'),
                }
                
                # Buat koneksi
                connection_id = f"conn_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                mysql_ssh = MySQLSSHConnection(ssh_config, mysql_config)
                
                if mysql_ssh.connect():
                    # Simpan koneksi aktif
                    self.active_connections[connection_id] = {
                        'connection': mysql_ssh,
                        'ssh_config': ssh_config,
                        'mysql_config': mysql_config,
                        'created_at': datetime.now(),
                        'status': 'connected'
                    }
                    
                    session['current_connection'] = connection_id
                    flash('Koneksi berhasil dibuat!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Gagal membuat koneksi. Periksa konfigurasi Anda.', 'error')
                    return redirect(url_for('index'))
                    
            except Exception as e:
                flash(f'Error: {str(e)}', 'error')
                return redirect(url_for('index'))
        
        @self.app.route('/dashboard')
        def dashboard():
            """Dashboard utama dengan informasi koneksi"""
            connection_id = session.get('current_connection')
            if not connection_id or connection_id not in self.active_connections:
                flash('Tidak ada koneksi aktif. Silakan buat koneksi baru.', 'warning')
                return redirect(url_for('index'))
            
            connection_info = self.active_connections[connection_id]
            return render_template('dashboard.html', 
                                 connection_id=connection_id,
                                 connection_info=connection_info)
        
        @self.app.route('/query', methods=['GET', 'POST'])
        def query():
            """Halaman untuk menjalankan query SQL"""
            connection_id = session.get('current_connection')
            if not connection_id or connection_id not in self.active_connections:
                return redirect(url_for('index'))
            
            if request.method == 'POST':
                return self.execute_query()
            
            return render_template('query.html')
        
        @self.app.route('/api/execute_query', methods=['POST'])
        def execute_query():
            """API endpoint untuk menjalankan query"""
            try:
                connection_id = session.get('current_connection')
                if not connection_id or connection_id not in self.active_connections:
                    return jsonify({'error': 'Tidak ada koneksi aktif'}), 400
                
                query_text = request.json.get('query', '').strip()
                if not query_text:
                    return jsonify({'error': 'Query tidak boleh kosong'}), 400
                
                mysql_ssh = self.active_connections[connection_id]['connection']
                result = mysql_ssh.execute_query(query_text)
                
                if result is None:
                    return jsonify({
                        'error': 'Query gagal dijalankan. Periksa syntax SQL atau koneksi database.'
                    }), 500
                
                if result is not None:
                    # Convert datetime objects untuk JSON serialization
                    if isinstance(result, list):
                        for row in result:
                            if isinstance(row, dict):
                                for key, value in row.items():
                                    if isinstance(value, datetime):
                                        row[key] = value.isoformat()
                    
                    return jsonify({
                        'success': True,
                        'data': result,
                        'row_count': len(result) if isinstance(result, list) else result,
                        'message': f'Query berhasil dijalankan. {len(result) if isinstance(result, list) else result} baris dikembalikan.'
                    })
                else:
                    return jsonify({
                        'success': True,
                        'data': [],
                        'row_count': 0,
                        'message': 'Query berhasil dijalankan tanpa hasil.'
                    })
                    
            except Exception as e:
                return jsonify({
                    'error': f'Error: {str(e)}',
                    'traceback': traceback.format_exc()
                }), 500
        
        @self.app.route('/api/get_databases')
        def get_databases():
            """API untuk mendapatkan daftar database"""
            try:
                connection_id = session.get('current_connection')
                if not connection_id or connection_id not in self.active_connections:
                    return jsonify({'error': 'Tidak ada koneksi aktif'}), 400
                
                mysql_ssh = self.active_connections[connection_id]['connection']
                result = mysql_ssh.execute_query("SHOW DATABASES")
                
                if result is None:
                    return jsonify({'error': 'Gagal mengambil daftar database. Periksa koneksi Anda.'}), 500
                
                databases = [row['Database'] for row in result] if result else []
                return jsonify({'databases': databases})
                
            except Exception as e:
                return jsonify({'error': f'Error: {str(e)}'}), 500
        
        @self.app.route('/api/get_tables')
        def get_tables():
            """API untuk mendapatkan daftar tabel"""
            try:
                connection_id = session.get('current_connection')
                if not connection_id or connection_id not in self.active_connections:
                    return jsonify({'error': 'Tidak ada koneksi aktif'}), 400
                
                mysql_ssh = self.active_connections[connection_id]['connection']
                result = mysql_ssh.execute_query("SHOW TABLES")
                
                if result is None:
                    return jsonify({'error': 'Gagal mengambil daftar tabel. Periksa koneksi database Anda.'}), 500
                
                tables = [list(row.values())[0] for row in result] if result else []
                return jsonify({'tables': tables})
                
            except Exception as e:
                return jsonify({'error': f'Error: {str(e)}'}), 500
        
        @self.app.route('/api/status')
        def status():
            """API untuk mendapatkan status koneksi"""
            try:
                connection_id = session.get('current_connection')
                if not connection_id or connection_id not in self.active_connections:
                    return jsonify({
                        'connected': False,
                        'message': 'Tidak ada koneksi aktif'
                    })
                
                connection_info = self.active_connections[connection_id]
                return jsonify({
                    'connected': True,
                    'connection_id': connection_id,
                    'ssh_host': connection_info.get('ssh_host', 'Unknown'),
                    'mysql_host': connection_info.get('mysql_host', 'Unknown'),
                    'mysql_database': connection_info.get('mysql_database', 'Unknown'),
                    'connected_at': connection_info.get('connected_at', 'Unknown')
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/disconnect')
        def disconnect():
            """Disconnect dari SSH dan MySQL"""
            connection_id = session.get('current_connection')
            if connection_id and connection_id in self.active_connections:
                mysql_ssh = self.active_connections[connection_id]['connection']
                mysql_ssh.close()
                del self.active_connections[connection_id]
                session.pop('current_connection', None)
                flash('Koneksi berhasil ditutup.', 'info')
            
            return redirect(url_for('index'))
        
        # ========== ADMIN ROUTES ==========
        @self.app.route('/admin/login', methods=['GET', 'POST'])
        def admin_login():
            """Admin login page with database authentication"""
            if request.method == 'POST':
                username = request.form.get('username')
                password = request.form.get('password')
                
                # Authenticate using database
                admin_user = admin_db.authenticate_admin(username, password)
                if admin_user:
                    session['admin_logged_in'] = True
                    session['admin_username'] = admin_user['username']
                    session['admin_user_id'] = admin_user['id']
                    session['admin_full_name'] = admin_user['full_name']
                    session['admin_role'] = admin_user['role']
                    session['admin_login_time'] = datetime.now().isoformat()
                    flash(f'Welcome back, {admin_user["full_name"]}!', 'success')
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('Invalid username or password!', 'error')
                    return render_template('admin_login.html', error='Invalid credentials')
            
            # Check if already logged in
            if session.get('admin_logged_in'):
                return redirect(url_for('admin_dashboard'))
                
            return render_template('admin_login.html')
        
        @self.app.route('/admin/register', methods=['GET', 'POST'])
        def admin_register():
            """Admin registration page"""
            if request.method == 'POST':
                username = request.form.get('username')
                email = request.form.get('email')
                password = request.form.get('password')
                confirm_password = request.form.get('confirm_password')
                full_name = request.form.get('full_name')
                role = request.form.get('role', 'admin')
                
                # Validation
                if not all([username, email, password, confirm_password, full_name]):
                    flash('All fields are required!', 'error')
                    return render_template('admin_register.html', error='All fields are required')
                
                if password != confirm_password:
                    flash('Password and confirmation do not match!', 'error')
                    return render_template('admin_register.html', error='Passwords do not match')
                
                if len(password) < 6:
                    flash('Password must be at least 6 characters long!', 'error')
                    return render_template('admin_register.html', error='Password too short')
                
                # Create admin in database
                if admin_db.create_admin(username, email, password, full_name, role):
                    flash(f'Admin account "{username}" created successfully!', 'success')
                    return redirect(url_for('admin_login'))
                else:
                    flash('Failed to create admin account. Username or email may already exist.', 'error')
                    return render_template('admin_register.html', error='Username or email already exists')
            
            return render_template('admin_register.html')
        
        @self.app.route('/admin/management')
        def admin_management():
            """Admin management page - requires admin login"""
            if not session.get('admin_logged_in'):
                flash('Please login as admin first.', 'warning')
                return redirect(url_for('admin_login'))
            
            # Get all admins and statistics
            admins = admin_db.get_all_admins()
            stats = admin_db.get_admin_stats()
            
            return render_template('admin_management.html', admins=admins, stats=stats)
        
        @self.app.route('/admin/toggle_status', methods=['POST'])
        def admin_toggle_status():
            """Toggle admin account status"""
            if not session.get('admin_logged_in'):
                return jsonify({'success': False, 'error': 'Unauthorized'}), 401
            
            data = request.get_json()
            admin_id = data.get('admin_id')
            is_active = data.get('is_active')
            
            if admin_db.update_admin_status(admin_id, is_active):
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'error': 'Failed to update admin status'})
        
        @self.app.route('/admin/delete_admin', methods=['POST'])
        def admin_delete_admin():
            """Delete admin account"""
            if not session.get('admin_logged_in'):
                return jsonify({'success': False, 'error': 'Unauthorized'}), 401
            
            data = request.get_json()
            admin_id = data.get('admin_id')
            
            if admin_db.delete_admin(admin_id):
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'error': 'Failed to delete admin account'})
        
        @self.app.route('/admin/dashboard')
        def admin_dashboard():
            """Admin dashboard - requires login"""
            if not session.get('admin_logged_in'):
                flash('Please login as admin first.', 'warning')
                return redirect(url_for('admin_login'))
            
            # Get real statistics
            admin_stats = admin_db.get_admin_stats()
            stats = {
                'active_connections': len(self.active_connections),
                'total_queries': 247,  # Could be made dynamic
                'uptime': '2d 14h',    # Could be made dynamic
                'admin_sessions': admin_stats['total_active']
            }
            
            # Generate dummy recent activities (could be made dynamic)
            recent_activities = [
                {
                    'time': '10:30:15',
                    'action': 'Database Query',
                    'user': 'Guest User',
                    'status': 'Success',
                    'status_class': 'success'
                },
                {
                    'time': '10:25:42',
                    'action': 'SSH Connection',
                    'user': 'Guest User',
                    'status': 'Connected',
                    'status_class': 'info'
                },
                {
                    'time': '10:22:18',
                    'action': 'Admin Login',
                    'user': session.get('admin_full_name', 'admin'),
                    'status': 'Success',
                    'status_class': 'success'
                },
                {
                    'time': '10:15:33',
                    'action': 'Database Query',
                    'user': 'Guest User',
                    'status': 'Error',
                    'status_class': 'danger'
                },
                {
                    'time': '10:12:07',
                    'action': 'Export Data',
                    'user': 'Guest User',
                    'status': 'Completed',
                    'status_class': 'success'
                }
            ]
            
            return render_template('admin_dashboard.html', 
                                 stats=stats, 
                                 recent_activities=recent_activities)
        
        @self.app.route('/admin/logout')
        def admin_logout():
            """Admin logout"""
            session.pop('admin_logged_in', None)
            session.pop('admin_username', None)
            session.pop('admin_login_time', None)
            flash('Logout admin berhasil.', 'info')
            return redirect(url_for('index'))
        
        # ============= WORKSPACE PERSONAL ROUTES =============
        
        @self.app.route('/admin/workspace')
        def admin_workspace():
            """Halaman workspace personal admin"""
            if not session.get('admin_logged_in'):
                flash('Please login to access admin workspace.', 'warning')
                return redirect(url_for('admin_login'))
            return render_template('admin_workspace.html')
        
        @self.app.route('/admin/api/workspace/queries')
        def api_workspace_queries():
            """API untuk mengambil custom queries admin"""
            if not session.get('admin_logged_in'):
                return jsonify({'success': False, 'message': 'Authentication required'})
                
            admin_id = session.get('admin_user_id')
            category = request.args.get('category')
            favorites_only = request.args.get('favorites_only') == 'true'
            
            result = admin_db.get_admin_custom_queries(admin_id, category, favorites_only)
            return jsonify(result)
        
        @self.app.route('/admin/api/workspace/queries/save', methods=['POST'])
        def api_workspace_save_query():
            """API untuk menyimpan custom query"""
            if not session.get('admin_logged_in'):
                return jsonify({'success': False, 'message': 'Authentication required'})
                
            admin_id = session.get('admin_user_id')
            
            query_name = request.form.get('query_name', '').strip()
            sql_query = request.form.get('sql_query', '').strip()
            description = request.form.get('query_description', '').strip()
            category = request.form.get('query_category', 'general')
            is_favorite = request.form.get('is_favorite') == 'on'
            
            if not query_name or not sql_query:
                return jsonify({'success': False, 'message': 'Query name and SQL are required'})
            
            result = admin_db.save_custom_query(
                admin_id, query_name, sql_query, description, category, is_favorite
            )
            return jsonify(result)
        
        @self.app.route('/admin/api/workspace/queries/favorite', methods=['POST'])
        def api_workspace_toggle_favorite():
            """API untuk toggle favorite query"""
            if not session.get('admin_logged_in'):
                return jsonify({'success': False, 'message': 'Authentication required'})
                
            admin_id = session.get('admin_user_id')
            data = request.get_json()
            query_id = data.get('query_id')
            
            if not query_id:
                return jsonify({'success': False, 'message': 'Query ID required'})
            
            result = admin_db.toggle_query_favorite(admin_id, query_id)
            return jsonify(result)
        
        @self.app.route('/admin/api/workspace/queries/execute', methods=['POST'])
        def api_workspace_execute_query():
            """API untuk eksekusi custom query"""
            if not session.get('admin_logged_in'):
                return jsonify({'success': False, 'message': 'Authentication required'})
                
            admin_id = session.get('admin_user_id')
            data = request.get_json()
            query_id = data.get('query_id')
            sql_query = data.get('sql_query', '').strip()
            
            if not sql_query:
                return jsonify({'success': False, 'message': 'SQL query required'})
            
            try:
                # Import MySQL connection
                import time
                from src.database.mysql_ssh_connection import MySQLSSHConnection
                
                start_time = time.time()
                db_connection = MySQLSSHConnection()
                
                # Execute query
                if sql_query.strip().upper().startswith('SELECT'):
                    # Read query
                    results = db_connection.execute_query(sql_query)
                    rows_affected = len(results) if results else 0
                    execution_status = 'success'
                    error_message = None
                else:
                    # Write query (INSERT, UPDATE, DELETE, etc.)
                    rows_affected = db_connection.execute_update(sql_query)
                    results = f"{rows_affected} rows affected"
                    execution_status = 'success'
                    error_message = None
                
                execution_time_ms = int((time.time() - start_time) * 1000)
                
                # Log execution
                if query_id:
                    # Get query name for logging
                    queries_result = admin_db.get_admin_custom_queries(admin_id)
                    query_name = None
                    if queries_result['success']:
                        for q in queries_result['queries']:
                            if q['id'] == int(query_id):
                                query_name = q['name']
                                break
                    
                    admin_db.log_query_execution(
                        admin_id, query_id, query_name, sql_query, 
                        execution_status, execution_time_ms, rows_affected, error_message
                    )
                
                return jsonify({
                    'success': True,
                    'results': results,
                    'rows_affected': rows_affected,
                    'execution_time_ms': execution_time_ms,
                    'message': f'Query executed successfully in {execution_time_ms}ms'
                })
                
            except Exception as e:
                execution_time_ms = int((time.time() - start_time) * 1000) if 'start_time' in locals() else 0
                error_message = str(e)
                
                # Log failed execution
                if query_id:
                    admin_db.log_query_execution(
                        admin_id, query_id, None, sql_query,
                        'error', execution_time_ms, 0, error_message
                    )
                
                return jsonify({
                    'success': False,
                    'message': f'Query execution failed: {error_message}',
                    'execution_time_ms': execution_time_ms
                })
        
        # ============= ERROR HANDLERS =============
        
        @self.app.errorhandler(404)
        def not_found(error):
            return render_template('error.html', 
                                 error_code=404, 
                                 error_message="Halaman tidak ditemukan"), 404
        
        @self.app.errorhandler(500)
        def internal_error(error):
            return render_template('error.html', 
                                 error_code=500, 
                                 error_message="Terjadi kesalahan internal"), 500
    
    def run(self, host='127.0.0.1', port=5000, debug=True):
        """Menjalankan Flask app"""
        print(f"🚀 MySQL SSH Web UI starting...")
        print(f"📡 Server: http://{host}:{port}")
        print(f"🔒 Security: Pastikan credential tidak di-commit ke repository!")
        print(f"👨‍💻 Author: Julian Sukrisna (Javasatu.com)")
        
        self.app.run(host=host, port=port, debug=debug)

def create_app():
    """Factory function untuk membuat Flask app"""
    mysql_flask_app = MySQLSSHFlaskApp()
    return mysql_flask_app.app

if __name__ == '__main__':
    app_instance = MySQLSSHFlaskApp()
    app_instance.run()
