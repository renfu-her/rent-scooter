from flask import Blueprint, redirect, url_for, render_template, flash, request, session
from flask_login import login_user, logout_user, current_user
from app.utils.decorators import backend_login_required
from app.controllers.motorcycle_controller import MotorcycleController
from app.controllers.order_controller import OrderController
from app.controllers.partner_controller import PartnerController
from app.controllers.store_controller import StoreController
from app.controllers.banner_controller import BannerController
from app.controllers.auth_controller import AuthController
from app.controllers.user_controller import UserController
from app.models.user import User
from app.models import db

backend_bp = Blueprint('backend', __name__)


@backend_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Backend login page"""
    # Check if user is already authenticated with backend session
    if current_user.is_authenticated and session.get('login_type') == 'backend':
        return redirect(url_for('backend.index'))
    
    # If user is authenticated but with frontend session, logout first
    if current_user.is_authenticated and session.get('login_type') == 'frontend':
        logout_user()
        session.pop('login_type', None)
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('請輸入使用者名稱和密碼', 'error')
            return render_template('auth/login.html')
        
        user = AuthController.login_by_username(username, password, login_type='backend')
        if user:
            flash(f'歡迎回來，{user.username}！', 'success')
            next_page = request.args.get('next')
            if not next_page:
                # Redirect based on user type
                if user.is_admin():
                    next_page = url_for('backend.index')
                elif user.is_store_admin():
                    next_page = url_for('backend.index')
                else:
                    next_page = url_for('frontend.index')
            return redirect(next_page)
        else:
            flash('使用者名稱或密碼錯誤', 'error')
    
    return render_template('auth/login.html')


@backend_bp.route('/')
@backend_login_required
def index():
    """Backend dashboard"""
    # Get statistics
    total_motorcycles = len(MotorcycleController.get_all())
    available_motorcycles = len(MotorcycleController.get_available())
    
    total_orders = len(OrderController.get_all())
    pending_orders = len([o for o in OrderController.get_all() if o.status == '待處理'])
    
    total_partners = len(PartnerController.get_all())
    total_stores = len(StoreController.get_all())
    total_banners = len(BannerController.get_active())
    total_users = User.query.count()
    admin_users = User.query.filter_by(user_type='admin').count()
    
    # Get recent orders
    recent_orders = OrderController.get_all()[:5]
    
    return render_template('admin/dashboard.html',
                         total_motorcycles=total_motorcycles,
                         available_motorcycles=available_motorcycles,
                         total_orders=total_orders,
                         pending_orders=pending_orders,
                         total_partners=total_partners,
                         total_stores=total_stores,
                         total_banners=total_banners,
                         total_users=total_users,
                         admin_users=admin_users,
                         recent_orders=recent_orders)


@backend_bp.route('/profile', methods=['GET', 'POST'])
@backend_login_required
def profile():
    """Backend user profile management"""
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            current_password = request.form.get('current_password', '').strip()
            new_password = request.form.get('new_password', '').strip()
            confirm_password = request.form.get('confirm_password', '').strip()
            
            if not username:
                flash('使用者名稱不能為空', 'error')
                return redirect(url_for('backend.profile'))
            if not email:
                flash('電子郵件不能為空', 'error')
                return redirect(url_for('backend.profile'))
            
            # Check if email is already taken by another user
            existing_user = User.query.filter(User.email == email, User.id != current_user.id).first()
            if existing_user:
                flash('此電子郵件已被使用', 'error')
                return redirect(url_for('backend.profile'))
            
            # Update basic info
            current_user.username = username
            current_user.email = email
            
            # Handle password change
            if new_password:
                if not current_password:
                    flash('請輸入當前密碼', 'error')
                    return redirect(url_for('backend.profile'))
                
                if not current_user.check_password(current_password):
                    flash('當前密碼錯誤', 'error')
                    return redirect(url_for('backend.profile'))
                
                if new_password != confirm_password:
                    flash('新密碼與確認密碼不一致', 'error')
                    return redirect(url_for('backend.profile'))
                
                if len(new_password) < 6:
                    flash('密碼長度至少需要6個字元', 'error')
                    return redirect(url_for('backend.profile'))
                
                current_user.set_password(new_password)
                flash('密碼已更新', 'success')
            
            db.session.commit()
            flash('個人資料更新成功', 'success')
            return redirect(url_for('backend.profile'))
        except Exception as e:
            flash(f'更新失敗：{str(e)}', 'error')
            db.session.rollback()
    
    return render_template('admin/profile.html', user=current_user)
