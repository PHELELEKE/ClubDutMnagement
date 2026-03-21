"""
Fixed app.py - no global FlaskWTF init
"""
from flask import Flask, render_template
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_caching import Cache
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
cache = Cache()
scheduler = BackgroundScheduler()

login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    return User.query.get(int(user_id))

def send_hourly_reminders():
    """Background task to send reminder notifications"""
    with scheduler.app.app_context():
        from routes.notifications import (
            send_reminder_notifications,
            send_meeting_reminders,
            send_1hour_event_reminders,
            send_1hour_meeting_reminders
        )
        try:
            send_reminder_notifications()
            send_meeting_reminders()
            send_1hour_event_reminders()
            send_1hour_meeting_reminders()
        except Exception as e:
            print(f"Error sending reminders: {e}")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    db.app = app
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    cache.init_app(app)

    from flask_wtf.csrf import CSRFProtect
    csrf = CSRFProtect(app)

    from routes.auth import auth_bp
    from routes.clubs import clubs_bp
    from routes.events import events_bp
    from routes.dashboard import dashboard_bp
    from routes.admin import admin_bp
    from routes.notifications import notifications_bp
    from routes.chat import chat_bp
    from routes.announcements import announcements_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(clubs_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(announcements_bp)

    scheduler.app = app
    scheduler.add_job(func=send_hourly_reminders, trigger="interval", hours=1, id='send_reminders')
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

    from flask_wtf.csrf import generate_csrf
    @app.context_processor
    def inject_csrf():
        return {'csrf_token': generate_csrf}

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

    return app
