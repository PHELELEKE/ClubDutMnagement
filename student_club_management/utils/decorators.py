from functools import wraps
from flask_login import current_user
from flask import redirect, url_for

def leader_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or getattr(current_user, 'role', '') != 'leader':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
