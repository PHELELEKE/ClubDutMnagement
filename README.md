# 🏫 DUT Club Management System

[![Railway Deploy](https://railway.app/button.svg)](https://railway.app/new)
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
Database: SQLite (local/test) / PostgreSQL (production)
Deployment: Railway or Render.com (free tiers)
```

## 📋 Quick Start (Local)

1. **Clone & Setup**
```powershell
git clone https://github.com/PHELELEKE/ClubManagementSystem.git
cd ClubManagementSystem
python -m venv venv
venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

2. **Run**
```powershell
python app.py
```
Open `http://localhost:5000` (or $PORT for Railway local test)

## 🌐 Deployment (Railway - Recommended, Free Postgres!)

1. Click Railway button above or go to [railway.app/new](https://railway.app/new)
2. Connect your GitHub repo
3. Railway auto-detects: Python, uses `Procfile`, `pip install -r requirements.txt`
4. **Add Postgres plugin**: Services → New → Database → PostgreSQL (sets DATABASE_URL)
5. **Add Variables** (Variables tab):
   - `SECRET_KEY` = `python -c "import secrets; print(secrets.token_hex(24))"`
   - Optional: `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_SUPPRESS_SEND=false`
6. **Deploy** → Live in ~2min! SQLite for quick test, Postgres for persistence.

**Procfile**: `web: gunicorn --bind 0.0.0.0:$PORT student_club_management.app:create_app()`

## 🌐 Alternative: Deployment (Render.com - Free!)

1. Fork/Connect this repo to Render.com
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `gunicorn --bind 0.0.0.0:$PORT student_club_management.app:create_app()`
4. SQLite auto-creates (ephemeral, resets daily)

## 🔄 Development Workflow
```
Edit locally → git add . → git commit → git push
↓ Auto-deploys to Railway/Render + GitHub Pages
```

## 📱 Online Editing
✨ Edit files directly at [github.com/PHELELEKE/ClubManagementSystem](https://github.com/PHELELEKE/ClubManagementSystem)

## 📂 Project Structure
```
ClubManagementSystem/
├── app.py              # Main Flask app (PORT-aware)
├── Procfile           # Railway/Render deploy
├── requirements.txt   # Dependencies + psycopg2-binary
├── railway-env.example # Env template
├── student_club_management/  # Core app, models, routes, templates
└── static/            # CSS/JS/Images
```

## 🐛 Troubleshooting
- **No data persistence**: Add Railway Postgres plugin
- **Emails**: `MAIL_SUPPRESS_SEND=false` + Gmail app password
- **Local SQL Server**: Only for dev (`config_fixed.py`)
- **Port issues**: `python app.py` binds $PORT automatically

## 🤝 Contributing
1. Fork repo
2. Create feature branch
3. Commit changes  
4. Push → Auto-deploy!

**Made with ❤️ for DUT Students**

![Screenshot](static/images/logo.png)

