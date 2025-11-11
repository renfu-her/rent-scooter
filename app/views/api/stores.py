from flask import jsonify, request
from app.views.api.stores import api_stores_bp
from app.controllers.store_controller import StoreController
from app.utils.decorators import login_required


@api_stores_bp.route('', methods=['GET'])
@login_required
def list_stores():
    """Get all stores"""
    stores = StoreController.get_all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'address': s.address,
        'phone': s.phone,
        'created_at': s.created_at.isoformat() if s.created_at else None
    } for s in stores])


@api_stores_bp.route('/<int:store_id>', methods=['GET'])
@login_required
def get_store(store_id):
    """Get store by ID"""
    store = StoreController.get_by_id(store_id)
    return jsonify({
        'id': store.id,
        'name': store.name,
        'address': store.address,
        'phone': store.phone,
        'created_at': store.created_at.isoformat() if store.created_at else None
    })


@api_stores_bp.route('', methods=['POST'])
@login_required
def create_store():
    """Create new store"""
    data = request.get_json()
    try:
        store = StoreController.create(
            name=data.get('name'),
            address=data.get('address'),
            phone=data.get('phone')
        )
        return jsonify({
            'id': store.id,
            'name': store.name,
            'address': store.address,
            'phone': store.phone
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@api_stores_bp.route('/<int:store_id>', methods=['PUT'])
@login_required
def update_store(store_id):
    """Update store"""
    data = request.get_json()
    try:
        store = StoreController.update(
            store_id,
            name=data.get('name'),
            address=data.get('address'),
            phone=data.get('phone')
        )
        return jsonify({
            'id': store.id,
            'name': store.name,
            'address': store.address,
            'phone': store.phone
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@api_stores_bp.route('/<int:store_id>', methods=['DELETE'])
@login_required
def delete_store(store_id):
    """Delete store"""
    try:
        StoreController.delete(store_id)
        return jsonify({'message': 'Store deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
