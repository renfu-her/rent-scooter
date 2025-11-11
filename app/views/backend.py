from flask import Blueprint, redirect, url_for
from flask_login import login_required

backend_bp = Blueprint('backend', __name__)


@backend_bp.route('/')
@login_required
def index():
    """Backend homepage - redirect to motorcycles"""
    return redirect(url_for('admin_motorcycles.index'))

