from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app
from app.controllers.store_controller import StoreController
from app.controllers.partner_controller import PartnerController
from app.utils.decorators import admin_required
from app.utils.image_processor import save_uploaded_image, allowed_file, delete_image

admin_stores_bp = Blueprint('admin_stores', __name__)


@admin_stores_bp.route('')
@admin_stores_bp.route('/')
@admin_required
def index():
    """List all stores"""
    stores = StoreController.get_all()
    # Eager load partner relationship to avoid N+1 queries
    for store in stores:
        if store.partner_id:
            store.partner  # Trigger lazy load
    return render_template('admin/stores/index.html', stores=stores)


@admin_stores_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    """Create new store"""
    partners = PartnerController.get_all()
    if request.method == 'POST':
        try:
            image_path = None
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename and allowed_file(file.filename):
                    image_path = save_uploaded_image(file, 'stores')
            
            partner_id = request.form.get('partner_id')
            if partner_id == '':
                partner_id = None
            else:
                partner_id = int(partner_id) if partner_id else None
            
            StoreController.create(
                name=request.form.get('name'),
                address=request.form.get('address'),
                phone=request.form.get('phone'),
                partner_id=partner_id,
                image_path=image_path
            )
            flash('商店建立成功', 'success')
            return redirect(url_for('admin_stores.index'))
        except Exception as e:
            flash(f'建立失敗: {str(e)}', 'error')
    return render_template('admin/stores/create.html', partners=partners)


@admin_stores_bp.route('/<int:store_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(store_id):
    """Edit store"""
    store = StoreController.get_by_id(store_id)
    partners = PartnerController.get_all()
    if request.method == 'POST':
        try:
            image_path = store.image_path
            old_image_path = store.image_path  # Save old image path for deletion
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename and allowed_file(file.filename):
                    # Delete old image if exists
                    if old_image_path:
                        delete_image(old_image_path)
                    # Save new image
                    image_path = save_uploaded_image(file, 'stores')
            
            partner_id = request.form.get('partner_id')
            if partner_id == '':
                partner_id = None
            else:
                partner_id = int(partner_id) if partner_id else None
            
            StoreController.update(
                store_id,
                name=request.form.get('name'),
                address=request.form.get('address'),
                phone=request.form.get('phone'),
                partner_id=partner_id,
                image_path=image_path
            )
            flash('商店更新成功', 'success')
            return redirect(url_for('admin_stores.index'))
        except Exception as e:
            flash(f'更新失敗: {str(e)}', 'error')
    return render_template('admin/stores/edit.html', store=store, partners=partners)


@admin_stores_bp.route('/<int:store_id>/delete', methods=['POST'])
@admin_required
def delete(store_id):
    """Delete store"""
    try:
        store = StoreController.get_by_id(store_id)
        # Delete image if exists
        if store.image_path:
            delete_image(store.image_path)
        StoreController.delete(store_id)
        flash('商店刪除成功', 'success')
    except Exception as e:
        flash(f'刪除失敗: {str(e)}', 'error')
    return redirect(url_for('admin_stores.index'))


@admin_stores_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
