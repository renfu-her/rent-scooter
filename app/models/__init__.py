from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.user import User
from app.models.partner import Partner
from app.models.store import Store
from app.models.motorcycle import Motorcycle
from app.models.order import Order, OrderMotorcycle
from app.models.banner import Banner

__all__ = ['db', 'User', 'Partner', 'Store', 'Motorcycle', 'Order', 'OrderMotorcycle', 'Banner']

