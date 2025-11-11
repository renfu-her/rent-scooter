from flask import Blueprint, render_template, redirect, url_for

frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/')
def index():
    """Frontend homepage"""
    return render_template('frontend/index.html')
