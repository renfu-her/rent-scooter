from flask import render_template, request, redirect, url_for, flash
from app.views.admin.stores import admin_stores_bp
from app.controllers.store_controller import StoreController
from app.utils.decorators import admin_required


@admin_stores_bp.route('')
@admin_stores_bp.route('/')
@admin_required
def index():
    """List all stores"""
    stores = StoreController.get_all()
    return render_template('admin/stores/index.html', stores=stores)


@admin_stores_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    """Create new store"""
    if request.method == 'POST':
        try:
            StoreController.create(
                name=request.form.get('name'),
                address=request.form.get('address'),
                phone=request.form.get('phone')
            )
            flash('商店建立成功', 'success')
            return redirect(url_for('admin_stores.index'))
        except Exception as e:
            flash(f'建立失敗: {str(e)}', 'error')
    return render_template('admin/stores/create.html')


@admin_stores_bp.route('/<int:store_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(store_id):
    """Edit store"""
    store = StoreController.get_by_id(store_id)
    if request.method == 'POST':
        try:
            StoreController.update(
                store_id,
                name=request.form.get('name'),
                address=request.form.get('address'),
                phone=request.form.get('phone')
            )
            flash('商店更新成功', 'success')
            return redirect(url_for('admin_stores.index'))
        except Exception as e:
            flash(f'更新失敗: {str(e)}', 'error')
    return render_template('admin/stores/edit.html', store=store)


@admin_stores_bp.route('/<int:store_id>/delete', methods=['POST'])
@admin_required
def delete(store_id):
    """Delete store"""
    try:
        StoreController.delete(store_id)
        flash('商店刪除成功', 'success')
    except Exception as e:
        flash(f'刪除失敗: {str(e)}', 'error')
    return redirect(url_for('admin_stores.index'))
