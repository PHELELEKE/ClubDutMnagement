import sqlite3

conn = sqlite3.connect('c:/Users/DELL/Desktop/ClubManagement/student_club_management/instance/clubmanagement.db')
cursor = conn.cursor()

# Show user login details - email and student_number
print('=== USER LOGIN DETAILS ===')
print('Email                 | Student Number')
print('-' * 50)
cursor.execute("SELECT email, student_number FROM user;")
for row in cursor.fetchall():
    print(f'{row[0]:<22} | {row[1]}')

conn.close()

