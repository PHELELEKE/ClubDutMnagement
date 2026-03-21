"""
Functional Tests for Student Club Management System
Tests all features work correctly
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from models.user import User, PreRegisteredStudent
from models.club import Club
from models.event import Event
from models.membership import Membership
from models.notification import Notification
from datetime import datetime, timedelta


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        
        # Create test admin
        admin = User(
            student_number='12345678',
            email='admin@test.com',
            first_name='Admin',
            last_name='User',
            password_hash='hashed_password',
            role='admin'
        )
        db.session.add(admin)
        
        # Create test leader
        leader = User(
            student_number='12345679',
            email='leader@test.com',
            first_name='Club',
            last_name='Leader',
            password_hash='hashed_password',
            role='leader'
        )
        db.session.add(leader)
        
        # Create test student
        student = User(
            student_number='12345670',
            email='student@test.com',
            first_name='Test',
            last_name='Student',
            password_hash='hashed_password',
            role='student'
        )
        db.session.add(student)
        
        # Create pre-registered student
        pre_student = PreRegisteredStudent(
            student_number='99999999',
            id_number='1234567890123',
            first_name='New',
            last_name='Student',
            email='newstudent@test.com'
        )
        db.session.add(pre_student)
        
        db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def auth_client(client, app):
    """Create authenticated test client"""
    with app.app_context():
        # Get the admin user
        admin = User.query.filter_by(email='admin@test.com').first()
        
        with client.session_transaction() as sess:
            sess['_user_id'] = str(admin.id)
            sess['_fresh'] = True
        
        return client


# ==================== AUTH TESTS ====================

class TestAuthentication:
    """Test authentication functionality"""
    
    def test_login_page_loads(self, client):
        """Test login page loads correctly"""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Login' in response.data
    
    def test_register_page_loads(self, client):
        """Test register page loads correctly"""
        response = client.get('/register')
        assert response.status_code == 200
    
    def test_forgot_password_page_loads(self, client):
        """Test forgot password page loads correctly"""
        response = client.get('/forgot-password')
        assert response.status_code == 200
    
    def test_logout_redirects(self, auth_client):
        """Test logout redirects to home"""
        response = auth_client.get('/logout', follow_redirects=True)
        assert response.status_code == 200


# ==================== USER TESTS ====================

class TestUserManagement:
    """Test user management functionality"""
    
    def test_user_creation(self, app):
        """Test user can be created"""
        with app.app_context():
            user_count = User.query.count()
            assert user_count == 3  # admin, leader, student
    
    def test_pre_registered_student(self, app):
        """Test pre-registered student exists"""
        with app.app_context():
            pre_student = PreRegisteredStudent.query.filter_by(student_number='99999999').first()
            assert pre_student is not None
            assert pre_student.email == 'newstudent@test.com'
    
    def test_user_roles(self, app):
        """Test user roles are assigned correctly"""
        with app.app_context():
            admin = User.query.filter_by(role='admin').first()
            leader = User.query.filter_by(role='leader').first()
            student = User.query.filter_by(role='student').first()
            
            assert admin is not None
            assert leader is not None
            assert student is not None


# ==================== CLUB TESTS ====================

class TestClubManagement:
    """Test club management functionality"""
    
    def test_club_creation(self, auth_client, app):
        """Test club can be created"""
        with app.app_context():
            leader = User.query.filter_by(role='leader').first()
            
            club_data = {
                'club_name': 'Test Club',
                'description': 'A test club for testing',
                'category': 'Academic',
                'meeting_day': 'Monday',
                'meeting_time': '14:00'
            }
            
            response = auth_client.post('/clubs/create', data=club_data, follow_redirects=True)
            assert response.status_code == 200
            
            # Verify club was created
            club = Club.query.filter_by(club_name='Test Club').first()
            assert club is not None
            assert club.created_by == leader.id


# ==================== EVENT TESTS ====================

class TestEventManagement:
    """Test event management functionality"""
    
    def test_event_creation(self, auth_client, app):
        """Test event can be created"""
        with app.app_context():
            leader = User.query.filter_by(role='leader').first()
            
            # First create a club
            club = Club(
                club_name='Test Event Club',
                description='Club for events',
                category='Sports',
                created_by=leader.id,
                status='active'
            )
            db.session.add(club)
            db.session.commit()
            
            # Create event
            future_date = (datetime.utcnow() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M')
            
            event_data = {
                'event_name': 'Test Event',
                'description': 'A test event',
                'event_date': future_date,
                'location': 'Test Hall',
                'max_attendees': '50',
                'club_id': club.id
            }
            
            response = auth_client.post('/events/create', data=event_data, follow_redirects=True)
            assert response.status_code == 200
            
            # Verify event was created
            event = Event.query.filter_by(event_name='Test Event').first()
            assert event is not None
    
    def test_event_conflict_detection(self, app):
        """Test event conflict detection works"""
        with app.app_context():
            leader = User.query.filter_by(role='leader').first()
            
            # Create a club first
            club = Club(
                club_name='Conflict Test Club',
                description='Club for conflict testing',
                category='Sports',
                created_by=leader.id,
                status='active'
            )
            db.session.add(club)
            db.session.commit()
            
            # Create first event
            event_date = datetime.utcnow() + timedelta(days=7)
            event1 = Event(
                event_name='Event 1',
                description='First event',
                created_by=leader.id,
                event_date=event_date,
                location='Main Hall',
                status='approved',
                club_id=club.id
            )
            db.session.add(event1)
            db.session.commit()
            
            # Try to create conflicting event
            from routes.events import check_event_conflicts
            conflicting_event_date = event_date + timedelta(hours=1)
            conflicts = check_event_conflicts(
                conflicting_event_date, 
                conflicting_event_date + timedelta(hours=2),
                'Main Hall'
            )
            
