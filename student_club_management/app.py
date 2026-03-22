from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
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
    
    # Configuration
    if config_name == 'development':
        app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clubmanagement.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 587
        app.config['MAIL_USE_TLS'] = True
        app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
        app.config['MAIL_PASSWORD'] = 'your-app-password'
    else:  # production
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
        database_url = os.environ.get('DATABASE_URL') or 'sqlite:///clubmanagement_prod.db'
        # Use pg8000 driver for Python 3.14 compatibility
        if database_url and database_url.startswith('postgresql://'):
            database_url = database_url.replace('postgresql://', 'postgresql+pg8000://')
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 587
        app.config['MAIL_USE_TLS'] = True
        app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
        app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    
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
    
    # Create database tables and admin user with proper error handling
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Create admin user automatically if not exists
            from models.user import User
            admin = User.query.filter_by(email='admin@dut.ac.za').first()
            if not admin:
                print("Creating default admin user...")
                admin_user = User(
                    student_number='ADMIN001',
                    email='admin@dut.ac.za',
                    first_name='Administrator',
                    last_name='System',
                    role='admin',
                    is_active=True,
                    email_verified=True
                )
                admin_user.set_password('admin@123')
                db.session.add(admin_user)
                db.session.commit()
                print("✅ Admin user created: admin@dut.ac.za / admin@123")
            else:
                print("✅ Admin user already exists")
                
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
            print("⚠️  Continuing without database initialization...")
            # Don't crash the app if database fails
    
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
