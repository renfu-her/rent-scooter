from app.models import db
from app.models.motorcycle import Motorcycle
from flask_login import current_user


class MotorcycleController:
    @staticmethod
    def get_all(store_id=None):
        """Get all motorcycles, optionally filtered by store"""
        query = Motorcycle.query
        # Store admin can only see their store's motorcycles
        if current_user.is_store_admin() and current_user.store_id:
            query = query.filter_by(store_id=current_user.store_id)
        elif store_id:
            query = query.filter_by(store_id=store_id)
        return query.all()
    
    @staticmethod
    def get_available(store_id=None):
        """Get available motorcycles (status = 待出租)"""
        query = Motorcycle.query.filter_by(status='待出租')
        if current_user.is_store_admin() and current_user.store_id:
            query = query.filter_by(store_id=current_user.store_id)
        elif store_id:
            query = query.filter_by(store_id=store_id)
        return query.all()
    
    @staticmethod
    def search_by_license_plate(license_plate, exclude_rented=True):
        """Search motorcycles by license plate"""
        query = Motorcycle.query.filter(
            Motorcycle.license_plate.like(f'%{license_plate}%')
        )
        if exclude_rented:
            query = query.filter(Motorcycle.status != '出租中')
        # Store admin filter
        if current_user.is_store_admin() and current_user.store_id:
            query = query.filter_by(store_id=current_user.store_id)
        return query.limit(20).all()
    
    @staticmethod
    def get_by_id(motorcycle_id):
        """Get motorcycle by ID"""
        motorcycle = Motorcycle.query.get_or_404(motorcycle_id)
        # Check permission for store admin
        if current_user.is_store_admin() and motorcycle.store_id != current_user.store_id:
            from flask import abort
            abort(403)
        return motorcycle
    
    @staticmethod
    def create(store_id, license_plate, model, vehicle_type, color=None, image_path=None):
        """Create a new motorcycle"""
        # Check permission for store admin
        if current_user.is_store_admin() and store_id != current_user.store_id:
            from flask import abort
            abort(403)
        
        motorcycle = Motorcycle(
            store_id=store_id,
            license_plate=license_plate,
            model=model,
            vehicle_type=vehicle_type,
            color=color,
            image_path=image_path,
            status='待出租'
        )
        db.session.add(motorcycle)
        db.session.commit()
        return motorcycle
    
    @staticmethod
    def update(motorcycle_id, store_id=None, license_plate=None, model=None, 
               vehicle_type=None, color=None, image_path=None, status=None):
        """Update motorcycle"""
        motorcycle = MotorcycleController.get_by_id(motorcycle_id)
        
        # Track old status for WebSocket notification
        old_status = motorcycle.status
        
        if store_id is not None:
            if current_user.is_store_admin() and store_id != current_user.store_id:
                from flask import abort
                abort(403)
            motorcycle.store_id = store_id
        if license_plate:
            motorcycle.license_plate = license_plate
        if model:
            motorcycle.model = model
        if vehicle_type:
            motorcycle.vehicle_type = vehicle_type
        if color is not None:
            motorcycle.color = color
        if image_path is not None:
            motorcycle.image_path = image_path
        if status:
            motorcycle.status = status
        
        db.session.commit()
        
        # Emit WebSocket notification if status changed
        if status and status != old_status:
            from app.utils.websocket_events import emit_motorcycle_status_change
            emit_motorcycle_status_change(motorcycle.license_plate, old_status, status)
        
        return motorcycle
    
    @staticmethod
    def delete(motorcycle_id):
        """Delete motorcycle"""
        motorcycle = MotorcycleController.get_by_id(motorcycle_id)
        db.session.delete(motorcycle)
        db.session.commit()
    
    @staticmethod
    def reserve(motorcycle_id, renter_name, renter_id_number, has_license, reservation_status='預訂', contact_phone=None, remarks=None):
        """Reserve a motorcycle with customer information"""
        from app.utils.timezone_utils import get_today_end
        from app.models.reservation import Reservation
        
        motorcycle = Motorcycle.query.get_or_404(motorcycle_id)
        
        # Track old status for WebSocket notification
        old_status = motorcycle.status
        
        # Only allow reservation if status is '待出租'
        if motorcycle.status != '待出租':
            raise ValueError(f'機車狀態為 {motorcycle.status}，無法預訂')
        
        # Validate license requirement based on vehicle type
        if not has_license:
            if motorcycle.vehicle_type in ('白牌', '綠牌'):
                raise ValueError(f'此車款類型（{motorcycle.vehicle_type}）需要駕照，無法預訂')
            elif motorcycle.vehicle_type != '電輔車':
                raise ValueError(f'此車款類型（{motorcycle.vehicle_type}）需要駕照，無法預訂')
        
        # Create reservation record
        reservation = Reservation(
            motorcycle_id=motorcycle_id,
            renter_name=renter_name,
            renter_id_number=renter_id_number,
            has_license=has_license,
            reservation_status=reservation_status,
            reservation_expires_at=get_today_end(),
            contact_phone=contact_phone,
            remarks=remarks
        )
        db.session.add(reservation)
        
        # Update motorcycle status
        motorcycle.status = reservation_status
        motorcycle.reservation_expires_at = get_today_end()
        
        db.session.commit()
        
        # Emit WebSocket notification
        if old_status != reservation_status:
            from app.utils.websocket_events import emit_motorcycle_status_change
            emit_motorcycle_status_change(motorcycle.license_plate, old_status, reservation_status)
        
        return motorcycle
    
    @staticmethod
    def get_by_id_public(motorcycle_id):
        """Get motorcycle by ID for public access (no permission check)"""
        return Motorcycle.query.get_or_404(motorcycle_id)

