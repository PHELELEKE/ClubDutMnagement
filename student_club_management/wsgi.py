#!/usr/bin/env python3
"""
Basic WSGI entry point with authentication and basic features
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, jsonify, render_template_string, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)

# Basic configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Initialize bcrypt
bcrypt = Bcrypt(app)

# Database configuration - don't initialize at import time
database_url = os.environ.get('DATABASE_URL')

# Simple in-memory user store for now (will upgrade to database later)
users = {}

# Test database connection at runtime
def test_database_connection():
    if not database_url:
        return False, "DATABASE_URL not set"
    
    try:
        import pg8000
        import urllib.parse
        
        parsed = urllib.parse.urlparse(database_url)
        
        conn = pg8000.connect(
            user=parsed.username,
            password=parsed.password,
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path.lstrip('/')
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        
        return True, "Connected to PostgreSQL database"
    except Exception as e:
        return False, f"Database error: {str(e)}"

# HTML Templates
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Club Management - Login</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        input { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .alert { padding: 10px; margin-bottom: 15px; border-radius: 4px; }
        .alert-success { background: #d4edda; color: #155724; }
        .alert-danger { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <h2>🎉 Club Management System</h2>
    <h3>Login</h3>
    
    {% with messages = get_flashed_messages() %}
        {% for message in messages %}
            <div class="alert alert-{{ 'success' if 'success' in message else 'danger' }}">{{ message }}</div>
        {% endfor %}
    {% endwith %}
    
    <form method="POST">
        <div class="form-group">
            <label>Username:</label>
            <input type="text" name="username" required>
        </div>
        <div class="form-group">
            <label>Password:</label>
            <input type="password" name="password" required>
        </div>
        <button type="submit">Login</button>
    </form>
    
    <p><a href="/register">Don't have an account? Register</a></p>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Club Management Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #007bff; color: white; padding: 20px; border-radius: 4px; margin-bottom: 20px; }
        .card { border: 1px solid #ddd; padding: 20px; margin-bottom: 20px; border-radius: 4px; }
        .btn { background: #007bff; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px; }
        .btn:hover { background: #0056b3; }
        .stats { display: flex; gap: 20px; margin-bottom: 20px; }
        .stat { background: #f8f9fa; padding: 15px; border-radius: 4px; text-align: center; }
    </style>
</head>
<body>
    <div class="header">
        <h2>🎉 Club Management Dashboard</h2>
        <p>Welcome, {{ username }}! | <a href="/logout" style="color: white;">Logout</a></p>
    </div>
    
    <div class="stats">
        <div class="stat">
            <h3>{{ clubs_count }}</h3>
            <p>Clubs</p>
        </div>
        <div class="stat">
            <h3>{{ events_count }}</h3>
            <p>Events</p>
        </div>
        <div class="stat">
            <h3>{{ members_count }}</h3>
            <p>Members</p>
        </div>
    </div>
    
    <div class="card">
        <h3>🏛️ Clubs</h3>
        <p>Manage your student organizations and activities.</p>
        <a href="/clubs" class="btn">Manage Clubs</a>
    </div>
    
    <div class="card">
        <h3>📅 Events</h3>
        <p>Schedule and track club events and activities.</p>
        <a href="/events" class="btn">Manage Events</a>
    </div>
    
    <div class="card">
        <h3>👥 Members</h3>
        <p>Manage club members and participation.</p>
        <a href="/members" class="btn">Manage Members</a>
    </div>
    
    <div class="card">
        <h3>📊 Analytics</h3>
        <p>View club analytics and reports.</p>
        <a href="/analytics" class="btn">View Analytics</a>
    </div>
</body>
</html>
"""

# Routes
@app.route('/')
def index():
    db_connected, db_status = test_database_connection()
    
    if 'user_id' in session:
        return redirect('/dashboard')
    
    return f"""
    <h1>🎉 Club Management System</h1>
    <h2>📊 Database Status: {db_status}</h2>
    <h3>🔧 Environment Variables:</h3>
    <ul>
        <li>DATABASE_URL: {'✅ Set' if database_url else '❌ Missing'}</li>
        <li>SECRET_KEY: {'✅ Set' if os.environ.get('SECRET_KEY') else '❌ Missing'}</li>
        <li>FLASK_ENV: {os.environ.get('FLASK_ENV', 'Not set')}</li>
    </ul>
    <h3>🚀 Features:</h3>
    <p><a href="/login">🔐 Login</a> | <a href="/register">📝 Register</a> | <a href="/dashboard">📊 Dashboard</a></p>
    <p>{'Database connected! Ready for club management features.' if db_connected else 'Add DATABASE_URL environment variable in Render dashboard to connect to PostgreSQL!'}</p>
    """

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple authentication (will upgrade to database later)
        if username in users and bcrypt.check_password_hash(users[username], password):
            session['user_id'] = username
            flash('Login successful!', 'success')
            return redirect('/dashboard')
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            # Hash password
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            users[username] = hashed_password
            
            flash('Registration successful! Please login.', 'success')
            return redirect('/login')
    
    return render_template_string(LOGIN_TEMPLATE.replace('Login', 'Register').replace("Don't have an account? Register", 'Already have an account? Login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    
    # Mock data (will get from database later)
    return render_template_string(DASHBOARD_TEMPLATE, 
                           username=session['user_id'],
                           clubs_count=3,
                           events_count=12,
                           members_count=45)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect('/')

@app.route('/health')
def health():
    db_connected, db_status = test_database_connection()
    
    if db_connected:
        return jsonify({
            'status': 'healthy', 
            'message': 'Club Management System is running',
            'database': 'connected',
            'features': ['authentication', 'dashboard', 'basic_club_management']
        })
    else:
        return jsonify({
            'status': 'unhealthy', 
            'message': db_status,
            'database': 'not connected'
        }), 500

@app.route('/api/test')
def api_test():
    """Test API endpoint"""
    return jsonify({
        'message': 'API is working',
        'database_url': 'Set' if database_url else 'Not set',
        'flask_env': os.environ.get('FLASK_ENV', 'Not set'),
        'features': ['authentication', 'dashboard', 'club_management']
    })

if __name__ == "__main__":
    app.run()

# For Gunicorn
application = app
