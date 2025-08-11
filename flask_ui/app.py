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
import logging
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask import session
import json
from datetime import datetime
import traceback

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import core MySQL SSH Connection
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from database.mysql_ssh_connection import MySQLSSHConnection
from database.admin_db import admin_db
from database.ssh_encryption import SSHConfigEncryption

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
            """Homepage - redirect ke admin login untuk multi-tenant access"""
            if not session.get('admin_logged_in'):
                return redirect(url_for('admin_login'))
            else:
                return redirect(url_for('admin_dashboard'))
        
        @self.app.route('/connect', methods=['POST'])
        def connect():
            """Endpoint untuk membuat koneksi SSH + MySQL menggunakan config admin"""
            try:
                # Pastikan admin sudah login
                admin_user_id = session.get('admin_user_id')
                if not admin_user_id:
                    return jsonify({'error': 'Admin not logged in'}), 401
                
                # Ambil SSH config aktif dari database
                active_config = admin_db.get_active_ssh_config(admin_user_id)
                if not active_config:
                    return jsonify({'error': 'No active SSH configuration found. Please select one first.'}), 400
                
                # Decrypt passwords
                ssh_encryption = SSHConfigEncryption()
                
                ssh_config = {
                    'host': active_config['ssh_host'],
                    'port': active_config['ssh_port'],
                    'username': active_config['ssh_username'],
                    'password': ssh_encryption.decrypt_password(active_config['ssh_password']),
                }
                
                mysql_config = {
                    'host': active_config['mysql_host'],
                    'port': active_config['mysql_port'],
                    'username': active_config['mysql_username'],
                    'password': ssh_encryption.decrypt_password(active_config['mysql_password']),
                    'database': active_config['mysql_database'],
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
        
        @self.app.route('/api/connection/status')
        def connection_status():
            """API untuk check status koneksi real-time"""
            try:
                connection_id = session.get('current_connection')
                logger.info(f"Checking connection status for ID: {connection_id}")
                
                if not connection_id:
                    logger.info("No connection ID in session")
                    return jsonify({
                        'connected': False,
                        'message': 'No active connection session'
                    })
                
                if connection_id not in self.active_connections:
                    # Connection ID ada di session tapi tidak ada di active_connections
                    logger.warning(f"Connection ID {connection_id} not found in active connections")
                    session.pop('current_connection', None)
                    return jsonify({
                        'connected': False,
                        'message': 'Connection not found in active connections'
                    })
                
                # Check apakah koneksi masih aktif
                mysql_ssh = self.active_connections[connection_id]['connection']
                logger.info(f"Testing connection health for {connection_id}")
                is_connected = mysql_ssh.is_connected()
                logger.info(f"Connection health result: {is_connected}")
                
                if not is_connected:
                    # Koneksi terputus, bersihkan session dan active_connections
                    logger.warning(f"Connection {connection_id} is dead, cleaning up")
                    del self.active_connections[connection_id]
                    session.pop('current_connection', None)
                    
                    return jsonify({
                        'connected': False,
                        'message': 'Connection lost'
                    })
                
                # Koneksi masih aktif
                connection_info = self.active_connections[connection_id]
                logger.info(f"Connection {connection_id} is healthy")
                return jsonify({
                    'connected': True,
                    'message': 'Connection active',
                    'connection_info': {
                        'host': connection_info['mysql_config']['host'],
                        'database': connection_info['mysql_config']['database'],
                        'created_at': connection_info['created_at'].strftime('%Y-%m-%d %H:%M:%S')
                    }
                })
                
            except Exception as e:
                logger.error(f"Error in connection_status endpoint: {e}")
                return jsonify({
                    'connected': False,
                    'message': f'Error checking status: {str(e)}'
                }), 500
        
        # ========== ADMIN ROUTES ==========
        @self.app.route('/admin')
        def admin():
            """Redirect admin root to appropriate page"""
            if session.get('admin_logged_in'):
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('admin_login'))
        
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
        
        @self.app.route('/admin/logout')
        def admin_logout():
            """Admin logout"""
            session.pop('admin_logged_in', None)
            session.pop('admin_username', None)
            session.pop('admin_login_time', None)
            flash('Logout admin berhasil.', 'info')
            return redirect(url_for('index'))
        
        @self.app.route('/admin/dashboard')
        def admin_dashboard():
            """Admin dashboard - pilih SSH config atau buat baru"""
            if not session.get('admin_logged_in'):
                return redirect(url_for('admin_login'))
            
            admin_id = session.get('admin_user_id')
            ssh_configs = admin_db.get_admin_ssh_configs(admin_id)
            
            # Jika admin punya konfigurasi SSH aktif, redirect ke workspace
            active_config = admin_db.get_active_ssh_config(admin_id)
            if active_config:
                return redirect(url_for('admin_workspace'))
            
            return render_template('admin_dashboard.html', ssh_configs=ssh_configs)
        
        @self.app.route('/admin/select-config/<int:config_id>')
        def admin_select_config(config_id):
            """Pilih SSH config untuk digunakan"""
            if not session.get('admin_logged_in'):
                return redirect(url_for('admin_login'))
            
            admin_id = session.get('admin_user_id')
            result = admin_db.activate_ssh_config(admin_id, config_id)
            
            if result['success']:
                flash(f'SSH Configuration activated: {result.get("config_name", "")}', 'success')
                return redirect(url_for('admin_workspace'))
            else:
                flash(f'Error activating config: {result.get("message", "")}', 'error')
                return redirect(url_for('admin_dashboard'))
        
        # ============= WORKSPACE PERSONAL ROUTES =============
        
        @self.app.route('/admin/workspace')
        def admin_workspace():
            """Halaman workspace personal admin"""
            if not session.get('admin_logged_in'):
                flash('Please login to access admin workspace.', 'warning')
                return redirect(url_for('admin_login'))
            
            admin_user_id = session.get('admin_user_id')
            
            # Cek apakah admin sudah memilih SSH configuration
            active_config = admin_db.get_active_ssh_config(admin_user_id)
            if not active_config:
                flash('Please select SSH configuration first.', 'warning')
                return redirect(url_for('admin_dashboard'))
            
            # Ensure session data completeness for workspace
            admin_role = session.get('admin_role')
            has_role = admin_role is not None and admin_role != ''
            has_user_id = admin_user_id is not None and admin_user_id != ''
            
            # If session data incomplete, refetch from database
            if not has_role or not has_user_id:
                username = session.get('admin_username')
                if username:
                    # Get admin data from database
                    try:
                        cursor = admin_db.conn.cursor()
                        cursor.execute("""
                            SELECT id, username, email, full_name, role, is_active 
                            FROM admin_users WHERE username = ? AND is_active = 1
                        """, (username,))
                        admin_data = cursor.fetchone()
                        
                        if admin_data:
                            # Update session with complete data
                            session['admin_user_id'] = admin_data[0]
                            session['admin_username'] = admin_data[1]
                            session['admin_email'] = admin_data[2]
                            session['admin_full_name'] = admin_data[3]
                            session['admin_role'] = admin_data[4]
                            session.modified = True  # Force session save
                        else:
                            session.clear()
                            flash('Session expired. Please login again.', 'warning')
                            return redirect(url_for('admin_login'))
                    except Exception as e:
                        session.clear()
                        flash('Session error. Please login again.', 'error')
                        return redirect(url_for('admin_login'))
            
            return render_template(
                'admin_workspace.html',
                admin_user_id=session.get('admin_user_id'),
                admin_username=session.get('admin_username'),
                admin_role=session.get('admin_role'),
                admin_full_name=session.get('admin_full_name'),
                active_ssh_config=active_config
            )
        
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
            
            if not admin_id:
                return jsonify({'success': False, 'message': 'Admin ID not found in session. Please login again.'})
            
            # Handle both JSON and form data
            if request.is_json:
                data = request.get_json()
                query_name = data.get('name', '').strip()
                sql_query = data.get('sql_query', '').strip()
                description = data.get('description', '').strip()
                category = data.get('category', 'general')
                is_favorite = data.get('is_favorite', False)
            else:
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
        
        @self.app.route('/admin/api/workspace/queries/update', methods=['POST'])
        def api_workspace_update_query():
            """API untuk update custom query"""
            if not session.get('admin_logged_in'):
                return jsonify({'success': False, 'message': 'Authentication required'})
                
            admin_id = session.get('admin_user_id')
            data = request.get_json()
            
            query_id = data.get('query_id')
            query_name = data.get('name', '').strip()
            category = data.get('category', 'uncategorized')
            description = data.get('description', '').strip()
            sql_query = data.get('sql_query', '').strip()
            
            if not query_id:
                return jsonify({'success': False, 'message': 'Query ID is required'})
            
            if not query_name:
                return jsonify({'success': False, 'message': 'Query name is required'})
            
            if not sql_query:
                return jsonify({'success': False, 'message': 'SQL query is required'})
            
            result = admin_db.update_custom_query(admin_id, query_id, query_name, sql_query, category, description)
            return jsonify(result)
        
        @self.app.route('/admin/api/workspace/queries/delete', methods=['DELETE'])
        def api_workspace_delete_query():
            """API untuk delete custom query"""
            if not session.get('admin_logged_in'):
                return jsonify({'success': False, 'message': 'Authentication required'})
                
            admin_id = session.get('admin_user_id')
            data = request.get_json()
            
            query_id = data.get('query_id')
            
            if not query_id:
                return jsonify({'success': False, 'message': 'Query ID is required'})
            
            result = admin_db.delete_custom_query(admin_id, query_id)
            return jsonify(result)
        
        # ============= SSH CONFIGURATION MANAGEMENT =============
        
        @self.app.route('/admin/ssh-configs')
        def admin_ssh_configs():
            """Halaman management SSH configurations untuk admin"""
            if not session.get('admin_logged_in'):
                return redirect(url_for('admin_login'))
            
            admin_id = session.get('admin_user_id')
            ssh_configs = admin_db.get_admin_ssh_configs(admin_id)
            return render_template('admin_ssh_configs.html', ssh_configs=ssh_configs)
        
        @self.app.route('/admin/ssh-configs/new', methods=['GET', 'POST'])
        def admin_ssh_config_new():
            """Form untuk menambah SSH configuration baru"""
            if not session.get('admin_logged_in'):
                return redirect(url_for('admin_login'))
            
            admin_id = session.get('admin_user_id')
            
            if request.method == 'POST':
                data = request.json
                config_data = {
                    'name': data.get('name'),
                    'ssh_host': data.get('ssh_host'),
                    'ssh_port': data.get('ssh_port', 22),
                    'ssh_username': data.get('ssh_username'),
                    'ssh_password': data.get('ssh_password'),
                    'mysql_host': data.get('mysql_host', 'localhost'),
                    'mysql_port': data.get('mysql_port', 3306),
                    'mysql_username': data.get('mysql_username'),
                    'mysql_password': data.get('mysql_password'),
                    'mysql_database': data.get('mysql_database'),
                    'description': data.get('description', ''),
                    'is_active': data.get('is_active', True)
                }
                
                result = admin_db.save_ssh_config(admin_id, config_data)
                return jsonify(result)
            
            return render_template('admin_ssh_config_form.html', config=None, action='new')
        
        @self.app.route('/admin/ssh-configs/<int:config_id>/edit', methods=['GET', 'POST'])
        def admin_ssh_config_edit(config_id):
            """Form untuk edit SSH configuration"""
            admin_id = session.get('admin_id')
            if not admin_id:
                return redirect(url_for('admin_login'))
            
            if request.method == 'POST':
                data = request.json
                config_data = {
                    'name': data.get('name'),
                    'ssh_host': data.get('ssh_host'),
                    'ssh_port': data.get('ssh_port', 22),
                    'ssh_username': data.get('ssh_username'),
                    'ssh_password': data.get('ssh_password'),
                    'mysql_host': data.get('mysql_host', 'localhost'),
                    'mysql_port': data.get('mysql_port', 3306),
                    'mysql_username': data.get('mysql_username'),
                    'mysql_password': data.get('mysql_password'),
                    'mysql_database': data.get('mysql_database'),
                    'description': data.get('description', ''),
                    'is_active': data.get('is_active', True)
                }
                
                result = admin_db.update_ssh_config(admin_id, config_id, config_data)
                return jsonify(result)
            
            config = admin_db.get_ssh_config_by_id(admin_id, config_id)
            if not config:
                return redirect(url_for('admin_ssh_configs'))
            
            return render_template('admin_ssh_config_form.html', config=config, action='edit')
        
        @self.app.route('/admin/ssh-configs/<int:config_id>/delete', methods=['POST'])
        def admin_ssh_config_delete(config_id):
            """Delete SSH configuration"""
            admin_id = session.get('admin_id')
            if not admin_id:
                return jsonify({'success': False, 'message': 'Unauthorized'})
            
            result = admin_db.delete_ssh_config(admin_id, config_id)
            return jsonify(result)
        
        @self.app.route('/admin/ssh-configs/<int:config_id>/test', methods=['POST'])
        def admin_ssh_config_test(config_id):
            """Test SSH connection"""
            admin_id = session.get('admin_id')
            if not admin_id:
                return jsonify({'success': False, 'message': 'Unauthorized'})
            
            result = admin_db.test_ssh_connection(admin_id, config_id)
            return jsonify(result)
        
        @self.app.route('/admin/ssh-configs/<int:config_id>/activate', methods=['POST'])
        def admin_ssh_config_activate(config_id):
            """Activate SSH configuration"""
            admin_id = session.get('admin_id')
            if not admin_id:
                return jsonify({'success': False, 'message': 'Unauthorized'})
            
            result = admin_db.activate_ssh_config(admin_id, config_id)
            return jsonify(result)
        
        @self.app.route('/admin/ssh-configs/<int:config_id>/deactivate', methods=['POST'])
        def admin_ssh_config_deactivate(config_id):
            """Deactivate SSH configuration"""
            admin_id = session.get('admin_id')
            if not admin_id:
                return jsonify({'success': False, 'message': 'Unauthorized'})
            
            result = admin_db.deactivate_ssh_config(admin_id, config_id)
            return jsonify(result)
        
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
