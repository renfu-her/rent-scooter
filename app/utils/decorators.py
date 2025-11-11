from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import current_user


def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('請先登入以繼續', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin user"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('您沒有權限訪問此頁面', 'error')
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def store_admin_required(f):
    """Decorator to require store admin or admin"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not (current_user.is_admin() or current_user.is_store_admin()):
            flash('您沒有權限訪問此頁面', 'error')
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

