from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from student_club_management.config import config
import os

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_name='development'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Login manager configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        return User.query.get(int(user_id))
    
    # Register blueprints - defer imports to avoid circular imports
    def register_blueprints():
        from routes.auth import auth_bp
        from routes.admin import admin_bp
        from routes.dashboard import dashboard_bp
        from routes.clubs import clubs_bp
        from routes.events import events_bp
        from routes.announcements import announcements_bp
        from routes.notifications import notifications_bp
        from routes.chat import chat_bp
        from routes.analytics import analytics_bp
        
        app.register_blueprint(auth_bp)
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
        app.register_blueprint(clubs_bp, url_prefix='/clubs')
        app.register_blueprint(events_bp, url_prefix='/events')
        app.register_blueprint(announcements_bp, url_prefix='/announcements')
        app.register_blueprint(notifications_bp, url_prefix='/notifications')
        app.register_blueprint(chat_bp, url_prefix='/chat')
        app.register_blueprint(analytics_bp)
    
    # Register blueprints after app context is set up
    register_blueprints()
    
    # Main route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Health check endpoint for monitoring
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Club Management System is running'}, 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    return app
