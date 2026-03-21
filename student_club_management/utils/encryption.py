"""
Encryption utilities for securing sensitive data at rest.
Uses AES-256 encryption for sensitive fields.
"""
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

# Generate a secure key from a passphrase (in production, store this securely)
def _get_encryption_key():
    """Generate encryption key based on machine-specific values"""
    # Use a combination of machine-specific values
    machine_id = os.environ.get('COMPUTERNAME', 'default') + os.environ.get('USERNAME', 'user')
    passphrase = f"ClubManagementSecureKey_{machine_id}_2024"
    
    # Generate key using PBKDF2HMAC
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'club_management_salt',
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
    return key

# Initialize the Fernet cipher with the key
_cipher = Fernet(_get_encryption_key())

def encrypt(plain_text):
    """Encrypt a string using AES-256."""
    if not plain_text:
        return None
    
    # If already encrypted, return as is
    if isinstance(plain_text, str) and plain_text.startswith('enc_'):
        return plain_text
    
    try:
        encrypted = _cipher.encrypt(plain_text.encode())
        return 'enc_' + base64.urlsafe_b64encode(encrypted).decode()
    except Exception as e:
        print(f"Encryption error: {e}")
        return plain_text

def decrypt(encrypted_text):
    """Decrypt an encrypted string."""
    if not encrypted_text:
        return None
    
    # Check if actually encrypted
    if not isinstance(encrypted_text, str) or not encrypted_text.startswith('enc_'):
        return encrypted_text
    
    try:
        encrypted_data = encrypted_text[4:]
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data)
        decrypted = _cipher.decrypt(encrypted_bytes)
        return decrypted.decode()
    except Exception as e:
        print(f"Decryption error: {e}")
        return encrypted_text

def encrypt_dict(data, fields_to_encrypt):
    """Encrypt specific fields in a dictionary."""
    if not data:
        return data
    
    result = data.copy()
    for field in fields_to_encrypt:
        if field in result and result[field]:
            result[field] = encrypt(str(result[field]))
    return result

def decrypt_dict(data, fields_to_decrypt):
    """Decrypt specific fields in a dictionary."""
    if not data:
        return data
    
    result = data.copy()
    for field in fields_to_decrypt:
        if field in result and result[field]:
            result[field] = decrypt(str(result[field]))
    return result

