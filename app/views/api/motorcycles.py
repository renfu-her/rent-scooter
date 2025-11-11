from flask import jsonify, request
from app.views.api.motorcycles import api_motorcycles_bp
from app.controllers.motorcycle_controller import MotorcycleController
from app.utils.decorators import login_required


@api_motorcycles_bp.route('', methods=['GET'])
@login_required
def list_motorcycles():
    """Get all motorcycles"""
    store_id = request.args.get('store_id', type=int)
    available_only = request.args.get('available_only', 'false').lower() == 'true'
    
    if available_only:
        motorcycles = MotorcycleController.get_available(store_id)
    else:
        motorcycles = MotorcycleController.get_all(store_id)
    
    return jsonify([{
        'id': m.id,
        'store_id': m.store_id,
        'license_plate': m.license_plate,
        'model': m.model,
        'color': m.color,
        'vehicle_type': m.vehicle_type,
        'image_path': m.image_path,
        'status': m.status,
        'store_name': m.store.name if m.store else None
    } for m in motorcycles])


@api_motorcycles_bp.route('/search', methods=['GET'])
@login_required
def search_motorcycles():
    """Search motorcycles by license plate"""
    license_plate = request.args.get('q', '')
    exclude_rented = request.args.get('exclude_rented', 'true').lower() == 'true'
    
    if not license_plate:
        return jsonify([])
    
    motorcycles = MotorcycleController.search_by_license_plate(license_plate, exclude_rented)
    return jsonify([{
        'id': m.id,
        'store_id': m.store_id,
        'license_plate': m.license_plate,
        'model': m.model,
        'color': m.color,
        'vehicle_type': m.vehicle_type,
        'image_path': m.image_path,
        'status': m.status,
        'store_name': m.store.name if m.store else None
    } for m in motorcycles])


@api_motorcycles_bp.route('/<int:motorcycle_id>', methods=['GET'])
@login_required
def get_motorcycle(motorcycle_id):
    """Get motorcycle by ID"""
    motorcycle = MotorcycleController.get_by_id(motorcycle_id)
    return jsonify({
        'id': motorcycle.id,
        'store_id': motorcycle.store_id,
        'license_plate': motorcycle.license_plate,
        'model': motorcycle.model,
        'color': motorcycle.color,
        'vehicle_type': motorcycle.vehicle_type,
        'image_path': motorcycle.image_path,
        'status': motorcycle.status,
        'store_name': motorcycle.store.name if motorcycle.store else None
    })


@api_motorcycles_bp.route('', methods=['POST'])
@login_required
def create_motorcycle():
    """Create new motorcycle"""
    data = request.get_json()
    try:
        motorcycle = MotorcycleController.create(
            store_id=data.get('store_id'),
            license_plate=data.get('license_plate'),
            model=data.get('model'),
            vehicle_type=data.get('vehicle_type'),
            color=data.get('color'),
            image_path=data.get('image_path')
        )
        return jsonify({
            'id': motorcycle.id,
            'store_id': motorcycle.store_id,
            'license_plate': motorcycle.license_plate,
            'model': motorcycle.model,
            'color': motorcycle.color,
            'vehicle_type': motorcycle.vehicle_type,
            'image_path': motorcycle.image_path,
            'status': motorcycle.status
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@api_motorcycles_bp.route('/<int:motorcycle_id>', methods=['PUT'])
@login_required
def update_motorcycle(motorcycle_id):
    """Update motorcycle"""
    data = request.get_json()
    try:
        motorcycle = MotorcycleController.update(
            motorcycle_id,
            store_id=data.get('store_id'),
            license_plate=data.get('license_plate'),
            model=data.get('model'),
            vehicle_type=data.get('vehicle_type'),
            color=data.get('color'),
            image_path=data.get('image_path'),
            status=data.get('status')
        )
        return jsonify({
            'id': motorcycle.id,
            'store_id': motorcycle.store_id,
            'license_plate': motorcycle.license_plate,
            'model': motorcycle.model,
            'color': motorcycle.color,
            'vehicle_type': motorcycle.vehicle_type,
            'image_path': motorcycle.image_path,
            'status': motorcycle.status
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@api_motorcycles_bp.route('/<int:motorcycle_id>', methods=['DELETE'])
@login_required
def delete_motorcycle(motorcycle_id):
    """Delete motorcycle"""
    try:
        MotorcycleController.delete(motorcycle_id)
        return jsonify({'message': 'Motorcycle deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
