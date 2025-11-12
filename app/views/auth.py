from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_user, logout_user, current_user
from app.controllers.auth_controller import AuthController
from app.utils.decorators import login_required
from app.utils.id_validator import validate_taiwan_id, format_taiwan_id

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page (backend)"""
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


@auth_bp.route('/frontend/login', methods=['GET', 'POST'])
def frontend_login():
    """Frontend login/register page"""
    # Check if user is already authenticated with frontend session
    if current_user.is_authenticated and session.get('login_type') == 'frontend' and current_user.user_type == 'customer':
        return redirect(url_for('frontend.index'))
    
    # If user is authenticated but with backend session, logout first
    if current_user.is_authenticated and session.get('login_type') == 'backend':
        logout_user()
        session.pop('login_type', None)
    
    return render_template('frontend/login.html')


@auth_bp.route('/api/frontend/login', methods=['POST'])
def api_frontend_login():
    """API endpoint for frontend login"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': '請輸入電子郵件和密碼'}), 400
        
        user = AuthController.login(email, password, login_type='frontend')
        if user:
            if user.user_type != 'customer':
                return jsonify({'error': '此帳號無法使用前端登入'}), 403
            return jsonify({
                'success': True,
                'message': f'歡迎回來，{user.username}！',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'id_number': user.id_number
                }
            }), 200
        else:
            return jsonify({'error': '電子郵件或密碼錯誤'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/api/frontend/register', methods=['POST'])
def api_frontend_register():
    """API endpoint for frontend registration"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        id_number = data.get('id_number', '').strip() or None
        
        if not username:
            return jsonify({'error': '請輸入使用者名稱'}), 400
        if not email:
            return jsonify({'error': '請輸入電子郵件'}), 400
        if not password:
            return jsonify({'error': '請輸入密碼'}), 400
        if len(password) < 6:
            return jsonify({'error': '密碼長度至少需要6個字元'}), 400
        
        # Validate ID number if provided
        if id_number:
            id_number = format_taiwan_id(id_number)
            is_valid, error_msg = validate_taiwan_id(id_number)
            if not is_valid:
                return jsonify({'error': error_msg}), 400
        
        user = AuthController.create_user(
            username=username,
            email=email,
            password=password,
            id_number=id_number,
            user_type='customer'
        )
        
        # Auto login after registration
        from flask import session
        login_user(user)
        session['login_type'] = 'frontend'  # Set session type for frontend
        
        return jsonify({
            'success': True,
            'message': f'註冊成功，歡迎 {user.username}！',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'id_number': user.id_number
            }
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/logout')
@login_required
def logout():
    """Logout"""
    user_type = current_user.user_type if current_user.is_authenticated else None
    logout_user()
    flash('您已成功登出', 'info')
    
    # Redirect based on user type
    if user_type == 'customer':
        return redirect(url_for('auth.frontend_login'))
    else:
        return redirect(url_for('auth.login'))
