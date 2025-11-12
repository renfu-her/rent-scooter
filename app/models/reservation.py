from datetime import datetime
from app.models import db


class Reservation(db.Model):
    __tablename__ = 'reservations'
    
    id = db.Column(db.Integer, primary_key=True)
    motorcycle_id = db.Column(db.Integer, db.ForeignKey('motorcycles.id'), nullable=False)
    renter_name = db.Column(db.String(100), nullable=False)  # 承租人姓名
    renter_id_number = db.Column(db.String(20), nullable=False)  # 身份證號碼
    has_license = db.Column(db.Boolean, default=False, nullable=False)  # 是否有駕照
    reservation_status = db.Column(db.String(20), default='預訂', nullable=False)  # 預訂, 出租中, 已出租
    reservation_expires_at = db.Column(db.DateTime, nullable=True)  # 預訂到期時間
    contact_phone = db.Column(db.String(20), nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    motorcycle = db.relationship('Motorcycle', backref='reservations', lazy=True)
    
    def __repr__(self):
        return f'<Reservation {self.renter_name} - {self.motorcycle_id}>'

