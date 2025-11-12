from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.models import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    id_number = db.Column(db.String(20), nullable=True)  # 身份證字號
    user_type = db.Column(db.String(20), nullable=False, default='customer')  # admin, customer, store_admin
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    store = db.relationship('Store', backref='users', lazy=True)
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user is admin"""
        return self.user_type == 'admin'
    
    def is_store_admin(self):
        """Check if user is store admin"""
        return self.user_type == 'store_admin'
    
    def __repr__(self):
        return f'<User {self.username}>'

