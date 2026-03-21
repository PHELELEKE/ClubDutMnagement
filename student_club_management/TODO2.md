# SQLAlchemy RuntimeError Fix Steps
- [x] Step 1: Add `db.app = app` to app_fixed.py create_app after db.init_app(app)
- [x] Step 2: Progress made on replacing 'from app import db' -> 'from app_fixed import db' (some files updated: user.py, auth.py, __init__.py; continue with remaining)
- [ ] Step 3: Test python run.py and access /

