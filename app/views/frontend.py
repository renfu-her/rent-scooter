from flask import render_template, redirect, url_for
from app.views.frontend import frontend_bp


@frontend_bp.route('/')
def index():
    """Frontend homepage"""
    return render_template('frontend/index.html')
