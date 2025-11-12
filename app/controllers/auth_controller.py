from flask import session
from flask_login import login_user, logout_user
from app.models import db
from app.models.user import User


class AuthController:
    @staticmethod
    def login(email, password, login_type='frontend'):
        """Authenticate user by email
        
        Args:
            email: User email
            password: User password
            login_type: 'frontend' or 'backend'
        """
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password) and user.is_active:
            login_user(user)
            # Set session type to distinguish frontend and backend sessions
            session['login_type'] = login_type
            return user
        return None
    
    @staticmethod
    def login_by_username(username, password, login_type='backend'):
        """Authenticate user by username (for backward compatibility)
        
        Args:
            username: User username
            password: User password
            login_type: 'frontend' or 'backend'
        """
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password) and user.is_active:
            login_user(user)
            # Set session type to distinguish frontend and backend sessions
            session['login_type'] = login_type
            return user
        return None
    
    @staticmethod
    def logout():
        """Logout user"""
        # Clear session type
        session.pop('login_type', None)
        logout_user()
    
    @staticmethod
    def create_user(username, email, password, id_number=None, user_type='customer', store_id=None):
        """Create a new user"""
        if User.query.filter_by(username=username).first():
            raise ValueError('使用者名稱已存在')
        if User.query.filter_by(email=email).first():
            raise ValueError('電子郵件已存在')
        
        user = User(
            username=username,
            email=email,
            id_number=id_number,
            user_type=user_type,
            store_id=store_id
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

