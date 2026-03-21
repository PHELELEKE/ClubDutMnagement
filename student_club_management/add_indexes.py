"""
Script to add database indexes for improved query performance.
"""
import sqlite3
conn = sqlite3.connect('c:/Users/DELL/Desktop/ClubManagement/student_club_management/instance/clubmanagement.db')
cursor = conn.cursor()

# Add indexes for performance
indexes = [
    'CREATE INDEX IF NOT EXISTS idx_notification_user_read ON notification(user_id, is_read)',
    'CREATE INDEX IF NOT EXISTS idx_chat_conversation ON chat_message(conversation_id, is_read)',
    'CREATE INDEX IF NOT EXISTS idx_chat_conversation_participants ON chat_conversation(participant_one, participant_two)',
    'CREATE INDEX IF NOT EXISTS idx_event_status ON event(status)',
    'CREATE INDEX IF NOT EXISTS idx_membership_user_club ON membership(user_id, club_id)',
    'CREATE INDEX IF NOT EXISTS idx_attendance_event ON event_attendees(event_id)',
    'CREATE INDEX IF NOT EXISTS idx_attendance_user ON event_attendees(user_id)',
]

for idx in indexes:
    try:
        cursor.execute(idx)
        print(f'Created index successfully')
    except Exception as e:
        print(f'Error: {e}')

conn.commit()
conn.close()
print('Database indexes created successfully!')

