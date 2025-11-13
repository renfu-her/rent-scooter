/**
 * Socket.IO Client for Backend
 * Handles WebSocket connections and real-time notifications
 */

(function() {
    'use strict';
    
    // Check if Socket.IO is loaded
    if (typeof io === 'undefined') {
        console.error('Socket.IO library not loaded. Please include socket.io.min.js first.');
        return;
    }
    
    // Initialize Socket.IO connection with reconnection settings
    const socket = io({
        reconnection: true,
        reconnectionDelay: 1000,
        reconnectionDelayMax: 5000,
        reconnectionAttempts: Infinity,
        timeout: 20000
    });
    
    // Connection status tracking
    let isConnected = false;
    let reconnectAttempts = 0;
    
    // Toast container for notifications
    function ensureToastContainer() {
        if ($('#toast-container').length === 0) {
            $('body').append('<div id="toast-container" class="toast-container position-fixed top-0 end-0 p-3" style="z-index: 9999;"></div>');
        }
    }
    
    // Function to show toast notification
    function showToast(message, type = 'info') {
        ensureToastContainer();
        
        const toastId = 'toast-' + Date.now();
        const bgClass = type === 'rented' ? 'bg-success' : 
                       type === 'returned' ? 'bg-info' : 
                       type === 'maintenance' ? 'bg-warning' : 
                       type === 'error' ? 'bg-danger' : 'bg-primary';
        const icon = type === 'rented' ? 'bi-check-circle' : 
                    type === 'returned' ? 'bi-arrow-counterclockwise' : 
                    type === 'maintenance' ? 'bi-tools' : 
                    type === 'error' ? 'bi-exclamation-triangle' : 'bi-info-circle';
        
        const toastHtml = `
            <div id="${toastId}" class="toast ${bgClass} text-white" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="5000">
                <div class="toast-header ${bgClass} text-white border-0">
                    <i class="bi ${icon} me-2"></i>
                    <strong class="me-auto">機車狀態通知</strong>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <div class="toast-body">
                    ${message}
                </div>
            </div>
        `;
        
        $('#toast-container').append(toastHtml);
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
        
        // Remove toast element after it's hidden
        toastElement.addEventListener('hidden.bs.toast', function() {
            $(toastElement).remove();
        });
    }
    
    // Socket.IO connection event handlers
    socket.on('connect', function() {
        isConnected = true;
        reconnectAttempts = 0;
        console.log('WebSocket connected');
        // Optionally show connection status (commented out to avoid spam)
        // showToast('即時通知已連接', 'info');
    });
    
    socket.on('disconnect', function(reason) {
        isConnected = false;
        console.log('WebSocket disconnected:', reason);
        if (reason === 'io server disconnect') {
            // Server disconnected, need to manually reconnect
            socket.connect();
        }
    });
    
    socket.on('reconnect', function(attemptNumber) {
        isConnected = true;
        reconnectAttempts = attemptNumber;
        console.log('WebSocket reconnected after', attemptNumber, 'attempts');
        showToast('即時通知已重新連接', 'info');
    });
    
    socket.on('reconnect_attempt', function(attemptNumber) {
        reconnectAttempts = attemptNumber;
        console.log('WebSocket reconnection attempt', attemptNumber);
    });
    
    socket.on('reconnect_error', function(error) {
        console.error('WebSocket reconnection error:', error);
    });
    
    socket.on('reconnect_failed', function() {
        console.error('WebSocket reconnection failed');
        showToast('即時通知連接失敗，請刷新頁面', 'error');
    });
    
    // Listen for motorcycle status changes
    socket.on('motorcycle_status_change', function(data) {
        if (isConnected) {
            showToast(data.message, data.type);
        }
    });
    
    // Export socket instance for use in other scripts
    window.backendSocket = socket;
    window.showToast = showToast;
    
})();

