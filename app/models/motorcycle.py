from datetime import datetime
from app.models import db


class Motorcycle(db.Model):
    __tablename__ = 'motorcycles'
    
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    license_plate = db.Column(db.String(20), unique=True, nullable=False, index=True)
    model = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(20), nullable=True)  # 黑, 白
    vehicle_type = db.Column(db.String(20), nullable=False)  # 白牌, 綠牌, 電輔車
    image_path = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(20), default='待出租', nullable=False)  # 待出租, 出租中, 預訂, 已出租, 下架
    reservation_expires_at = db.Column(db.DateTime, nullable=True)  # 預訂到期時間
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    order_motorcycles = db.relationship('OrderMotorcycle', backref='motorcycle', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Motorcycle {self.license_plate}>'

