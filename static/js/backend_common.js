/**
 * Backend Common JavaScript
 * Handles sidebar toggle, DataTables initialization, and other common backend functionality
 */

(function() {
    'use strict';
    
    // Wait for jQuery and DOM to be ready
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
        if (typeof $.fn.DataTable !== 'undefined') {
            $('.data-table').each(function() {
                if (!$.fn.DataTable.isDataTable(this)) {
                    var $table = $(this);
                    // Ensure all columns are left-aligned
                    $table.find('th, td').addClass('text-start');
                    var $tbody = $table.find('tbody');
                    var headerCols = $table.find('thead th').length;
                    
                    // 移除所有帶有 colspan 的空數據行（這些行會導致列數不匹配）
                    $tbody.find('tr').each(function() {
                        var $row = $(this);
                        var $tds = $row.find('td');
                        // 如果這行只有一個 td 且有 colspan，說明是空數據提示行，移除它
                        if ($tds.length === 1 && $tds.first().attr('colspan')) {
                            $row.remove();
                        }
                    });
                    
                    if (headerCols > 0) {
                        try {
                            $table.DataTable({
                                language: {
                                    url: 'https://cdn.datatables.net/plug-ins/2.3.4/i18n/zh-HANT.json',
                                    emptyTable: '尚無資料'
                                },
                                pageLength: 25,
                                responsive: true,
                                order: [],
                                columnDefs: [
                                    { orderable: false, targets: -1 }, // 最後一列（操作列）不可排序
                                    { className: 'text-start', targets: '_all' } // 所有列左對齊
                                ]
                            });
                        } catch (e) {
                            console.error('DataTables initialization error:', e);
                        }
                    }
                }
            });
        } else {
            console.warn('DataTables library not loaded. Tables will not be initialized.');
        }
        
        // Handle window resize for sidebar
        $(window).on('resize', function() {
            if ($(window).width() >= 992) {
                $('#sidebar').removeClass('show');
                $('.sidebar-overlay').remove();
            }
        });
    });
    
})();

