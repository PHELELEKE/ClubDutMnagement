# Fix Plan for Student Club Management

## Errors Identified and Fixed:

1. **app.py** - ImportError: `AnnouncementNotification` was imported from wrong module - FIXED
2. **app.py** - AttributeError: `Announcement.is_published` doesn't exist - FIXED

## Calendar Page Fixes (calendar.html):

3. **XSS Vulnerability**: Event titles were directly inserted into HTML without escaping - FIXED
   - Added `escapeHtml()` function to sanitize user input
   - All event titles are now properly escaped

4. **Date Handling**: Empty/null dates caused JavaScript errors - FIXED
   - Added `formatDate()` function to safely handle date parsing
   - Returns 'Date TBA' for invalid or missing dates

5. **JSON Parsing**: Used unsafe method to parse events data - FIXED
   - Changed from `{{ events | safe }}` to `JSON.parse('{{ events | tojson | safe }}')`
   - Added try-catch for safe JSON parsing
   - Falls back to empty array on parse errors

6. **Route Data Serialization**: Fixed events route to properly serialize event data
   - Changed from `json.dumps(events_data)` to passing `events_data` directly
   - Uses Jinja2's `tojson` filter in template for proper serialization
   - Handles null/None dates properly by using `None` instead of empty string

## Data at Rest Encryption - IMPLEMENTED:

### 1. Added Encryption Utilities
- Created `utils/encryption.py` with AES-256 encryption
- Uses PBKDF2HMAC for key derivation from machine-specific values
- Provides encrypt/decrypt functions for sensitive data

### 2. Updated User Model
- Added encrypted columns: `encrypted_student_number`, `encrypted_id_number`, `encrypted_email`
- Added `encrypt_sensitive_data()` and `decrypt_sensitive_data()` methods
- Added migration columns to database

### 3. Created Encryption Script
- Created `encrypt_existing_data.py` to encrypt existing PII
- Successfully encrypted 5 user records

### 4. Updated Dependencies
- Added `cryptography` package to requirements.txt
- Installed cryptography==46.0.5

