# 🏫 DUT Club Management System

[![Render Deploy](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/PHELELEKE/ClubManagementSystem)

## 🚀 Live Demo
**Live App**: https://club-management-system.onrender.com (deploys automatically)
**GitHub Pages**: https://pheleleke.github.io/ClubManagementSystem/ (static demo)

## ✨ Features
- 👥 **Student Registration/Login** (Student Number + Email)
- 🏢 **Club Management** (Create, Join, Lead clubs)
- 📅 **Events & Calendar** (RSVP, QR Attendance, Reminders)
- 💬 **Real-time Chat** (1:1 conversations)
- 🔔 **Smart Notifications** (Email + In-app)
- 📢 **Announcements** (Club-specific, reactions)
- 👑 **Admin Dashboard** (Users, Clubs, Events)
- 🔐 **Password Reset** (Email-based)
- 🎨 **Responsive UI** (Mobile/Desktop)

## 🛠 Tech Stack
```
Backend: Flask 3.0 + SQLAlchemy + APScheduler
Frontend: Jinja2 + Bootstrap5 + Custom CSS/JS
Database: SQLite (local) / PostgreSQL (production)
Deployment: Render.com (free tier)
```

## 📋 Quick Start (Local)

1. **Clone & Setup**
```powershell
git clone https://github.com/PHELELEKE/ClubManagementSystem.git
cd ClubManagementSystem
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. **Run**
```powershell
python run.py
```
Open `http://localhost:5000`

## 🌐 Deployment (Render.com - Free!)

1. Fork/Connect this repo to Render.com
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `gunicorn run:app`
4. **SQLite** auto-creates on first run

## 🔄 Development Workflow
```
Edit locally → git add . → git commit → git push
↓ Auto-deploys to Render + GitHub Pages
```

## 📱 Online Editing
✨ Edit files directly at [github.com/PHELELEKE/ClubManagementSystem](https://github.com/PHELELEKE/ClubManagementSystem)

## 📂 Project Structure
```
ClubManagementSystem/
├── app.py              # Main Flask app
├── run.py             # Server entrypoint  
├── requirements.txt   # Dependencies
├── student_club_management/  # All models, routes, templates
└── static/            # CSS/JS/Images
```

## 🐛 Troubleshooting
- **Emails**: Set `MAIL_SUPPRESS_SEND=false` + Gmail creds in .env
- **Database**: SQLite ephemeral on Render (resets daily)
- **SQL Server**: Local only - uses `DESKTOP-QN2C237\\SQLEXPRESS`

## 🤝 Contributing
1. Fork repo
2. Create feature branch
3. Commit changes  
4. Push → Auto-deploy!

**Made with ❤️ for DUT Students**

![Screenshot](static/images/logo.png)

