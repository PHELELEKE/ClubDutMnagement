"""Initialize database with all tables"""
import os

# Remove old database if exists
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'club_management.db')
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Removed old database: {db_path}")

# Create new database with all tables
from app import create_app, db
from database import init_db

app = create_app()
with app.app_context():
    # Import all models to register them
    from models import (
        User, PreRegisteredStudent, Club, Event, Membership,
        Announcement, AnnouncementReaction, AnnouncementComment,
        Resource, Booking, Achievement, event_attendees,
        announcement_read_receipts, UserAchievement, EventAttendance,
        Notification, AnnouncementNotification, ChatConversation,
        ChatMessage, ChatRequest
    )
    
    db.create_all()
    print("Database created successfully with all tables!")

# Create admin user
from app import create_app, db
from models.user import User
from flask_bcrypt import Bcrypt

app = create_app()
bcrypt = Bcrypt(app)

with app.app_context():
    # Check if admin exists
    admin = User.query.filter_by(email='admin@dut.ac.za').first()
    if not admin:
        admin = User(
            student_number='ADMIN001',
            email='admin@dut.ac.za',
            password_hash=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            first_name='Admin',
            last_name='User',
            role='admin',
            email_verified=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: admin@dut.ac.za / admin123")
    else:
        print("Admin user already exists")

