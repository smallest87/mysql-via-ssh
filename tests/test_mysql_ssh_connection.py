"""
Unit tests untuk MySQL SSH Connection
"""

import unittest
import sys
import os

# Tambahkan path src ke Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from database.mysql_ssh_connection import MySQLSSHConnection

class TestMySQLSSHConnection(unittest.TestCase):
    """Test cases untuk MySQLSSHConnection"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.ssh_config = {
            'host': 'test-server.com',
            'port': 22,
            'username': 'test_user',
            'password': 'test_password',
        }
        
        self.mysql_config = {
            'host': 'localhost',
            'port': 3306,
            'username': 'test_mysql_user',
            'password': 'test_mysql_password',
            'database': 'test_database',
        }
    
    def test_initialization(self):
        """Test inisialisasi class"""
        mysql_ssh = MySQLSSHConnection(self.ssh_config, self.mysql_config)
        
        self.assertEqual(mysql_ssh.ssh_config, self.ssh_config)
        self.assertEqual(mysql_ssh.mysql_config, self.mysql_config)
        self.assertIsNone(mysql_ssh.tunnel)
        self.assertIsNone(mysql_ssh.connection)
    
    def test_config_validation(self):
        """Test validasi konfigurasi"""
        # Test dengan konfigurasi None
        with self.assertRaises(TypeError):
            MySQLSSHConnection(None, None)
            
        # Test dengan konfigurasi bukan dict
        with self.assertRaises(TypeError):
            MySQLSSHConnection("invalid", "invalid")
            
        # Test dengan SSH config kosong
        with self.assertRaises(ValueError):
            MySQLSSHConnection({}, self.mysql_config)
            
        # Test dengan MySQL config kosong
        with self.assertRaises(ValueError):
            MySQLSSHConnection(self.ssh_config, {})
            
        # Test dengan field yang hilang
        incomplete_ssh = self.ssh_config.copy()
        del incomplete_ssh['host']
        with self.assertRaises(ValueError):
            MySQLSSHConnection(incomplete_ssh, self.mysql_config)
    
    # Note: Test koneksi aktual memerlukan server yang nyata
    # Untuk testing yang lebih komprehensif, gunakan mock objects

if __name__ == '__main__':
    unittest.main()
