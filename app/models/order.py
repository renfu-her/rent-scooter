from datetime import datetime
from app.models import db


class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    partner_id = db.Column(db.Integer, db.ForeignKey('partners.id'), nullable=True)
    renter_id = db.Column(db.String(200), nullable=True)  # 承租人 (text field)
    rental_plan_id = db.Column(db.Integer, nullable=True)  # 租賃方案
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='待處理', nullable=False)  # 待處理, 進行中, 已完成, 已取消
    reservation_date = db.Column(db.Date, nullable=False)
    rental_start_time = db.Column(db.DateTime, nullable=True)
    rental_end_time = db.Column(db.DateTime, nullable=True)
    shipping_company = db.Column(db.String(50), nullable=True)  # 泰富, 藍白, 聯營, 大福
    ferry_departure_time = db.Column(db.DateTime, nullable=True)
    ferry_return_time = db.Column(db.DateTime, nullable=True)
    contact_phone = db.Column(db.String(20), nullable=True)
    payment_method = db.Column(db.String(20), nullable=True)  # 現金, 月結, 日結
    estimated_return_time = db.Column(db.DateTime, nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    motorcycles = db.relationship('OrderMotorcycle', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.order_number}>'


class OrderMotorcycle(db.Model):
    __tablename__ = 'order_motorcycles'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    motorcycle_id = db.Column(db.Integer, db.ForeignKey('motorcycles.id'), nullable=False)
    
    def __repr__(self):
        return f'<OrderMotorcycle order_id={self.order_id} motorcycle_id={self.motorcycle_id}>'

