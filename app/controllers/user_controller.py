from app.models import db
from app.models.user import User
from app.controllers.auth_controller import AuthController


class UserController:
    @staticmethod
    def get_all(search=None, role_filter=None, status_filter=None):
        """Get all users with optional filters"""
        query = User.query
        
        if search:
            search_term = f'%{search}%'
            query = query.filter(
                (User.username.like(search_term)) |
                (User.email.like(search_term))
            )
        
        if role_filter and role_filter != 'all':
            query = query.filter_by(user_type=role_filter)
        
        if status_filter and status_filter != 'all':
            is_active = status_filter == 'active'
            query = query.filter_by(is_active=is_active)
        
        return query.order_by(User.created_at.desc()).all()
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        return User.query.get_or_404(user_id)
    
    @staticmethod
    def create(username, email, password, user_type='customer', store_id=None, is_active=True):
        """Create a new user"""
        try:
            user = AuthController.create_user(
                username=username,
                email=email,
                password=password,
                user_type=user_type,
                store_id=store_id
            )
            user.is_active = is_active
            db.session.commit()
            return user
        except ValueError as e:
            raise ValueError(str(e))
    
    @staticmethod
    def update(user_id, username=None, email=None, password=None, user_type=None, 
               store_id=None, is_active=None):
        """Update user"""
        user = User.query.get_or_404(user_id)
        
        if username and username != user.username:
            if User.query.filter_by(username=username).first():
                raise ValueError('使用者名稱已存在')
            user.username = username
        
        if email and email != user.email:
            if User.query.filter_by(email=email).first():
                raise ValueError('電子郵件已存在')
            user.email = email
        
        if password:
            user.set_password(password)
        
        if user_type is not None:
            user.user_type = user_type
        
        if store_id is not None:
            user.store_id = store_id
        
        if is_active is not None:
            user.is_active = is_active
        
        db.session.commit()
        return user
    
    @staticmethod
    def delete(user_id):
        """Delete user"""
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

