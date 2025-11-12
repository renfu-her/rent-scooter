from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app
from app.controllers.motorcycle_controller import MotorcycleController
from app.controllers.store_controller import StoreController
from app.utils.decorators import store_admin_required
from app.utils.image_processor import save_uploaded_image, allowed_file, delete_image

admin_motorcycles_bp = Blueprint('admin_motorcycles', __name__)


@admin_motorcycles_bp.route('')
@admin_motorcycles_bp.route('/')
@store_admin_required
def index():
    """List all motorcycles"""
    motorcycles = MotorcycleController.get_all()
    return render_template('admin/motorcycles/index.html', motorcycles=motorcycles)


@admin_motorcycles_bp.route('/create', methods=['GET', 'POST'])
@store_admin_required
def create():
    """Create new motorcycle"""
    stores = StoreController.get_all()
    if request.method == 'POST':
        try:
            image_path = None
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename and allowed_file(file.filename):
                    image_path = save_uploaded_image(file, 'motorcycles')
            
            MotorcycleController.create(
                store_id=int(request.form.get('store_id')),
                license_plate=request.form.get('license_plate'),
                model=request.form.get('model'),
                vehicle_type=request.form.get('vehicle_type'),
                color=request.form.get('color') or None,
                image_path=image_path
            )
            flash('機車建立成功', 'success')
            return redirect(url_for('admin_motorcycles.index'))
        except Exception as e:
            flash(f'建立失敗: {str(e)}', 'error')
    return render_template('admin/motorcycles/create.html', stores=stores)


@admin_motorcycles_bp.route('/<int:motorcycle_id>/edit', methods=['GET', 'POST'])
@store_admin_required
def edit(motorcycle_id):
    """Edit motorcycle"""
    motorcycle = MotorcycleController.get_by_id(motorcycle_id)
    stores = StoreController.get_all()
    if request.method == 'POST':
        try:
            image_path = motorcycle.image_path
            old_image_path = motorcycle.image_path  # Save old image path for deletion
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename and allowed_file(file.filename):
                    # Delete old image if exists
                    if old_image_path:
                        delete_image(old_image_path)
                    # Save new image
                    image_path = save_uploaded_image(file, 'motorcycles')
            
            MotorcycleController.update(
                motorcycle_id,
                store_id=int(request.form.get('store_id')) if request.form.get('store_id') else None,
                license_plate=request.form.get('license_plate'),
                model=request.form.get('model'),
                vehicle_type=request.form.get('vehicle_type'),
                color=request.form.get('color') or None,
                image_path=image_path,
                status=request.form.get('status')
            )
            flash('機車更新成功', 'success')
            return redirect(url_for('admin_motorcycles.index'))
        except Exception as e:
            flash(f'更新失敗: {str(e)}', 'error')
    return render_template('admin/motorcycles/edit.html', motorcycle=motorcycle, stores=stores)


@admin_motorcycles_bp.route('/<int:motorcycle_id>/delete', methods=['POST'])
@store_admin_required
def delete(motorcycle_id):
    """Delete motorcycle"""
    try:
        MotorcycleController.delete(motorcycle_id)
        flash('機車刪除成功', 'success')
    except Exception as e:
        flash(f'刪除失敗: {str(e)}', 'error')
    return redirect(url_for('admin_motorcycles.index'))


@admin_motorcycles_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
