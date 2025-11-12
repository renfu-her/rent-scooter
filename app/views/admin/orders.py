from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from app.controllers.order_controller import OrderController
from app.controllers.partner_controller import PartnerController
from app.controllers.motorcycle_controller import MotorcycleController
from app.utils.decorators import store_admin_required

admin_orders_bp = Blueprint('admin_orders', __name__)


@admin_orders_bp.route('')
@admin_orders_bp.route('/')
@store_admin_required
def index():
    """List all orders"""
    orders = OrderController.get_all()
    return render_template('admin/orders/index.html', orders=orders)


@admin_orders_bp.route('/create', methods=['GET', 'POST'])
@store_admin_required
def create():
    """Create new order"""
    partners = PartnerController.get_all()
    if request.method == 'POST':
        try:
            reservation_date = None
            if request.form.get('reservation_date'):
                reservation_date = datetime.strptime(request.form.get('reservation_date'), '%Y-%m-%d').date()
            
            rental_start_time = None
            if request.form.get('rental_start_time'):
                rental_start_time = datetime.strptime(request.form.get('rental_start_time'), '%Y-%m-%dT%H:%M')
            
            rental_end_time = None
            if request.form.get('rental_end_time'):
                rental_end_time = datetime.strptime(request.form.get('rental_end_time'), '%Y-%m-%dT%H:%M')
            
            ferry_departure_time = None
            if request.form.get('ferry_departure_time'):
                ferry_departure_time = datetime.strptime(request.form.get('ferry_departure_time'), '%Y-%m-%dT%H:%M')
            
            ferry_return_time = None
            if request.form.get('ferry_return_time'):
                ferry_return_time = datetime.strptime(request.form.get('ferry_return_time'), '%Y-%m-%dT%H:%M')
            
            estimated_return_time = None
            if request.form.get('estimated_return_time'):
                estimated_return_time = datetime.strptime(request.form.get('estimated_return_time'), '%Y-%m-%dT%H:%M')
            
            motorcycle_ids = request.form.getlist('motorcycle_ids')
            motorcycle_ids = [int(id) for id in motorcycle_ids if id]
            
            OrderController.create(
                partner_id=int(request.form.get('partner_id')) if request.form.get('partner_id') else None,
                renter_id=request.form.get('renter_id') or None,
                renter_name=request.form.get('renter_name') or None,
                renter_id_number=request.form.get('renter_id_number') or None,
                has_license=request.form.get('has_license') == 'true' if request.form.get('has_license') else None,
                rental_plan_id=int(request.form.get('rental_plan_id')) if request.form.get('rental_plan_id') else None,
                total_amount=float(request.form.get('total_amount', 0)),
                status=request.form.get('status', '待處理'),
                reservation_date=reservation_date or datetime.now().date(),
                rental_start_time=rental_start_time,
                rental_end_time=rental_end_time,
                shipping_company=request.form.get('shipping_company') or None,
                ferry_departure_time=ferry_departure_time,
                ferry_return_time=ferry_return_time,
                contact_phone=request.form.get('contact_phone') or None,
                payment_method=request.form.get('payment_method') or None,
                estimated_return_time=estimated_return_time,
                remarks=request.form.get('remarks') or None,
                motorcycle_ids=motorcycle_ids
            )
            flash('訂單建立成功', 'success')
            return redirect(url_for('admin_orders.index'))
        except Exception as e:
            flash(f'建立失敗: {str(e)}', 'error')
    return render_template('admin/orders/create.html', partners=partners)


@admin_orders_bp.route('/<int:order_id>')
@store_admin_required
def detail(order_id):
    """View order detail"""
    order = OrderController.get_by_id(order_id)
    counts, total = OrderController.get_motorcycle_counts_by_model(order_id)
    return render_template('admin/orders/detail.html', order=order, counts=counts, total=total)


@admin_orders_bp.route('/search_motorcycles')
@store_admin_required
def search_motorcycles():
    """Search motorcycles API endpoint"""
    q = request.args.get('q', '')
    motorcycles = MotorcycleController.search_by_license_plate(q, exclude_rented=True)
    return jsonify([{
        'id': m.id,
        'license_plate': m.license_plate,
        'model': m.model,
        'vehicle_type': m.vehicle_type,
        'status': m.status,
        'store_name': m.store.name if m.store else None
    } for m in motorcycles])
