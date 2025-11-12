from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from app.controllers.store_controller import StoreController
from app.controllers.motorcycle_controller import MotorcycleController
from app.models.motorcycle import Motorcycle
from app.utils.timezone_utils import check_expired_reservations

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
        reservation_status = data.get('status', '預訂')
        
        motorcycle = MotorcycleController.reserve(motorcycle_id, reservation_status)
        
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
