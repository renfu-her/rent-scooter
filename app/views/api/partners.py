from flask import Blueprint, jsonify, request
from app.controllers.partner_controller import PartnerController
from app.utils.decorators import login_required

api_partners_bp = Blueprint('api_partners', __name__)


@api_partners_bp.route('', methods=['GET'])
@login_required
def list_partners():
    """Get all partners"""
    partners = PartnerController.get_all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'address': p.address,
        'tax_id': p.tax_id,
        'created_at': p.created_at.isoformat() if p.created_at else None
    } for p in partners])


@api_partners_bp.route('/<int:partner_id>', methods=['GET'])
@login_required
def get_partner(partner_id):
    """Get partner by ID"""
    partner = PartnerController.get_by_id(partner_id)
    return jsonify({
        'id': partner.id,
        'name': partner.name,
        'address': partner.address,
        'tax_id': partner.tax_id,
        'created_at': partner.created_at.isoformat() if partner.created_at else None
    })


@api_partners_bp.route('', methods=['POST'])
@login_required
def create_partner():
    """Create new partner"""
    data = request.get_json()
    try:
        partner = PartnerController.create(
            name=data.get('name'),
            address=data.get('address'),
            tax_id=data.get('tax_id')
        )
        return jsonify({
            'id': partner.id,
            'name': partner.name,
            'address': partner.address,
            'tax_id': partner.tax_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@api_partners_bp.route('/<int:partner_id>', methods=['PUT'])
@login_required
def update_partner(partner_id):
    """Update partner"""
    data = request.get_json()
    try:
        partner = PartnerController.update(
            partner_id,
            name=data.get('name'),
            address=data.get('address'),
            tax_id=data.get('tax_id')
        )
        return jsonify({
            'id': partner.id,
            'name': partner.name,
            'address': partner.address,
            'tax_id': partner.tax_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@api_partners_bp.route('/<int:partner_id>', methods=['DELETE'])
@login_required
def delete_partner(partner_id):
    """Delete partner"""
    try:
        PartnerController.delete(partner_id)
        return jsonify({'message': 'Partner deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
