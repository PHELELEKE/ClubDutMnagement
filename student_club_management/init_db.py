#!/usr/bin/env python
"""
init_db.py - Database initialization script
Run this once after installing requirements to create all database tables.

Usage:
    python init_db.py
"""

from app import create_app, db
from database import init_db

if __name__ == '__main__':
    try:
        app = create_app()
        with app.app_context():
            init_db(app)
            print("✓ Database initialized successfully!")
            print("✓ All tables created.")
            print("\nYou can now run: python run.py")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        print("\nMake sure your .env file has the correct DATABASE_URL")
