from datetime import datetime
import uuid
from app.models import db
from app.models.order import Order, OrderMotorcycle
from app.models.motorcycle import Motorcycle


class OrderController:
    @staticmethod
    def generate_order_number():
        """Generate unique order number"""
        return f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
    
    @staticmethod
    def get_all():
        """Get all orders"""
        return Order.query.order_by(Order.created_at.desc()).all()
    
    @staticmethod
    def get_by_id(order_id):
        """Get order by ID"""
        return Order.query.get_or_404(order_id)
    
    @staticmethod
    def create(partner_id=None, renter_id=None, renter_name=None, renter_id_number=None, 
               has_license=None, rental_plan_id=None,
               total_amount=0, status='待處理', reservation_date=None,
               rental_start_time=None, rental_end_time=None,
               shipping_company=None, ferry_departure_time=None,
               ferry_return_time=None, contact_phone=None,
               payment_method=None, estimated_return_time=None,
               remarks=None, motorcycle_ids=None):
        """Create a new order"""
        if not reservation_date:
            reservation_date = datetime.now().date()
        
        order = Order(
            order_number=OrderController.generate_order_number(),
            partner_id=partner_id,
            renter_id=renter_id,
            renter_name=renter_name,
            renter_id_number=renter_id_number,
            has_license=has_license,
            rental_plan_id=rental_plan_id,
            total_amount=total_amount,
            status=status,
            reservation_date=reservation_date,
            rental_start_time=rental_start_time,
            rental_end_time=rental_end_time,
            shipping_company=shipping_company,
            ferry_departure_time=ferry_departure_time,
            ferry_return_time=ferry_return_time,
            contact_phone=contact_phone,
            payment_method=payment_method,
            estimated_return_time=estimated_return_time,
            remarks=remarks
        )
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Add motorcycles
        status_changes = []  # Track status changes to emit after commit
        if motorcycle_ids:
            for motorcycle_id in motorcycle_ids:
                order_motorcycle = OrderMotorcycle(
                    order_id=order.id,
                    motorcycle_id=motorcycle_id
                )
                db.session.add(order_motorcycle)
                # Update motorcycle status
                motorcycle = Motorcycle.query.get(motorcycle_id)
                if motorcycle:
                    old_status = motorcycle.status
                    motorcycle.status = '出租中'
                    # Store status change to emit after commit
                    if old_status != '出租中':
                        status_changes.append((motorcycle.license_plate, old_status, '出租中'))
        
        db.session.commit()
        
        # Emit WebSocket notifications after successful commit
        if status_changes:
            from app.utils.websocket_events import emit_motorcycle_status_change
            for license_plate, old_status, new_status in status_changes:
                emit_motorcycle_status_change(license_plate, old_status, new_status)
        
        return order
    
    @staticmethod
    def update(order_id, **kwargs):
        """Update order"""
        order = Order.query.get_or_404(order_id)
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(order, key) and value is not None:
                setattr(order, key, value)
        
        # Handle motorcycle updates
        status_changes = []  # Track status changes to emit after commit
        if 'motorcycle_ids' in kwargs and kwargs['motorcycle_ids'] is not None:
            # Remove old associations
            OrderMotorcycle.query.filter_by(order_id=order.id).delete()
            # Add new associations
            for motorcycle_id in kwargs['motorcycle_ids']:
                order_motorcycle = OrderMotorcycle(
                    order_id=order.id,
                    motorcycle_id=motorcycle_id
                )
                db.session.add(order_motorcycle)
                # Update motorcycle status
                motorcycle = Motorcycle.query.get(motorcycle_id)
                if motorcycle:
                    old_status = motorcycle.status
                    motorcycle.status = '出租中'
                    # Store status change to emit after commit
                    if old_status != '出租中':
                        status_changes.append((motorcycle.license_plate, old_status, '出租中'))
        
        # Auto-update motorcycle status based on order status
        if 'status' in kwargs:
            if kwargs['status'] in ('已完成', '已取消'):
                # Set motorcycles back to available
                for om in order.motorcycles:
                    motorcycle = Motorcycle.query.get(om.motorcycle_id)
                    if motorcycle:
                        old_status = motorcycle.status
                        motorcycle.status = '待出租'
                        # Store status change to emit after commit
                        if old_status != '待出租':
                            status_changes.append((motorcycle.license_plate, old_status, '待出租'))
            elif kwargs['status'] == '進行中':
                # Set motorcycles to rented
                for om in order.motorcycles:
                    motorcycle = Motorcycle.query.get(om.motorcycle_id)
                    if motorcycle:
                        old_status = motorcycle.status
                        motorcycle.status = '出租中'
                        # Store status change to emit after commit
                        if old_status != '出租中':
                            status_changes.append((motorcycle.license_plate, old_status, '出租中'))
        
        db.session.commit()
        
        # Emit WebSocket notifications after successful commit
        if status_changes:
            from app.utils.websocket_events import emit_motorcycle_status_change
            for license_plate, old_status, new_status in status_changes:
                emit_motorcycle_status_change(license_plate, old_status, new_status)
        
        return order
    
    @staticmethod
    def delete(order_id):
        """Delete order"""
        order = Order.query.get_or_404(order_id)
        # Set motorcycles back to available
        for om in order.motorcycles:
            motorcycle = Motorcycle.query.get(om.motorcycle_id)
            if motorcycle:
                motorcycle.status = '待出租'
        db.session.delete(order)
        db.session.commit()
    
    @staticmethod
    def get_motorcycle_counts_by_model(order_id):
        """Get motorcycle counts grouped by model for an order"""
        order = Order.query.get_or_404(order_id)
        counts = {}
        total = 0
        
        for om in order.motorcycles:
            motorcycle = Motorcycle.query.get(om.motorcycle_id)
            if motorcycle:
                model = motorcycle.model
                counts[model] = counts.get(model, 0) + 1
                total += 1
        
        return counts, total

