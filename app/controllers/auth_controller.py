from flask_login import login_user, logout_user
from app.models import db
from app.models.user import User


class AuthController:
    @staticmethod
    def login(email, password):
        """Authenticate user by email"""
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password) and user.is_active:
            login_user(user)
            return user
        return None
    
    @staticmethod
    def login_by_username(username, password):
        """Authenticate user by username (for backward compatibility)"""
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password) and user.is_active:
            login_user(user)
            return user
        return None
    
    @staticmethod
    def logout():
        """Logout user"""
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

