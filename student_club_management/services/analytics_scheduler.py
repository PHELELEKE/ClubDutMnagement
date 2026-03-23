from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalyticsScheduler:
    """Scheduler for automated analytics and reminders"""
    
    def __init__(self, app=None):
        self.scheduler = BackgroundScheduler()
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize scheduler with Flask app"""
        self.app = app
        with app.app_context():
            self.setup_scheduler()
    
    def setup_scheduler(self):
        """Setup all scheduled tasks"""
        logger.info("Setting up analytics scheduler...")
        
        # Schedule daily analytics calculation at 2 AM
        self.scheduler.add_job(
            func=self.calculate_daily_analytics,
            trigger=CronTrigger(hour=2, minute=0),
            id='daily_analytics',
            name='Calculate daily analytics',
            replace_existing=True
        )
        
        # Schedule event reminders - every hour
        self.scheduler.add_job(
            func=self.send_event_reminders,
            trigger=CronTrigger(minute=0),
            id='hourly_event_reminders',
            name='Send hourly event reminders',
            replace_existing=True
        )
        
        # Schedule club reminders - every 6 hours
        self.scheduler.add_job(
            func=self.send_club_reminders,
            trigger=CronTrigger(hour='*/6'),
            id='club_reminders',
            name='Send club reminders',
            replace_existing=True
        )
        
        # Schedule weekly cleanup - every Sunday at 3 AM
        self.scheduler.add_job(
            func=self.cleanup_old_data,
            trigger=CronTrigger(day_of_week='sun', hour=3, minute=0),
            id='weekly_cleanup',
            name='Weekly cleanup of old data',
            replace_existing=True
        )
        
        # Start scheduler
        try:
            self.scheduler.start()
            logger.info("✅ Analytics scheduler started successfully")
            
            # Register shutdown handler
            atexit.register(lambda: self.scheduler.shutdown())
            
        except Exception as e:
            logger.error(f"❌ Failed to start scheduler: {e}")
    
    def calculate_daily_analytics(self):
        """Calculate daily analytics metrics"""
        try:
            with self.app.app_context():
                logger.info("📊 Calculating daily analytics...")
                
                # Import services here to avoid circular imports
                from services.analytics_service import AnalyticsService
                
                # Calculate analytics for the last 30 days
                AnalyticsService.calculate_membership_growth(30)
                AnalyticsService.calculate_event_attendance(30)
                AnalyticsService.calculate_participation_trends(30)
                
                logger.info("✅ Daily analytics calculation completed")
                
        except Exception as e:
            logger.error(f"❌ Error calculating daily analytics: {e}")
    
    def send_event_reminders(self):
        """Send event reminders (1 day and 5 hours before)"""
        try:
            with self.app.app_context():
                logger.info("📧 Sending event reminders...")
                
                # Enhanced reminder service with specific timing
                self.send_event_reminders_enhanced()
                
                logger.info("✅ Event reminders sent successfully")
                
        except Exception as e:
            logger.error(f"❌ Error sending event reminders: {e}")
    
    def send_event_reminders_enhanced(self):
        """Enhanced event reminders with 1 day and 5 hours before timing"""
        from datetime import datetime, timedelta
        from models.event import Event
        from models.attendance import EventAttendance
        from models.notification import Notification
        from models.analytics import EventReminder
        from app import db
        
        now = datetime.utcnow()
        
        # Calculate reminder times
        one_day_later = now + timedelta(days=1)
        five_hours_later = now + timedelta(hours=5)
        
        # 1 day before reminders
        events_1day = Event.query.filter(
            Event.event_date >= now,
            Event.event_date <= one_day_later,
            Event.status == 'approved'
        ).all()
        
        for event in events_1day:
            attendees = EventAttendance.query.filter_by(event_id=event.id).all()
            for attendance in attendees:
                # Check if 1-day reminder already sent
                existing = EventReminder.query.filter_by(
                    event_id=event.id,
                    user_id=attendance.user_id,
                    reminder_type='1_day'
                ).first()
                
                if not existing:
                    # Send notification
                    Notification.create_event_reminder(
                        attendance.user_id,
                        event,
                        '1_day',
                        f"🗓️ Reminder: {event.event_name} is tomorrow at {event.event_date.strftime('%I:%M %p')}!"
                    )
                    
                    # Track reminder
                    reminder = EventReminder(
                        event_id=event.id,
                        user_id=attendance.user_id,
                        reminder_type='1_day'
                    )
                    db.session.add(reminder)
        
        # 5 hours before reminders
        events_5hours = Event.query.filter(
            Event.event_date >= now,
            Event.event_date <= five_hours_later,
            Event.status == 'approved'
        ).all()
        
        for event in events_5hours:
            attendees = EventAttendance.query.filter_by(event_id=event.id).all()
            for attendance in attendees:
                # Check if 5-hour reminder already sent
                existing = EventReminder.query.filter_by(
                    event_id=event.id,
                    user_id=attendance.user_id,
                    reminder_type='5_hours'
                ).first()
                
                if not existing:
                    # Send notification
                    Notification.create_event_reminder(
                        attendance.user_id,
                        event,
                        '5_hours',
                        f"⏰ URGENT: {event.event_name} starts in 5 hours at {event.event_date.strftime('%I:%M %p')}!"
                    )
                    
                    # Track reminder
                    reminder = EventReminder(
                        event_id=event.id,
                        user_id=attendance.user_id,
                        reminder_type='5_hours'
                    )
                    db.session.add(reminder)
        
        db.session.commit()
    
    def send_club_reminders(self):
        """Send club activity reminders"""
        try:
            with self.app.app_context():
                logger.info("🏛️ Sending club reminders...")
                
                # Enhanced club reminders
                self.send_club_reminders_enhanced()
                
                logger.info("✅ Club reminders sent successfully")
                
        except Exception as e:
            logger.error(f"❌ Error sending club reminders: {e}")
    
    def send_club_reminders_enhanced(self):
        """Enhanced club reminders with specific timing"""
        from datetime import datetime, timedelta
        from models.club import Club
        from models.membership import Membership
        from models.notification import Notification
        from models.analytics import ClubReminder
        from app import db
        
        now = datetime.utcnow()
        
        # Get active clubs
        clubs = Club.query.filter_by(status='active').all()
        
        for club in clubs:
            # Get all club members
            members = Membership.query.filter_by(club_id=club.id, status='active').all()
            
            for member in members:
                # Check if weekly club reminder already sent this week
                existing = ClubReminder.query.filter_by(
                    club_id=club.id,
                    user_id=member.user_id,
                    reminder_type='weekly_activity'
                ).filter(
                    ClubReminder.sent_at >= now - timedelta(days=7)
                ).first()
                
                if not existing:
                    # Send weekly activity reminder
                    Notification.create_club_reminder(
                        member.user_id,
                        club,
                        'weekly_activity',
                        f"🏛️ Weekly reminder: Stay active in {club.club_name}! Check for upcoming events and meetings."
                    )
                    
                    # Track reminder
                    reminder = ClubReminder(
                        club_id=club.id,
                        user_id=member.user_id,
                        reminder_type='weekly_activity'
                    )
                    db.session.add(reminder)
        
        db.session.commit()
    
    def cleanup_old_data(self):
        """Clean up old analytics and reminder data"""
        try:
            with self.app.app_context():
                logger.info("🧹 Cleaning up old data...")
                
                # Clean up analytics data older than 90 days
                from models.analytics import Analytics, EventReminder, ClubReminder
                from app import db
                
                cutoff_date = datetime.utcnow() - timedelta(days=90)
                
                # Delete old analytics
                old_analytics = Analytics.query.filter(
                    Analytics.created_at < cutoff_date
                ).delete()
                
                # Delete old reminders (keep for 30 days)
                reminder_cutoff = datetime.utcnow() - timedelta(days=30)
                old_event_reminders = EventReminder.query.filter(
                    EventReminder.sent_at < reminder_cutoff
                ).delete()
                
                old_club_reminders = ClubReminder.query.filter(
                    ClubReminder.sent_at < reminder_cutoff
                ).delete()
                
                db.session.commit()
                
                logger.info(f"✅ Cleanup completed: {old_analytics} analytics, {old_event_reminders} event reminders, {old_club_reminders} club reminders removed")
                
        except Exception as e:
            logger.error(f"❌ Error during cleanup: {e}")

# Global scheduler instance
analytics_scheduler = AnalyticsScheduler()
