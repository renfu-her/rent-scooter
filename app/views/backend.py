from flask import Blueprint, redirect, url_for, render_template
from app.utils.decorators import backend_login_required
from app.controllers.motorcycle_controller import MotorcycleController
from app.controllers.order_controller import OrderController
from app.controllers.partner_controller import PartnerController
from app.controllers.store_controller import StoreController
from app.controllers.banner_controller import BannerController
from app.models.user import User

backend_bp = Blueprint('backend', __name__)


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
