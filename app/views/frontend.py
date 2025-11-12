from flask import Blueprint, render_template, redirect, url_for
from app.controllers.store_controller import StoreController
from app.models.motorcycle import Motorcycle

frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/')
def index():
    """Frontend homepage"""
    stores = StoreController.get_all()
    return render_template('frontend/index.html', stores=stores)


@frontend_bp.route('/stores/<int:store_id>')
def store_detail(store_id):
    """Store detail page"""
    store = StoreController.get_by_id(store_id)
    # Get motorcycles directly from model for frontend (no permission check needed)
    motorcycles = Motorcycle.query.filter_by(store_id=store_id).all()
    return render_template('frontend/store_detail.html', store=store, motorcycles=motorcycles)
