/**
 * Backend Common JavaScript
 * Handles sidebar toggle, DataTables initialization, and other common backend functionality
 */

(function() {
    'use strict';
    
    // Wait for jQuery to be available
    function waitForJQuery(callback) {
        if (typeof jQuery !== 'undefined' && typeof $ !== 'undefined') {
            callback();
        } else {
            setTimeout(function() {
                waitForJQuery(callback);
            }, 50);
        }
    }
    
    // Global function to initialize DataTables (for backward compatibility)
    window.initializeDataTable = function(tableSelector) {
        if (typeof $ === 'undefined' || typeof jQuery === 'undefined') {
            console.warn('jQuery not loaded. Cannot initialize DataTables.');
            return;
        }
        
        if (typeof $.fn.DataTable === 'undefined') {
            console.warn('DataTables library not loaded. Tables will not be initialized.');
            return;
        }
        
        var $table = $(tableSelector || '.data-table');
        $table.each(function() {
            if (!$.fn.DataTable.isDataTable(this)) {
                var $t = $(this);
                $t.find('th, td').addClass('text-start');
                var $tbody = $t.find('tbody');
                var headerCols = $t.find('thead th').length;
                
                // Remove empty data rows with colspan
                $tbody.find('tr').each(function() {
                    var $row = $(this);
                    var $tds = $row.find('td');
                    if ($tds.length === 1 && $tds.first().attr('colspan')) {
                        $row.remove();
                    }
                });
                
                if (headerCols > 0) {
                    try {
                        $t.DataTable({
                            language: {
                                url: 'https://cdn.datatables.net/plug-ins/2.3.4/i18n/zh-HANT.json',
                                emptyTable: '尚無資料'
                            },
                            pageLength: 25,
                            responsive: true,
                            order: [],
                            columnDefs: [
                                { orderable: false, targets: -1 },
                                { className: 'text-start', targets: '_all' }
                            ]
                        });
                    } catch (e) {
                        console.error('DataTables initialization error:', e);
                    }
                }
            }
        });
    };
    
    // Wait for jQuery and DOM to be ready
    waitForJQuery(function() {
        $(document).ready(function() {
        // Sidebar toggle for mobile
        $('#sidebarToggle').on('click', function(e) {
            e.stopPropagation();
            $('#sidebar').toggleClass('show');
            if ($(window).width() < 992) {
                if ($('#sidebar').hasClass('show')) {
                    $('body').append('<div class="sidebar-overlay show" id="sidebarOverlay"></div>');
                } else {
                    $('#sidebarOverlay').remove();
                }
            }
        });
        
        // Close sidebar when clicking outside on mobile
        $(document).on('click', '.sidebar-overlay', function() {
            $('#sidebar').removeClass('show');
            $(this).remove();
        });
        
        // Close sidebar when clicking outside on mobile
        $(document).on('click', function(e) {
            if ($(window).width() < 992) {
                if (!$(e.target).closest('#sidebar, #sidebarToggle').length) {
                    $('#sidebar').removeClass('show');
                    $('.sidebar-overlay').remove();
                }
            }
        });
        
        // Initialize DataTables for all tables with class 'data-table'
        // Use the global function for consistency
        if (typeof window.initializeDataTable === 'function') {
            window.initializeDataTable('.data-table');
        }
        
        // Handle window resize for sidebar
        $(window).on('resize', function() {
            if ($(window).width() >= 992) {
                $('#sidebar').removeClass('show');
                $('.sidebar-overlay').remove();
            }
        });
        });
    });
    
})();

