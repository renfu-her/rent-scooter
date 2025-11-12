from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from app.controllers.store_controller import StoreController
from app.controllers.motorcycle_controller import MotorcycleController
from app.models.motorcycle import Motorcycle
from app.utils.timezone_utils import check_expired_reservations
from app.utils.id_validator import validate_taiwan_id, format_taiwan_id

frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/')
def index():
    """Frontend homepage"""
    # Check expired reservations before loading
    check_expired_reservations()
    stores = StoreController.get_all()
    return render_template('frontend/index.html', stores=stores)


@frontend_bp.route('/stores/<int:store_id>')
def store_detail(store_id):
    """Store detail page"""
    # Check expired reservations before loading
    check_expired_reservations()
    store = StoreController.get_by_id(store_id)
    # Get motorcycles directly from model for frontend (no permission check needed)
    # Filter out '下架' status motorcycles
    motorcycles = Motorcycle.query.filter_by(store_id=store_id).filter(Motorcycle.status != '下架').all()
    return render_template('frontend/store_detail.html', store=store, motorcycles=motorcycles)


@frontend_bp.route('/api/motorcycles/<int:motorcycle_id>', methods=['GET'])
def get_motorcycle(motorcycle_id):
    """Get motorcycle details for reservation"""
    try:
        # Check expired reservations first
        check_expired_reservations()
        motorcycle = MotorcycleController.get_by_id_public(motorcycle_id)
        return jsonify({
            'id': motorcycle.id,
            'license_plate': motorcycle.license_plate,
            'model': motorcycle.model,
            'vehicle_type': motorcycle.vehicle_type,
            'color': motorcycle.color,
            'status': motorcycle.status,
            'image_path': motorcycle.image_path,
            'store_id': motorcycle.store_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@frontend_bp.route('/api/motorcycles/<int:motorcycle_id>/reserve', methods=['POST'])
def reserve_motorcycle(motorcycle_id):
    """Reserve a motorcycle"""
    try:
        data = request.get_json()
        
        # Validate required fields
        renter_name = data.get('renter_name', '').strip()
        renter_id_number = data.get('renter_id_number', '').strip()
        has_license = data.get('has_license', False)
        reservation_status = data.get('status', '預訂')
        contact_phone = data.get('contact_phone', '').strip() or None
        remarks = data.get('remarks', '').strip() or None
        
        if not renter_name:
            return jsonify({'error': '請輸入承租人姓名'}), 400
        if not renter_id_number:
            return jsonify({'error': '請輸入身份證號碼'}), 400
        
        # Format and validate Taiwan ID number
        renter_id_number = format_taiwan_id(renter_id_number)
        is_valid, error_msg = validate_taiwan_id(renter_id_number)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        motorcycle = MotorcycleController.reserve(
            motorcycle_id=motorcycle_id,
            renter_name=renter_name,
            renter_id_number=renter_id_number,
            has_license=has_license,
            reservation_status=reservation_status,
            contact_phone=contact_phone,
            remarks=remarks
        )
        
        return jsonify({
            'success': True,
            'message': '預訂成功',
            'motorcycle': {
                'id': motorcycle.id,
                'license_plate': motorcycle.license_plate,
                'status': motorcycle.status
            }
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
