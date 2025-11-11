from flask import Blueprint, jsonify, request
from app.controllers.banner_controller import BannerController
from app.utils.decorators import login_required

api_banners_bp = Blueprint('api_banners', __name__)


@api_banners_bp.route('', methods=['GET'])
def list_banners():
    """Get all banners (public endpoint)"""
    active_only = request.args.get('active_only', 'false').lower() == 'true'
    
    if active_only:
        banners = BannerController.get_active()
    else:
        banners = BannerController.get_all()
    
    return jsonify([{
        'id': b.id,
        'title': b.title,
        'image_path': b.image_path,
        'link_url': b.link_url,
        'display_order': b.display_order,
        'is_active': b.is_active
    } for b in banners])


@api_banners_bp.route('/<int:banner_id>', methods=['GET'])
def get_banner(banner_id):
    """Get banner by ID"""
    banner = BannerController.get_by_id(banner_id)
    return jsonify({
        'id': banner.id,
        'title': banner.title,
        'image_path': banner.image_path,
        'link_url': banner.link_url,
        'display_order': banner.display_order,
        'is_active': banner.is_active
    })


@api_banners_bp.route('', methods=['POST'])
@login_required
def create_banner():
    """Create new banner"""
    data = request.get_json()
    try:
        banner = BannerController.create(
            title=data.get('title'),
            image_path=data.get('image_path'),
            link_url=data.get('link_url'),
            display_order=data.get('display_order', 0),
            is_active=data.get('is_active', True)
        )
        return jsonify({
            'id': banner.id,
            'title': banner.title,
            'image_path': banner.image_path,
            'link_url': banner.link_url,
            'display_order': banner.display_order,
            'is_active': banner.is_active
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@api_banners_bp.route('/<int:banner_id>', methods=['PUT'])
@login_required
def update_banner(banner_id):
    """Update banner"""
    data = request.get_json()
    try:
        banner = BannerController.update(
            banner_id,
            title=data.get('title'),
            image_path=data.get('image_path'),
            link_url=data.get('link_url'),
            display_order=data.get('display_order'),
            is_active=data.get('is_active')
        )
        return jsonify({
            'id': banner.id,
            'title': banner.title,
            'image_path': banner.image_path,
            'link_url': banner.link_url,
            'display_order': banner.display_order,
            'is_active': banner.is_active
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@api_banners_bp.route('/<int:banner_id>', methods=['DELETE'])
@login_required
def delete_banner(banner_id):
    """Delete banner"""
    try:
        BannerController.delete(banner_id)
        return jsonify({'message': 'Banner deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
