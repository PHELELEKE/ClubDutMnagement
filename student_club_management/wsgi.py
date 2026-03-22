#!/usr/bin/env python3
"""
Database-connected WSGI entry point for Render deployment
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Test database connection
@app.route('/')
def index():
    try:
        # Test database connection
        db.engine.execute('SELECT 1')
        db_status = "Connected to PostgreSQL database"
        db_connected = True
    except Exception as e:
        db_status = f"Database error: {str(e)}"
        db_connected = False
    
    return f"""
    <h1>🎉 Club Management System</h1>
    <h2>📊 Database Status: {db_status}</h2>
    <h3>🔧 Environment Variables:</h3>
    <ul>
        <li>DATABASE_URL: {'✅ Set' if os.environ.get('DATABASE_URL') else '❌ Missing'}</li>
        <li>SECRET_KEY: {'✅ Set' if os.environ.get('SECRET_KEY') else '❌ Missing'}</li>
        <li>FLASK_ENV: {os.environ.get('FLASK_ENV', 'Not set')}</li>
    </ul>
    <h3>🚀 Next Steps:</h3>
    <p>If database is connected, we can add full club management features!</p>
    """

@app.route('/health')
def health():
    try:
        # Test database connection
        db.engine.execute('SELECT 1')
        return jsonify({
            'status': 'healthy', 
            'message': 'Club Management System is running',
            'database': 'connected'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy', 
            'message': 'Database connection failed',
            'error': str(e)
        }), 500

@app.route('/api/test')
def api_test():
    """Test API endpoint"""
    return jsonify({
        'message': 'API is working',
        'database_url': os.environ.get('DATABASE_URL', 'Not set'),
        'flask_env': os.environ.get('FLASK_ENV', 'Not set')
    })

if __name__ == "__main__":
    app.run()

# For Gunicorn
application = app
