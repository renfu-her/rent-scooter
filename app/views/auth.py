from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app.controllers.auth_controller import AuthController
from app.utils.decorators import login_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('admin_motorcycles.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('請輸入使用者名稱和密碼', 'error')
            return render_template('auth/login.html')
        
        user = AuthController.login(username, password)
        if user:
            flash(f'歡迎回來，{user.username}！', 'success')
            next_page = request.args.get('next')
            if not next_page:
                # Redirect based on user type
                if user.is_admin():
                    next_page = url_for('admin_motorcycles.index')
                elif user.is_store_admin():
                    next_page = url_for('admin_motorcycles.index')
                else:
                    next_page = url_for('frontend.index')
            return redirect(next_page)
        else:
            flash('使用者名稱或密碼錯誤', 'error')
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Logout"""
    logout_user()
    flash('您已成功登出', 'info')
    return redirect(url_for('auth.login'))
