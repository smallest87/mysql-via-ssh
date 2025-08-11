"""
Encryption Utilities untuk SSH Config Management

Author: Julian Sukrisna
Organization: Javasatu.com
Created: August 2025

Utility untuk enkripsi dan dekripsi password SSH/MySQL
menggunakan Fernet (symmetric encryption) yang aman.
"""

from cryptography.fernet import Fernet
import base64
import os
import hashlib

class SSHConfigEncryption:
    def __init__(self, key=None):
        """
        Initialize encryption dengan key
        
        Args:
            key: Encryption key. Jika None, akan generate/load dari file
        """
        if key is None:
            self.key = self._get_or_create_key()
        else:
            self.key = key
        
        self.cipher = Fernet(self.key)
    
    def _get_or_create_key(self):
        """Get atau create encryption key"""
        key_file = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'ssh_encrypt.key')
        
        if os.path.exists(key_file):
            # Load existing key
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # Generate new key
            key = Fernet.generate_key()
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(key_file), exist_ok=True)
            
            # Save key
            with open(key_file, 'wb') as f:
                f.write(key)
            
            return key
    
    def encrypt_password(self, password: str) -> str:
        """
        Encrypt password
        
        Args:
            password: Plain text password
            
        Returns:
            str: Encrypted password (base64 encoded)
        """
        if not password:
            return ""
        
        encrypted = self.cipher.encrypt(password.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt_password(self, encrypted_password: str) -> str:
        """
        Decrypt password
        
        Args:
            encrypted_password: Encrypted password (base64 encoded)
            
        Returns:
            str: Plain text password
        """
        if not encrypted_password:
            return ""
        
        try:
            encrypted_bytes = base64.b64decode(encrypted_password.encode())
            decrypted = self.cipher.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception:
            # Return empty string if decryption fails
            return ""
    
    def encrypt_ssh_config(self, config: dict) -> dict:
        """
        Encrypt sensitive fields dalam SSH config
        
        Args:
            config: SSH config dictionary
            
        Returns:
            dict: Config dengan password ter-encrypt
        """
        encrypted_config = config.copy()
        
        # Encrypt SSH password
        if 'ssh_password' in config:
            encrypted_config['ssh_password'] = self.encrypt_password(config['ssh_password'])
        
        # Encrypt MySQL password
        if 'mysql_password' in config:
            encrypted_config['mysql_password'] = self.encrypt_password(config['mysql_password'])
        
        return encrypted_config
    
    def decrypt_ssh_config(self, config: dict) -> dict:
        """
        Decrypt sensitive fields dalam SSH config
        
        Args:
            config: SSH config dictionary dengan encrypted passwords
            
        Returns:
            dict: Config dengan password ter-decrypt
        """
        decrypted_config = config.copy()
        
        # Decrypt SSH password
        if 'ssh_password' in config:
            decrypted_config['ssh_password'] = self.decrypt_password(config['ssh_password'])
        
        # Decrypt MySQL password
        if 'mysql_password' in config:
            decrypted_config['mysql_password'] = self.decrypt_password(config['mysql_password'])
        
        return decrypted_config

# Global instance
ssh_encryption = SSHConfigEncryption()
