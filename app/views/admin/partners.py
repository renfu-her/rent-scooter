from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.controllers.partner_controller import PartnerController
from app.utils.decorators import admin_required

admin_partners_bp = Blueprint('admin_partners', __name__)


@admin_partners_bp.route('')
@admin_partners_bp.route('/')
@admin_required
def index():
    """List all partners"""
    partners = PartnerController.get_all()
    return render_template('admin/partners/index.html', partners=partners)


@admin_partners_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    """Create new partner"""
    if request.method == 'POST':
        try:
            PartnerController.create(
                name=request.form.get('name'),
                address=request.form.get('address'),
                tax_id=request.form.get('tax_id')
            )
            flash('合作商建立成功', 'success')
            return redirect(url_for('admin_partners.index'))
        except Exception as e:
            flash(f'建立失敗: {str(e)}', 'error')
    return render_template('admin/partners/create.html')


@admin_partners_bp.route('/<int:partner_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(partner_id):
    """Edit partner"""
    partner = PartnerController.get_by_id(partner_id)
    if request.method == 'POST':
        try:
            PartnerController.update(
                partner_id,
                name=request.form.get('name'),
                address=request.form.get('address'),
                tax_id=request.form.get('tax_id')
            )
            flash('合作商更新成功', 'success')
            return redirect(url_for('admin_partners.index'))
        except Exception as e:
            flash(f'更新失敗: {str(e)}', 'error')
    return render_template('admin/partners/edit.html', partner=partner)


@admin_partners_bp.route('/<int:partner_id>/delete', methods=['POST'])
@admin_required
def delete(partner_id):
    """Delete partner"""
    try:
        PartnerController.delete(partner_id)
        flash('合作商刪除成功', 'success')
    except Exception as e:
        flash(f'刪除失敗: {str(e)}', 'error')
    return redirect(url_for('admin_partners.index'))
