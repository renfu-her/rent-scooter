from flask import jsonify, request
from datetime import datetime
from app.views.api.orders import api_orders_bp
from app.controllers.order_controller import OrderController
from app.utils.decorators import login_required


@api_orders_bp.route('', methods=['GET'])
@login_required
def list_orders():
    """Get all orders"""
    orders = OrderController.get_all()
    return jsonify([{
        'id': o.id,
        'order_number': o.order_number,
        'partner_id': o.partner_id,
        'renter_id': o.renter_id,
        'total_amount': float(o.total_amount),
        'status': o.status,
        'reservation_date': o.reservation_date.isoformat() if o.reservation_date else None,
        'motorcycle_count': len(o.motorcycles)
    } for o in orders])


@api_orders_bp.route('/<int:order_id>', methods=['GET'])
@login_required
def get_order(order_id):
    """Get order by ID"""
    order = OrderController.get_by_id(order_id)
    counts, total = OrderController.get_motorcycle_counts_by_model(order_id)
    
    return jsonify({
        'id': order.id,
        'order_number': order.order_number,
        'partner_id': order.partner_id,
        'renter_id': order.renter_id,
        'rental_plan_id': order.rental_plan_id,
        'total_amount': float(order.total_amount),
        'status': order.status,
        'reservation_date': order.reservation_date.isoformat() if order.reservation_date else None,
        'rental_start_time': order.rental_start_time.isoformat() if order.rental_start_time else None,
        'rental_end_time': order.rental_end_time.isoformat() if order.rental_end_time else None,
        'shipping_company': order.shipping_company,
        'ferry_departure_time': order.ferry_departure_time.isoformat() if order.ferry_departure_time else None,
        'ferry_return_time': order.ferry_return_time.isoformat() if order.ferry_return_time else None,
        'contact_phone': order.contact_phone,
        'payment_method': order.payment_method,
        'estimated_return_time': order.estimated_return_time.isoformat() if order.estimated_return_time else None,
        'remarks': order.remarks,
        'motorcycles': [{
            'id': om.motorcycle_id,
            'license_plate': om.motorcycle.license_plate,
            'model': om.motorcycle.model
        } for om in order.motorcycles],
        'motorcycle_counts': counts,
        'motorcycle_total': total
    })


@api_orders_bp.route('', methods=['POST'])
@login_required
def create_order():
    """Create new order"""
    data = request.get_json()
    try:
        reservation_date = None
        if data.get('reservation_date'):
            reservation_date = datetime.fromisoformat(data.get('reservation_date')).date()
        
        rental_start_time = None
        if data.get('rental_start_time'):
            rental_start_time = datetime.fromisoformat(data.get('rental_start_time'))
        
        rental_end_time = None
        if data.get('rental_end_time'):
            rental_end_time = datetime.fromisoformat(data.get('rental_end_time'))
        
        ferry_departure_time = None
        if data.get('ferry_departure_time'):
            ferry_departure_time = datetime.fromisoformat(data.get('ferry_departure_time'))
        
        ferry_return_time = None
        if data.get('ferry_return_time'):
            ferry_return_time = datetime.fromisoformat(data.get('ferry_return_time'))
        
        estimated_return_time = None
        if data.get('estimated_return_time'):
            estimated_return_time = datetime.fromisoformat(data.get('estimated_return_time'))
        
        order = OrderController.create(
            partner_id=data.get('partner_id'),
            renter_id=data.get('renter_id'),
            rental_plan_id=data.get('rental_plan_id'),
            total_amount=data.get('total_amount', 0),
            status=data.get('status', '待處理'),
            reservation_date=reservation_date,
            rental_start_time=rental_start_time,
            rental_end_time=rental_end_time,
            shipping_company=data.get('shipping_company'),
            ferry_departure_time=ferry_departure_time,
            ferry_return_time=ferry_return_time,
            contact_phone=data.get('contact_phone'),
            payment_method=data.get('payment_method'),
            estimated_return_time=estimated_return_time,
            remarks=data.get('remarks'),
            motorcycle_ids=data.get('motorcycle_ids', [])
        )
        return jsonify({
            'id': order.id,
            'order_number': order.order_number
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@api_orders_bp.route('/<int:order_id>', methods=['PUT'])
@login_required
def update_order(order_id):
    """Update order"""
    data = request.get_json()
    try:
        update_data = {}
        
        if 'reservation_date' in data:
            update_data['reservation_date'] = datetime.fromisoformat(data['reservation_date']).date()
        if 'rental_start_time' in data:
            update_data['rental_start_time'] = datetime.fromisoformat(data['rental_start_time']) if data['rental_start_time'] else None
        if 'rental_end_time' in data:
            update_data['rental_end_time'] = datetime.fromisoformat(data['rental_end_time']) if data['rental_end_time'] else None
        if 'ferry_departure_time' in data:
            update_data['ferry_departure_time'] = datetime.fromisoformat(data['ferry_departure_time']) if data['ferry_departure_time'] else None
        if 'ferry_return_time' in data:
            update_data['ferry_return_time'] = datetime.fromisoformat(data['ferry_return_time']) if data['ferry_return_time'] else None
        if 'estimated_return_time' in data:
            update_data['estimated_return_time'] = datetime.fromisoformat(data['estimated_return_time']) if data['estimated_return_time'] else None
        
        # Copy other fields
        for key in ['partner_id', 'renter_id', 'rental_plan_id', 'total_amount', 'status',
                   'shipping_company', 'contact_phone', 'payment_method', 'remarks', 'motorcycle_ids']:
            if key in data:
                update_data[key] = data[key]
        
        order = OrderController.update(order_id, **update_data)
        return jsonify({
            'id': order.id,
            'order_number': order.order_number
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@api_orders_bp.route('/<int:order_id>', methods=['DELETE'])
@login_required
def delete_order(order_id):
    """Delete order"""
    try:
        OrderController.delete(order_id)
        return jsonify({'message': 'Order deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
