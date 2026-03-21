# DUT Club Management System - Setup Guide

## Step 1: Navigate to Project Directory
```powershell
cd C:\Users\DELL\Desktop\ClubManagement\student_club_management
```

## Step 2: Create Virtual Environment (one-time only)
```powershell
python -m venv venv
```

## Step 3: Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

You should see `(venv)` at the start of your PowerShell prompt.

## Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```

This installs all required packages including Flask, SQLAlchemy, etc.

## Step 5: Initialize Database
```powershell
python init_db.py
```

This creates all database tables in your SQL Server instance.

## Step 6: Start Development Server
```powershell
python run.py
```

The app will start on `http://localhost:5000`

## Important Notes:

- Make sure your `.env` file contains the correct DATABASE_URL
- The SERVER is: `DESKTOP-QN2C237\SQLEXPRESS`
- The DATABASE should be: `ClubManagementDB`
- Windows Authentication is used automatically

## Troubleshooting:

**If you get "pyodbc not found":**
```powershell
pip install pyodbc
```

**If you get database connection errors:**
- Make sure SQL Server is running
- Verify the server name: `DESKTOP-QN2C237\SQLEXPRESS`
- Check that you have ODBC Driver 17 for SQL Server installed

**To deactivate virtual environment later:**
```powershell
deactivate
```

## Next Time You Come Back:

Just do:
```powershell
cd C:\Users\DELL\Desktop\ClubManagement\student_club_management
.\venv\Scripts\Activate.ps1
python run.py
```
