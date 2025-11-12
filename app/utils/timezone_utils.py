"""Timezone utilities for Asia/Taipei"""
from datetime import datetime
import pytz


def get_taipei_time():
    """Get current time in Asia/Taipei timezone"""
    taipei_tz = pytz.timezone('Asia/Taipei')
    return datetime.now(taipei_tz)


def get_today_end():
    """Get today 23:59:59 in Asia/Taipei timezone"""
    taipei_tz = pytz.timezone('Asia/Taipei')
    now = datetime.now(taipei_tz)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=0)
    return today_end


def to_taipei_timezone(dt):
    """Convert datetime to Asia/Taipei timezone"""
    if dt is None:
        return None
    taipei_tz = pytz.timezone('Asia/Taipei')
    if dt.tzinfo is None:
        # Assume UTC if no timezone info
        dt = pytz.utc.localize(dt)
    return dt.astimezone(taipei_tz)


def check_expired_reservations():
    """Check and update expired reservations"""
    from app.models.motorcycle import Motorcycle
    from app.models import db
    from app.utils.websocket_events import emit_motorcycle_status_change
    
    taipei_tz = pytz.timezone('Asia/Taipei')
    now = datetime.now(taipei_tz)
    
    # Find motorcycles with expired reservations
    expired_motorcycles = Motorcycle.query.filter(
        Motorcycle.status == '預訂',
        Motorcycle.reservation_expires_at.isnot(None),
        Motorcycle.reservation_expires_at < now
    ).all()
    
    status_changes = []
    for motorcycle in expired_motorcycles:
        old_status = motorcycle.status
        motorcycle.status = '待出租'
        motorcycle.reservation_expires_at = None
        status_changes.append((motorcycle.license_plate, old_status, '待出租'))
    
    if status_changes:
        db.session.commit()
        # Emit WebSocket notifications
        for license_plate, old_status, new_status in status_changes:
            emit_motorcycle_status_change(license_plate, old_status, new_status)
    
    return len(status_changes)

