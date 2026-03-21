# 🔐 Email Password Reset - Quick Setup Guide

## What's New?
Your Student Club Management System now has a complete email-based password reset feature!

## ✨ Features
- **Forgot Password** link on login page
- **Secure reset emails** with one-time tokens
- **1-hour expiration** for security
- **Strong password requirements** (8+ chars, uppercase, lowercase, number, special char)
- **Professional email templates** matching your liquid glass design
- **Generic error messages** to prevent account enumeration

## 🚀 Quick Setup (5 minutes)

### Step 1: Configure Email
Edit `.env` file and uncomment/update email settings:

**For Gmail (Recommended):**
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

⚠️ For Gmail, you MUST:
1. Go to https://myaccount.google.com/apppasswords
2. Generate an "App Password" for "Mail - Windows Computer"
3. Use the 16-character password in `MAIL_PASSWORD`

### Step 2: Restart Flask App
```bash
python run.py
```

### Step 3: Test the Feature
1. Go to http://localhost:5000/login
2. Click "Forgot password?"
3. Enter a registered email
4. Check your email for reset link
5. Click link and set new password

## 📧 Email Configuration Options

### Gmail
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=app-password-16-chars
```

### Outlook/Office365
```env
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password
```

### University Email
Contact your IT department for SMTP settings and fill in accordingly.

## 🔒 Password Requirements
Users must create passwords with:
- ✓ Minimum 8 characters
- ✓ At least one uppercase letter (A-Z)
- ✓ At least one lowercase letter (a-z)
- ✓ At least one number (0-9)
- ✓ At least one special character (!@#$%^&*(),.?":{}|<>)

**Valid Examples:**
- `MyPassword123!`
- `Secure#Pass2024`
- `Club@Management99`

## 📍 Routes Added

| Route | Method | Purpose |
|-------|--------|---------|
| `/forgot-password` | GET/POST | Request password reset |
| `/reset-password/<token>` | GET/POST | Set new password |

## 🐛 Troubleshooting

**"Email not sending?"**
1. Check MAIL_SERVER and MAIL_PORT in .env
2. For Gmail: Verify app password is 16 characters
3. Check Flask console logs for SMTP errors

**"Token expired error?"**
1. Reset links expire after 1 hour
2. User must request new link if expired

**"Password requirements too strict?"**
Edit `routes/auth.py` → `validate_password_strength()` function

## 📁 Files Changed

### New Files Created:
```
templates/auth/forgot-password.html
templates/auth/reset-password.html
templates/auth/email/reset_password.html
templates/auth/email/reset_password.txt
templates/auth/email/password_changed.html
PASSWORD_RESET_FEATURE.md
```

### Modified Files:
```
models/user.py              (Added reset_token_expiry)
routes/auth.py              (Added password reset routes)
templates/auth/login.html   (Added forgot password link)
.env                        (Email configuration)
```

## 🎯 User Flow

```
User clicks "Forgot password?"
         ↓
   Enters registered email
         ↓
System sends reset link via email
         ↓
User clicks link in email
         ↓
User enters new password
         ↓
System validates password strength
         ↓
Password updated & confirmation email sent
         ↓
User redirected to login page
```

## 🔐 Security Features

- ✓ Secure random tokens (secrets module)
- ✓ One-time use only
- ✓ 1-hour expiration
- ✓ No email enumeration (generic messages)
- ✓ Password strength requirements
- ✓ Optional confirmation email
- ✓ Tokens stored uniquely in database

## 📚 Full Documentation

For detailed information, see: `PASSWORD_RESET_FEATURE.md`

Topics covered:
- Complete setup guide
- Email template customization
- Testing scenarios
- API endpoints
- Troubleshooting
- Future enhancements

## ✅ Verification Checklist

- [ ] Email configuration added to .env
- [ ] Flask app restarted
- [ ] "Forgot password?" link visible on login page
- [ ] Email received when requesting reset
- [ ] Password reset link works
- [ ] New password validated for strength
- [ ] Confirmation email received (optional)

## 🆘 Need Help?

1. Check `PASSWORD_RESET_FEATURE.md` for detailed docs
2. Review `.env.example` for email setup
3. Check Flask console for error messages
4. Verify MAIL_USERNAME and MAIL_PASSWORD are correct

---

**Ready to use!** 🚀

Your password reset feature is now active. Users can click "Forgot password?" on the login page anytime they need to reset their password.
