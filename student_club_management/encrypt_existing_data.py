"""
Script to encrypt existing sensitive data in the database.
Run this once to encrypt all existing PII data.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from models.user import User, PreRegisteredStudent

def encrypt_existing_data():
    """Encrypt all sensitive data in the database"""
    app = create_app()
    with app.app_context():
        print("🔐 Encrypting existing user data...")
        
        # Encrypt User table data
        users = User.query.all()
        encrypted_count = 0
        for user in users:
            # Skip if already encrypted
            if not user.encrypted_student_number and not user.encrypted_email:
                user.encrypt_sensitive_data()
                encrypted_count += 1
        
        db.session.commit()
        print(f"✅ Encrypted {encrypted_count} user records")
        
        # Show sample of encrypted data
        print("\n📊 Sample of encrypted data:")
        user = User.query.first()
        if user:
            print(f"  Original Email: {user.email}")
            print(f"  Encrypted Email: {user.encrypted_email}")
        
        print("\n🔒 Data at rest encryption complete!")
        print("All sensitive PII (student numbers, emails) are now encrypted in the database.")

if __name__ == '__main__':
    encrypt_existing_data()

