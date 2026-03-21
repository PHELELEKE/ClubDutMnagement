"""
app.py – main application factory
---------------------------------
Setup instructions (run this once you have cloned the repo):

1. Create and activate a Python virtual environment:
   powershell
   python -m venv venv
   .\\venv\\Scripts\\Activate.ps1  # Windows PowerShell
   
2. Install dependencies:
   bash
   pip install -r requirements.txt
   
3. Update the `.env` file with your configuration values.  The SQLAlchemy
   URI is already populated with the SQL Server connection string using
   Windows authentication.
4. Initialize the database:
   python
   from app import create_app, db
   app = create_app()
   with app.app_context():
       from database import init_db
       init_db(app)  # creates tables
   
   Alternatively use Flask-Migrate if you add migrations.
5. Start the development server:
   bash
   python run.py

Once running, point your browser at `http://localhost:5000`.

"""

from flask import Flask, render_template
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
# from flask_wtf import FlaskForm as FlaskWTF  # Fixed import - no global init needed
from flask_mail import Mail
from flask_caching import Cache
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
# wtf = FlaskWTF()  # Fixed - init in create_app
mail = Mail()
cache = Cache()
scheduler = BackgroundScheduler()

# configure login behavior
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
    """Factory to create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    wtf.init_app(app)
    mail.init_app(app)
    cache.init_app(app)

    # CSRF protection for all routes
    from flask_wtf.csrf import CSRFProtect
    csrf = CSRFProtect(app)

    # register blueprints
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

    # Start the scheduler for reminder notifications
    scheduler.app = app
    # Run every hour to check for upcoming events/meetings
    scheduler.add_job(func=send_hourly_reminders, trigger="interval", hours=1, id='send_reminders')
    scheduler.start()
    # Shut down scheduler when app exits
    atexit.register(lambda: scheduler.shutdown())

    # CSRF context processor for {{ csrf_token() }} in templates
    from flask_wtf.csrf import generate_csrf
    @app.context_processor
    def inject_csrf():
        return {'csrf_token': generate_csrf}

    # Before request - calculate unread counts for authenticated users
    @app.before_request
    def before_request():
        from flask_login import current_user
        from flask import g
        from models.notification import Notification
        from models.chat import ChatMessage, ChatConversation
        from models.announcement import Announcement
        from models.notification import Notification, AnnouncementNotification
        from sqlalchemy import select, func
        
        if current_user.is_authenticated:
            # Calculate unread notifications (optimized query)
            unread_notifications = db.session.query(func.count(Notification.id)).filter(
                Notification.user_id == current_user.id,
                Notification.is_read == False
            ).scalar() or 0
            
            # Calculate unread chat messages (optimized query)
            unread_messages = db.session.query(func.count(ChatMessage.id)).join(
                ChatConversation,
                ChatMessage.conversation_id == ChatConversation.id
            ).filter(
                ((ChatConversation.participant_one == current_user.id) | 
                 (ChatConversation.participant_two == current_user.id)) &
                 (ChatMessage.sender_id != current_user.id) &
                 (ChatMessage.is_read == False)
            ).scalar() or 0
            
            # Calculate unread announcements - only count announcements user can access
            # Get user's accessible club IDs first
            from models.club import Club
            from models.membership import Membership
            
            user_club_ids = []
            if current_user.role == 'admin':
                # Admin can see all clubs
                user_club_ids = [c.id for c in Club.query.all()]
            elif current_user.role == 'leader':
                # Leader sees their clubs and clubs they're members of
                leader_clubs = Club.query.filter_by(created_by=current_user.id).all()
                member_clubs = Club.query.join(Membership).filter(
                    Membership.user_id == current_user.id,
                    Membership.status == 'active'
                ).all()
                user_club_ids = list(set([c.id for c in leader_clubs] + [c.id for c in member_clubs]))
            else:
                # Regular student sees their club memberships
                memberships = Membership.query.filter_by(user_id=current_user.id, status='active').all()
                user_club_ids = [m.club_id for m in memberships]
            
            # Only count unread announcements from clubs user can access
            if user_club_ids:
                read_receipts = db.session.query(AnnouncementNotification.announcement_id).filter(
                    AnnouncementNotification.user_id == current_user.id
                ).subquery()
                unread_announcements = db.session.query(func.count(Announcement.id)).filter(
                    Announcement.club_id.in_(user_club_ids),
                    ~Announcement.id.in_(select(read_receipts))
                ).scalar() or 0
            else:
                unread_announcements = 0
            
            # Make available in templates
            g.unread_notifications = unread_notifications
            g.chat_unread_count = unread_messages
            g.unread_announcements = unread_announcements

    # home route
    @app.route('/')
    def index():
        return render_template('index.html')

    # error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

    return app

