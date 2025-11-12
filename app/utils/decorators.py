from functools import wraps
from flask import redirect, url_for, flash, abort, session
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


def frontend_login_required(f):
    """Decorator to require frontend login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('請先登入以繼續', 'warning')
            return redirect(url_for('auth.frontend_login'))
        # Check if session is frontend type
        if session.get('login_type') != 'frontend':
            flash('請使用前端登入', 'warning')
            return redirect(url_for('auth.frontend_login'))
        return f(*args, **kwargs)
    return decorated_function


def backend_login_required(f):
    """Decorator to require backend login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('請先登入以繼續', 'warning')
            return redirect(url_for('auth.login'))
        # Check if session is backend type
        if session.get('login_type') != 'backend':
            flash('請使用後台登入', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin user"""
    @wraps(f)
    @backend_login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('您沒有權限訪問此頁面', 'error')
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def store_admin_required(f):
    """Decorator to require store admin or admin"""
    @wraps(f)
    @backend_login_required
    def decorated_function(*args, **kwargs):
        if not (current_user.is_admin() or current_user.is_store_admin()):
            flash('您沒有權限訪問此頁面', 'error')
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

