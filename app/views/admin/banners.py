from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app
from app.controllers.banner_controller import BannerController
from app.utils.decorators import admin_required
from app.utils.image_processor import save_uploaded_image, allowed_file, delete_image

admin_banners_bp = Blueprint('admin_banners', __name__)


@admin_banners_bp.route('')
@admin_banners_bp.route('/')
@admin_required
def index():
    """List all banners"""
    banners = BannerController.get_all()
    return render_template('admin/banners/index.html', banners=banners)


@admin_banners_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    """Create new banner"""
    if request.method == 'POST':
        try:
            if 'image' not in request.files or not request.files['image'].filename:
                flash('請選擇圖片', 'error')
                return render_template('admin/banners/create.html')
            
            file = request.files['image']
            if not allowed_file(file.filename):
                flash('不支援的圖片格式', 'error')
                return render_template('admin/banners/create.html')
            
            image_path = save_uploaded_image(file, 'banners')
            
            BannerController.create(
                banner_name=request.form.get('banner_name') or None,
                title=request.form.get('title'),
                subtitle=request.form.get('subtitle') or None,
                image_path=image_path,
                link_url=request.form.get('link_url') or None,
                display_order=int(request.form.get('display_order', 0)),
                is_active=request.form.get('is_active') == 'on'
            )
            flash('Banner建立成功', 'success')
            return redirect(url_for('admin_banners.index'))
        except Exception as e:
            flash(f'建立失敗: {str(e)}', 'error')
    return render_template('admin/banners/create.html')


@admin_banners_bp.route('/<int:banner_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(banner_id):
    """Edit banner"""
    banner = BannerController.get_by_id(banner_id)
    if request.method == 'POST':
        try:
            image_path = banner.image_path
            old_image_path = banner.image_path  # Save old image path for deletion
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename and allowed_file(file.filename):
                    # Delete old image if exists
                    if old_image_path:
                        delete_image(old_image_path)
                    # Save new image
                    image_path = save_uploaded_image(file, 'banners')
            
            BannerController.update(
                banner_id,
                banner_name=request.form.get('banner_name') or None,
                title=request.form.get('title'),
                subtitle=request.form.get('subtitle') or None,
                image_path=image_path,
                link_url=request.form.get('link_url') or None,
                display_order=int(request.form.get('display_order', 0)),
                is_active=request.form.get('is_active') == 'on'
            )
            flash('Banner更新成功', 'success')
            return redirect(url_for('admin_banners.index'))
        except Exception as e:
            flash(f'更新失敗: {str(e)}', 'error')
    return render_template('admin/banners/edit.html', banner=banner)


@admin_banners_bp.route('/<int:banner_id>/toggle-status', methods=['POST'])
@admin_required
def toggle_status(banner_id):
    """Toggle banner status"""
    try:
        banner = BannerController.get_by_id(banner_id)
        BannerController.update(banner_id, is_active=not banner.is_active)
        status_text = '啟用' if not banner.is_active else '停用'
        flash(f'Banner已{status_text}', 'success')
    except Exception as e:
        flash(f'操作失敗: {str(e)}', 'error')
    return redirect(url_for('admin_banners.index'))


@admin_banners_bp.route('/<int:banner_id>/delete', methods=['POST'])
@admin_required
def delete(banner_id):
    """Delete banner"""
    try:
        BannerController.delete(banner_id)
        flash('Banner刪除成功', 'success')
    except Exception as e:
        flash(f'刪除失敗: {str(e)}', 'error')
    return redirect(url_for('admin_banners.index'))


@admin_banners_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
