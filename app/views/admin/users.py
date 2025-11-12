from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.controllers.user_controller import UserController
from app.controllers.store_controller import StoreController
from app.utils.decorators import admin_required

admin_users_bp = Blueprint('admin_users', __name__)


@admin_users_bp.route('')
@admin_users_bp.route('/')
@admin_required
def index():
    """List all users"""
    search = request.args.get('search', '')
    role_filter = request.args.get('role', 'all')
    status_filter = request.args.get('status', 'all')
    
    users = UserController.get_all(
        search=search if search else None,
        role_filter=role_filter if role_filter != 'all' else None,
        status_filter=status_filter if status_filter != 'all' else None
    )
    
    return render_template('admin/users/index.html', 
                         users=users,
                         search=search,
                         role_filter=role_filter,
                         status_filter=status_filter)


@admin_users_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    """Create new user"""
    stores = StoreController.get_all()
    
    if request.method == 'POST':
        try:
            UserController.create(
                username=request.form.get('username'),
                email=request.form.get('email'),
                password=request.form.get('password'),
                user_type=request.form.get('user_type', 'customer'),
                store_id=int(request.form.get('store_id')) if request.form.get('store_id') else None,
                is_active=request.form.get('is_active') == 'on'
            )
            flash('使用者建立成功', 'success')
            return redirect(url_for('admin_users.index'))
        except ValueError as e:
            flash(f'建立失敗: {str(e)}', 'error')
        except Exception as e:
            flash(f'建立失敗: {str(e)}', 'error')
    
    return render_template('admin/users/create.html', stores=stores)


@admin_users_bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(user_id):
    """Edit user"""
    user = UserController.get_by_id(user_id)
    stores = StoreController.get_all()
    
    if request.method == 'POST':
        try:
            UserController.update(
                user_id,
                username=request.form.get('username'),
                email=request.form.get('email'),
                password=request.form.get('password') if request.form.get('password') else None,
                user_type=request.form.get('user_type'),
                store_id=int(request.form.get('store_id')) if request.form.get('store_id') else None,
                is_active=request.form.get('is_active') == 'on'
            )
            flash('使用者更新成功', 'success')
            return redirect(url_for('admin_users.index'))
        except ValueError as e:
            flash(f'更新失敗: {str(e)}', 'error')
        except Exception as e:
            flash(f'更新失敗: {str(e)}', 'error')
    
    return render_template('admin/users/edit.html', user=user, stores=stores)


@admin_users_bp.route('/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete(user_id):
    """Delete user"""
    try:
        UserController.delete(user_id)
        flash('使用者刪除成功', 'success')
    except Exception as e:
        flash(f'刪除失敗: {str(e)}', 'error')
    return redirect(url_for('admin_users.index'))

