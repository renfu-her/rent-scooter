"""WebSocket event handlers for real-time notifications"""


def register_websocket_events(socketio):
    """Register all WebSocket event handlers"""
    
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection"""
        print('Client connected')
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        print('Client disconnected')


def emit_motorcycle_status_change(license_plate, old_status, new_status):
    """Emit motorcycle status change notification"""
    try:
        from app import socketio
        
        # Determine action message
        if new_status == '出租中':
            message = f'車牌 {license_plate} 已經出租'
            message_type = 'rented'
        elif new_status == '待出租':
            message = f'車牌 {license_plate} 已經歸還'
            message_type = 'returned'
        elif new_status == '維修中':
            message = f'車牌 {license_plate} 已送修'
            message_type = 'maintenance'
        else:
            message = f'車牌 {license_plate} 狀態已變更為 {new_status}'
            message_type = 'updated'
        
        # Emit to all connected clients
        socketio.emit('motorcycle_status_change', {
            'license_plate': license_plate,
            'old_status': old_status,
            'new_status': new_status,
            'message': message,
            'type': message_type
        }, broadcast=True)
    except Exception as e:
        # Log error but don't break the application
        import logging
        logging.error(f"Failed to emit WebSocket notification: {str(e)}")

