#!/usr/bin/env python
"""Seed database with test data"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db, bcrypt
from models.user import User
from models.club import Club
from models.membership import Membership
from models.event import Event
from datetime import datetime, timedelta

def seed_database():
    """Populate database with test records"""
    app = create_app()
    with app.app_context():
        # Clear existing data
        print("🗑️  Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Create admin user
        print("👤 Creating admin user...")
        admin = User(
            student_number='ADMIN001',
            email='admin@dut.ac.za',
            first_name='Administrator',
            last_name='System',
            password_hash=bcrypt.generate_password_hash('admin@123').decode('utf-8'),
            role='admin',
            is_active=True,
            email_verified=True
        )
        db.session.add(admin)
        
        # Create regular user
        print("👤 Creating regular user...")
        student = User(
            student_number='STU001',
            email='student@dut.ac.za',
            first_name='John',
            last_name='Doe',
            password_hash=bcrypt.generate_password_hash('student@123').decode('utf-8'),
            role='student',
            is_active=True,
            email_verified=True
        )
        db.session.add(student)
        
        # Create club leader user
        print("👤 Creating club leader user...")
        leader = User(
            student_number='STU002',
            email='leader@dut.ac.za',
            first_name='Sarah',
            last_name='Johnson',
            password_hash=bcrypt.generate_password_hash('leader@123').decode('utf-8'),
            role='leader',
            is_active=True,
            email_verified=True
        )
        db.session.add(leader)
        db.session.commit()
        
        # Create test clubs
        print("🎭 Creating test clubs...")
        club1 = Club(
            club_name='Photography Club',
            description='A club for photography enthusiasts to share their work and learn new techniques.',
            category='Arts',
            created_by=leader.id,
            max_members=20,
            meeting_schedule='Every Wednesday at 4 PM',
            status='active'
        )
        db.session.add(club1)
        
        club2 = Club(
            club_name='Coding Club',
            description='Join us to learn programming, algorithms, and build cool projects together.',
            category='Technical',
            created_by=leader.id,
            max_members=30,
            meeting_schedule='Every Friday at 5 PM',
            status='active'
        )
        db.session.add(club2)
        
        club3 = Club(
            club_name='Soccer Club',
            description='Come play soccer with us! All skill levels welcome.',
            category='Sports',
            created_by=leader.id,
            max_members=25,
            meeting_schedule='Every Tuesday and Thursday',
            status='pending'
        )
        db.session.add(club3)
        db.session.commit()
        
        # Create memberships
        print("🤝 Creating club memberships...")
        member1 = Membership(user_id=student.id, club_id=club1.id, role='member')
        member2 = Membership(user_id=student.id, club_id=club2.id, role='member')
        member3 = Membership(user_id=leader.id, club_id=club1.id, role='leader')
        member4 = Membership(user_id=leader.id, club_id=club2.id, role='leader')
        db.session.add_all([member1, member2, member3, member4])
        db.session.commit()
        
        # Create test events
        print("📅 Creating test events...")
        now = datetime.utcnow()
        
        # Open event - approved
        event1 = Event(
            event_name='Photography Workshop',
            description='Learn landscape photography techniques with experienced photographers.',
            created_by=leader.id,
            club_id=club1.id,
            event_date=now + timedelta(days=7),
            location='DUT Student Center - Room 101',
            max_attendees=30,
            requires_club=False,  # Open event
            status='approved'
        )
        db.session.add(event1)
        
        # Team event - pending approval
        event2 = Event(
            event_name='Coding Competition 2024',
            description='Compete with your club team in programming challenges.',
            created_by=leader.id,
            club_id=None,  # Organization-wide event
            event_date=now + timedelta(days=14),
            location='DUT Auditorium',
            max_attendees=100,
            requires_club=True,  # Team event
            min_club_members=3,
            max_club_members=8,
            status='pending'  # Awaiting admin approval
        )
        db.session.add(event2)
        
        # Another open event
        event3 = Event(
            event_name='Python Coding Session',
            description='Beginner-friendly session on Python fundamentals.',
            created_by=leader.id,
            club_id=club2.id,
            event_date=now + timedelta(days=3),
            location='Computer Lab B2',
            max_attendees=25,
            requires_club=False,
            status='approved'
        )
        db.session.add(event3)
        
        db.session.commit()
        
        # Add student to approved open event
        event1.attendees.append(student)
        db.session.commit()
        
        print("\n" + "="*60)
        print("✅ DATABASE SEEDED SUCCESSFULLY!")
        print("="*60)
        print("\n📝 TEST ACCOUNTS:\n")
        print("ADMIN ACCOUNT:")
        print("  Email: admin@dut.ac.za")
        print("  Password: admin@123")
        print("  Role: Administrator\n")
        print("LEADER ACCOUNT (has created clubs):")
        print("  Email: leader@dut.ac.za")
        print("  Password: leader@123")
        print("  Role: Club Leader\n")
        print("STUDENT ACCOUNT:")
        print("  Email: student@dut.ac.za")
        print("  Password: student@123")
        print("  Role: Student\n")
        print("📊 TEST DATA:")
        print("  • 3 Users (admin, leader, student)")
        print("  • 3 Clubs (2 active, 1 pending)")
        print("  • 3 Events:")
        print("    - Photography Workshop (Open event, approved)")
        print("    - Coding Competition (Team event, PENDING approval)")
        print("    - Python Coding Session (Open event, approved)")
        print("\n🎯 TASK WORKFLOW:")
        print("  1. Login as leader@dut.ac.za (leader@123)")
        print("  2. Try creating a new event with team requirements")
        print("  3. Login as admin@dut.ac.za to approve it")
        print("  4. Login as student to join events")
        print("\n🚀 Ready to start!")
        print("  Role: Club Leader")
        print("\nSTUDENT ACCOUNT:")
        print("  Email: student@dut.ac.za")
        print("  Password: password@123")
        print("  Role: Student")
        print("\n🎭 TEST DATA CREATED:")
        print("  • 3 clubs (Photography, Coding, Soccer)")
        print("  • 2 active clubs (Photography, Coding)")
        print("  • 1 pending club (Soccer)")
        print("  • 2 upcoming events")
        print("  • Club memberships linked")
        print("="*60)

if __name__ == '__main__':
    seed_database()
