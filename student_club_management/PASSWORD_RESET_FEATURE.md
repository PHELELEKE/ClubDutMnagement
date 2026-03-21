# Password Reset Feature - Implementation Guide

## Overview
This document describes the email-based password reset feature implemented in the Student Club Management System.

## Features

### User-Facing Features
1. **Forgot Password Link** - Users can click "Forgot password?" on the login page
2. **Email Verification** - System sends secure reset link to registered email
3. **Secure Token** - One-time use tokens that expire after 1 hour
4. **Password Strength Requirements** - Enforced password complexity:
   - Minimum 8 characters
   - At least one uppercase letter
   - At least one lowercase letter
   - At least one number
   - At least one special character (!@#$%^&*)
5. **Confirmation Email** - Optional confirmation email after successful reset

### Security Features
- **Secure Random Tokens** - Generated using Python's `secrets` module
- **Token Expiry** - Links expire after 1 hour
- **One-Time Use** - Tokens are deleted after successful use
- **Generic Messages** - System doesn't reveal whether email exists (security best practice)
- **Rate Limiting Ready** - Structure supports adding rate limiting
- **HTTPS Recommended** - Should be deployed over HTTPS in production

## Database Changes

### User Model Updates
Added two new fields to the `User` model:

```python
reset_token = db.Column(db.String(128), nullable=True, unique=True)
reset_token_expiry = db.Column(db.DateTime, nullable=True)
```

## Email Configuration

### Setup Instructions

#### Option 1: Gmail (Recommended for Testing)
1. Enable 2-Factor Authentication on your Gmail account
2. Visit: https://myaccount.google.com/apppasswords
3. Generate an "App Password" for "Mail - Windows Computer"
4. Copy the 16-character password
5. Update `.env` file:

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

#### Option 2: Outlook/Office365
```env
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password
```

#### Option 3: University Email
Contact your IT department for SMTP settings:
```env
MAIL_SERVER=smtp.your-university.ac.za
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@your-university.ac.za
MAIL_PASSWORD=your-password
```

## Routes

### /forgot-password
- **Method:** GET, POST
- **Description:** User enters email address to request password reset
- **Response:** 
  - Shows form (GET)
  - Sends email if account exists (POST)
  - Always shows success message for security

### /reset-password/<token>
- **Method:** GET, POST
- **Description:** User enters new password after clicking email link
- **URL Parameters:** 
  - `token`: Secure reset token from email
- **Validation:**
  - Token must be valid and not expired
  - Passwords must match
  - Password must meet strength requirements
- **Response:**
  - Shows form (GET)
  - Updates password and redirects to login (POST)

## Email Templates

### Structure
Three email templates are provided:

1. **reset_password.html** - Beautiful HTML email sent to user
2. **reset_password.txt** - Plain text fallback version
3. **password_changed.html** - Confirmation email after successful reset

### Customization
Email templates are located in `templates/auth/email/`

To customize:
1. Edit HTML/text templates
2. Update sender name in `send_reset_email()` function
3. Update app name in templates

Current sender: `DUT Club Management <noreply@dutclubs.com>`

## Testing

### Test Scenarios

#### 1. Valid Email Reset
```
1. Go to /forgot-password
2. Enter registered email
3. Check email for reset link
4. Click link from email
5. Enter new password matching requirements
6. Confirm password
7. Verify redirect to login with success message
```

#### 2. Invalid Email
```
1. Go to /forgot-password
2. Enter non-existent email
3. See generic success message (security feature)
4. No email sent
```

#### 3. Expired Token
```
1. Get valid reset link
2. Wait 1+ hour
3. Click expired link
4. See error message
5. Redirected to login with option to request new link
```

#### 4. Password Strength
```
1. Try password without uppercase: "password123@"
   → Error: "must contain at least one uppercase letter"
2. Try password without number: "Password@"
   → Error: "must contain at least one number"
3. Try short password: "Pass@1"
   → Error: "must be at least 8 characters"
```

#### 5. Mismatched Passwords
```
1. Enter "ValidPass@123" in password field
2. Enter "OtherPass@123" in confirm field
3. See error: "Passwords do not match"
```

## API Endpoints

### Form-Based (Standard)
- `GET /forgot-password` - Show forgot password form
- `POST /forgot-password` - Process email submission
- `GET /reset-password/<token>` - Show password reset form
- `POST /reset-password/<token>` - Process password change

## Password Requirements

Users must enter passwords that contain:
- ✓ Minimum 8 characters
- ✓ At least one uppercase letter (A-Z)
- ✓ At least one lowercase letter (a-z)
- ✓ At least one number (0-9)
- ✓ At least one special character (!@#$%^&*(),.?":{}|<>)

Examples:
- ✓ `MyPassword123!` - Valid
- ✓ `Secure#Pass2024` - Valid
- ✗ `password123` - Missing uppercase and special char
- ✗ `Pass@123` - Valid
- ✗ `Pass!` - Too short

## Security Best Practices

### Implemented
1. ✓ Secure random token generation
2. ✓ Token expiration (1 hour)
3. ✓ One-time use tokens
4. ✓ Password strength enforcement
5. ✓ Generic error messages (no email enumeration)
6. ✓ HTTPS recommended in production
7. ✓ Tokens stored uniquely in database

### Recommended Additional Measures
1. **Rate Limiting** - Limit reset requests to 3 per hour per IP
2. **HTTPS** - All password operations over HTTPS
3. **Audit Logging** - Log all password reset attempts
4. **Security Headers** - Add security headers to all responses
5. **CSRF Protection** - Already included via Flask-WTF

## Troubleshooting

### Emails Not Sending

**Problem:** Email configuration not working

**Solutions:**
1. Check MAIL_SERVER, MAIL_PORT in .env
2. Verify email credentials are correct
3. For Gmail: Ensure app password was generated correctly
4. Check Flask app logs for SMTP errors
5. Test connection:
   ```python
   from app import create_app, mail
   app = create_app()
   with app.app_context():
       with mail.connect() as conn:
           print("SMTP connection successful!")
   ```

### Token Expiry Not Working

**Problem:** Users can use expired tokens

**Solutions:**
1. Verify database migration added `reset_token_expiry` column
2. Ensure system time is correct (NTP sync)
3. Check token validation in `reset_password()` route

### Password Requirements Too Strict

**Problem:** Users finding requirements too complex

**Solution:** Modify `validate_password_strength()` in `routes/auth.py`

## Future Enhancements

### Possible Additions
1. **Rate Limiting** - Prevent password reset spam
2. **Two-Factor Authentication** - Additional security layer
3. **Reset History** - Track when passwords were reset
4. **Device Verification** - Verify reset from known device
5. **SMS Verification** - Optional SMS code verification
6. **Recovery Codes** - Backup access codes if email unavailable

## Files Modified

### Created
- `templates/auth/forgot-password.html` - Form for password reset request
- `templates/auth/reset-password.html` - Form for new password entry
- `templates/auth/email/reset_password.html` - HTML email template
- `templates/auth/email/reset_password.txt` - Text email template
- `templates/auth/email/password_changed.html` - Confirmation email

### Modified
- `models/user.py` - Added reset_token_expiry field
- `routes/auth.py` - Added password reset routes and functions
- `templates/auth/login.html` - Added "Forgot password?" link
- `.env` - Updated with email configuration examples

## Support

For issues or questions about this feature:
1. Check "Troubleshooting" section above
2. Review email configuration setup
3. Check application logs for errors
4. Contact system administrator

---

**Last Updated:** March 5, 2026
**Feature Version:** 1.0
