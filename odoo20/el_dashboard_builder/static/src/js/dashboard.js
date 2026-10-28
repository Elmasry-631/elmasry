/* Dashboard Builder - standalone frontend for Odoo 20.
 * Plain ES module-free script: loaded in the dedicated dashboard asset bundle.
 */
(function () {
    'use strict';

    var PALETTE = [
        '#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6',
        '#1abc9c', '#e67e22', '#34495e', '#16a085', '#c0392b',
    ];

    function csrfToken() {
        return (window.odoo && window.odoo.csrf_token) || '';
    }

    async function jsonRpc(url, params) {
        var payload = Object.assign(
            { jsonrpc: '2.0', method: 'call', params: Object.assign({}, params || {}) },
            {}
        );
        payload.params.csrf_token = csrfToken();
        var response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'same-origin',
            body: JSON.stringify(payload),
        });
        if (!response.ok) {
            throw new Error('Request failed (' + response.status + ')');
        }
        var data = await response.json();
        if (data.error) {
            var message = (data.error.data && data.error.data.message) || data.error.message || 'RPC error';
            throw new Error(message);
        }
        return data.result;
    }

    function escapeHtml(value) {
        return String(value === undefined || value === null ? '' : value)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    function formatNumber(value, digits) {
        var number = Number(value);
        if (!isFinite(number)) {
            return escapeHtml(value);
        }
        var options = {};
        if (digits !== undefined && digits !== null) {
            options.minimumFractionDigits = digits;
            options.maximumFractionDigits = digits;
        }
        return number.toLocaleString(undefined, options);
    }

    function formatCell(value, format) {
        if (value === false || value === null || value === undefined || value === '') {
            return '<span class="text-muted">—</span>';
        }
        if (Array.isArray(value)) {
            value = value.length > 1 ? value[1] : value[0];
        }
        switch (format) {
            case 'number':
                return escapeHtml(formatNumber(value));
            case 'currency':
                try {
                    return escapeHtml(Number(value).toLocaleString(undefined, {
                        style: 'currency', currency: 'USD', minimumFractionDigits: 2,
                    }));
                } catch (error) {
                    return escapeHtml(value);
                }
            case 'percentage':
                return escapeHtml((Number(value) * 100).toFixed(1) + '%');
            case 'date':
            case 'datetime': {
                var date = new Date(value);
                if (isNaN(date.getTime())) {
                    return escapeHtml(value);
                }
                var options = { year: 'numeric', month: 'short', day: 'numeric' };
                if (format === 'datetime') {
                    options.hour = '2-digit';
                    options.minute = '2-digit';
                }
                return escapeHtml(date.toLocaleDateString(undefined, options));
            }
            case 'boolean':
                return value ? '<i class="fa fa-check text-success"></i>' : '<i class="fa fa-times text-muted"></i>';
            default:
                return escapeHtml(value);
        }
    }

    function spinner() {
        return '<div class="o_widget_placeholder text-center text-muted py-4">' +
            '<i class="fa fa-spinner fa-spin fa-2x"></i> Loading widget...</div>';
    }

    function errorBox(message) {
        return '<div class="o_widget_error d-flex flex-column align-items-center justify-content-center h-100 p-3 text-danger text-center">' +
            '<i class="fa fa-exclamation-triangle fa-2x mb-2"></i>' +
            '<div class="small">' + escapeHtml(message) + '</div>' +
            '</div>';
    }

    function toast(message, type) {
        var existing = document.getElementById('o_dashboard_toast');
        if (existing) {
            existing.remove();
        }
        var node = document.createElement('div');
        node.id = 'o_dashboard_toast';
        node.className = 'o_dashboard_toast alert alert-' + (type || 'success') + ' shadow';
        node.textContent = message;
        document.body.appendChild(node);
        window.setTimeout(function () { node.remove(); }, 2600);
    }

    function itemDataUrl(itemId, token) {
        return '/dashboard/builder/api/items/' + itemId + '/data';
    }

    async function fetchItemData(itemId, token) {
        var params = {};
        if (token) {
            params.token = token;
        }
        return jsonRpc(itemDataUrl(itemId, token), params);
    }

    // ------------------------------------------------------------------
    // Widget renderers
    // ------------------------------------------------------------------
    function renderKpi(container, data) {
        var color = data.color || '#3498db';
        var progress = data.target_progress;
        var html = '<div class="o_kpi_widget d-flex flex-column justify-content-center h-100 p-2">' +
            '<div class="o_kpi_label text-muted small text-truncate">' + escapeHtml(data.label) + '</div>' +
            '<div class="o_kpi_value fw-bold" style="font-size: 2.1rem; color:' + escapeHtml(color) + ';">' +
            escapeHtml(data.formatted_value) + '</div>';
        if (progress !== null && progress !== undefined) {
            var width = Math.max(0, Math.min(100, Number(progress) || 0));
            html += '<div class="o_kpi_target mt-2">' +
                '<div class="progress" style="height: 6px;"><div class="progress-bar" role="progressbar" style="width:' + width + '%; background-color:' + escapeHtml(color) + ';"></div></div>' +
                '<div class="small text-muted mt-1">' + escapeHtml(data.target_label || 'Target') +
                ': ' + escapeHtml(formatNumber(data.target_value)) + ' (' + width.toFixed(0) + '%)</div>' +
                '</div>';
        }
        html += '</div>';
        container.innerHTML = html;
    }

    function renderChart(container, data) {
        if (typeof window.Chart === 'undefined') {
            container.innerHTML = errorBox('Chart.js is not available.');
            return;
        }
        if (container._dashboardChart) {
            container._dashboardChart.destroy();
            container._dashboardChart = null;
        }
        container.innerHTML = '<div class="o_chart_wrapper" style="position:relative;height:100%;min-height:180px;"><canvas></canvas></div>';
        var canvas = container.querySelector('canvas');
        var type = data.chart_type === 'line' ? 'line' : (data.chart_type === 'bar' ? 'bar' : data.chart_type || 'bar');
        var isHorizontal = data.orientation === 'horizontal';
        var options = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: data.show_legend !== false,
                },
            },
            scales: {},
        };
        if (type === 'bar' || type === 'line') {
            options.indexAxis = isHorizontal ? 'y' : 'x';
            options.scales = {
                x: { beginAtZero: true },
                y: { beginAtZero: true, title: { display: !!data.y_axis_label, text: data.y_axis_label || '' } },
            };
            if (isHorizontal) {
                options.scales.x.title = { display: !!data.y_axis_label, text: data.y_axis_label || '' };
                options.scales.y.beginAtZero = false;
            }
        }
        container._dashboardChart = new window.Chart(canvas.getContext('2d'), {
            type: type,
            data: { labels: data.labels || [], datasets: data.datasets || [] },
            options: options,
        });
    }

    function renderPie(container, data) {
        if (typeof window.Chart === 'undefined') {
            container.innerHTML = errorBox('Chart.js is not available.');
            return;
        }
        if (container._dashboardChart) {
            container._dashboardChart.destroy();
            container._dashboardChart = null;
        }
        container.innerHTML = '<div class="o_chart_wrapper" style="position:relative;height:100%;min-height:180px;"><canvas></canvas></div>';
        var canvas = container.querySelector('canvas');
        var percentages = data.percentages || [];
        container._dashboardChart = new window.Chart(canvas.getContext('2d'), {
            type: data.chart_type || 'doughnut',
            data: { labels: data.labels || [], datasets: data.datasets || [] },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', display: data.show_legend !== false },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                var value = context.raw || 0;
                                var percentage = percentages[context.dataIndex] || 0;
                                if (data.label_format === 'percentage') {
                                    return context.label + ': ' + percentage + '%';
                                }
                                if (data.label_format === 'value') {
                                    return context.label + ': ' + formatNumber(value);
                                }
                                return context.label + ': ' + formatNumber(value) + ' (' + percentage + '%)';
                            },
                        },
                    },
                },
            },
        });
    }

    function renderTable(container, data) {
        if (!data.columns || !data.columns.length) {
            container.innerHTML = '<div class="text-muted text-center p-3">No columns configured.</div>';
            return;
        }
        var html = '<div class="o_table_widget table-responsive" style="max-height:100%;">' +
            '<table class="table table-sm table-hover mb-0"><thead><tr>';
        data.columns.forEach(function (column) {
            html += '<th class="text-nowrap">' + escapeHtml(column.label || column.name) + '</th>';
        });
        html += '</tr></thead><tbody>';
        if (!data.rows || !data.rows.length) {
            html += '<tr><td colspan="' + data.columns.length + '" class="text-center text-muted py-3">No records found.</td></tr>';
        } else {
            data.rows.forEach(function (row) {
                html += '<tr>';
                data.columns.forEach(function (column) {
                    html += '<td>' + formatCell(row[column.name], column.format) + '</td>';
                });
                html += '</tr>';
            });
        }
        html += '</tbody></table></div>';
        if (data.total !== undefined) {
            html += '<div class="small text-muted mt-2">Showing ' + (data.rows || []).length +
                ' of ' + data.total + ' record(s)</div>';
        }
        container.innerHTML = html;
    }

    function renderPivot(container, data) {
        var html = '<div class="o_pivot_widget table-responsive" style="max-height:100%;">' +
            '<table class="table table-sm table-bordered mb-0"><thead><tr><th></th>';
        (data.col_labels || []).forEach(function (label) {
            html += '<th class="text-nowrap">' + escapeHtml(label || '(empty)') + '</th>';
        });
        html += '</tr></thead><tbody>';
        (data.rows || []).forEach(function (row) {
            html += '<tr><th class="text-nowrap">' + escapeHtml(row.label || '(empty)') + '</th>';
            (row.values || []).forEach(function (value) {
                html += '<td class="text-end">' + formatCell(value, 'number') + '</td>';
            });
            html += '</tr>';
        });
        html += '</tbody></table></div>';
        container.innerHTML = html;
    }

    function drawGauge(canvas, data) {
        var rect = canvas.getBoundingClientRect();
        var dpr = window.devicePixelRatio || 1;
        var width = Math.max(rect.width, 120);
        var height = Math.max(rect.height, 120);
        canvas.width = width * dpr;
        canvas.height = height * dpr;
        var ctx = canvas.getContext('2d');
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        ctx.clearRect(0, 0, width, height);

        var centerX = width / 2;
        var centerY = height * 0.9;
        var radius = Math.min(width / 2, height * 0.85) * 0.82;
        var min = Number(data.min_value) || 0;
        var max = Number(data.max_value) || 100;
        var value = Number(data.value) || 0;
        var range = (max - min) || 1;
        var ratio = Math.max(0, Math.min(1, (value - min) / range));

        var start = Math.PI;
        var end = 2 * Math.PI;

        ctx.lineWidth = Math.max(10, radius * 0.16);
        ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.strokeStyle = '#e9ecef';
        ctx.arc(centerX, centerY, radius, start, end);
        ctx.stroke();

        var color = data.color || '#3498db';
        ctx.beginPath();
        ctx.strokeStyle = color;
        ctx.arc(centerX, centerY, radius, start, start + Math.PI * ratio);
        ctx.stroke();

        var needleAngle = start + Math.PI * ratio;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(centerX + Math.cos(needleAngle) * radius * 0.82, centerY + Math.sin(needleAngle) * radius * 0.82);
        ctx.lineWidth = 3;
        ctx.strokeStyle = '#2c3e50';
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(centerX, centerY, 6, 0, 2 * Math.PI);
        ctx.fillStyle = '#2c3e50';
        ctx.fill();

        ctx.fillStyle = '#2c3e50';
        ctx.textAlign = 'center';
        ctx.font = 'bold ' + Math.max(16, Math.round(width / 12)) + 'px sans-serif';
        ctx.fillText(data.formatted_value || formatNumber(value), centerX, centerY - radius * 0.28);
        ctx.fillStyle = '#6c757d';
        ctx.font = Math.max(11, Math.round(width / 28)) + 'px sans-serif';
        ctx.fillText(data.label || '', centerX, centerY - radius * 0.05);
        ctx.fillText(formatNumber(min), centerX - radius, centerY + 16);
        ctx.fillText(formatNumber(max), centerX + radius, centerY + 16);
    }

    function renderGauge(container, data) {
        container.innerHTML = '<div style="position:relative;height:100%;min-height:160px;"><canvas style="width:100%;height:100%;display:block;"></canvas></div>';
        var canvas = container.querySelector('canvas');
        // Wait for layout to settle before measuring.
        window.requestAnimationFrame(function () {
            drawGauge(canvas, data);
        });
    }

    function renderProgress(container, data) {
        var percentage = Math.max(0, Math.min(100, Number(data.percentage) || 0));
        var color = data.color || '#2ecc71';
        container.innerHTML = '<div class="o_progress_widget d-flex flex-column justify-content-center h-100 p-2">' +
            '<div class="d-flex justify-content-between mb-1">' +
            '<span class="fw-bold text-truncate">' + escapeHtml(data.label) + '</span>' +
            '<span class="text-muted small">' + percentage.toFixed(0) + '%</span></div>' +
            '<div class="progress" style="height:16px;">' +
            '<div class="progress-bar" role="progressbar" style="width:' + percentage + '%; background-color:' + escapeHtml(color) + ';"></div></div>' +
            '<div class="small text-muted mt-1">' + escapeHtml(formatNumber(data.value)) +
            ' / ' + escapeHtml(formatNumber(data.target)) + '</div></div>';
    }

    function renderHtml(container, data) {
        if (data.format === 'text') {
            container.innerHTML = '<div class="p-2" style="white-space:pre-wrap;">' + escapeHtml(data.content) + '</div>';
        } else {
            container.innerHTML = '<div class="p-2 o_html_widget">' + (data.content || '') + '</div>';
        }
    }

    function renderActionButtons(container, data) {
        var buttons = data.buttons || [];
        if (!buttons.length) {
            container.innerHTML = '<div class="text-muted text-center p-3">No buttons configured.</div>';
            return;
        }
        var html = '<div class="d-flex flex-wrap gap-2 p-2 align-content-center h-100">';
        buttons.forEach(function (button) {
            var style = button.style || 'primary';
            html += '<button type="button" class="btn btn-' + escapeHtml(style) + '" ' +
                'data-button-index="' + buttons.indexOf(button) + '">' +
                (button.icon ? '<i class="' + escapeHtml(button.icon) + ' me-1"></i>' : '') +
                escapeHtml(button.label || 'Action') + '</button>';
        });
        html += '</div>';
        container.innerHTML = html;
        container.querySelectorAll('[data-button-index]').forEach(function (element) {
            element.addEventListener('click', function () {
                var button = buttons[Number(element.dataset.buttonIndex)];
                if (!button) {
                    return;
                }
                if (button.action_type === 'url') {
                    window.open(button.url || '#', '_blank');
                } else if (button.action_type === 'create') {
                    window.location.href = '/web#model=' + encodeURIComponent(button.model || '') + '&view_type=form';
                } else if (button.action_type === 'server_action') {
                    window.location.href = '/web#action=' + encodeURIComponent(button.action_id || '');
                } else {
                    var view = (button.view_mode || 'list').split(',')[0];
                    window.location.href = '/web#model=' + encodeURIComponent(button.model || '') +
                        '&view_type=' + encodeURIComponent(view);
                }
            });
        });
    }

    function renderCalendar(container, data) {
        var events = data.events || [];
        if (!events.length) {
            container.innerHTML = '<div class="text-muted text-center p-3">No events found.</div>';
            return;
        }
        var html = '<div class="o_calendar_widget p-2" style="max-height:100%;overflow:auto;">';
        events.forEach(function (event) {
            var raw = event.date ? String(event.date).slice(0, 10) : '';
            html += '<div class="d-flex align-items-start mb-2 pb-2 border-bottom">' +
                '<div class="o_calendar_date badge bg-primary me-2">' + escapeHtml(raw) + '</div>' +
                '<div class="text-truncate">' + escapeHtml(event.title) + '</div></div>';
        });
        html += '</div>';
        container.innerHTML = html;
    }

    function renderWidget(container, data, component) {
        component = component || (data && data.component) || '';
        if (!data || data.error) {
            container.innerHTML = errorBox((data && data.error) || 'Unable to load widget.');
            return;
        }
        switch (component) {
            case 'DashboardKpiCard':
                renderKpi(container, data);
                break;
            case 'DashboardBarChart':
            case 'DashboardLineChart':
                renderChart(container, data);
                break;
            case 'DashboardPieChart':
                renderPie(container, data);
                break;
            case 'DashboardTable':
                renderTable(container, data);
                break;
            case 'DashboardPivotTable':
                renderPivot(container, data);
                break;
            case 'DashboardGauge':
                renderGauge(container, data);
                break;
            case 'DashboardProgressBar':
                renderProgress(container, data);
                break;
            case 'DashboardHtml':
                renderHtml(container, data);
                break;
            case 'DashboardActionButtons':
                renderActionButtons(container, data);
                break;
            case 'DashboardCalendar':
                renderCalendar(container, data);
                break;
            default:
                container.innerHTML = '<pre class="small p-2 mb-0" style="max-height:100%;overflow:auto;">' +
                    escapeHtml(JSON.stringify(data, null, 2)) + '</pre>';
        }
    }

    async function loadWidget(wrapper, token) {
        var content = wrapper.querySelector('.o_dashboard_item_content');
        if (!content) {
            return;
        }
        content.innerHTML = spinner();
        try {
            var result = await fetchItemData(wrapper.dataset.itemId, token);
            if (result.error) {
                throw new Error(result.error);
            }
            renderWidget(content, result.data, wrapper.dataset.component);
        } catch (error) {
            content.innerHTML = errorBox(error.message || String(error));
        }
    }

    async function loadAllWidgets(root, token) {
        var wrappers = Array.prototype.slice.call(
            root.querySelectorAll('.o_dashboard_grid .o_dashboard_item_wrapper[data-item-id]')
        );
        await Promise.all(wrappers.map(function (wrapper) {
            return loadWidget(wrapper, token);
        }));
    }

    // ------------------------------------------------------------------
    // Simple dropdown + modal helpers (Bootstrap JS is not loaded on frontend)
    // ------------------------------------------------------------------
    function setupDropdowns(root) {
        root.querySelectorAll('[data-dashboard-dropdown]').forEach(function (toggle) {
            toggle.addEventListener('click', function (event) {
                event.preventDefault();
                event.stopPropagation();
                var menu = toggle.parentElement.querySelector('.dropdown-menu');
                if (!menu) {
                    return;
                }
                var isOpen = menu.classList.contains('show');
                root.querySelectorAll('.dropdown-menu.show').forEach(function (openMenu) {
                    openMenu.classList.remove('show');
                });
                if (!isOpen) {
                    menu.classList.add('show');
                }
            });
        });
        document.addEventListener('click', function () {
            root.querySelectorAll('.dropdown-menu.show').forEach(function (menu) {
                menu.classList.remove('show');
            });
        });
    }

    function showTextModal(title, text) {
        closeModal();
        var overlay = document.createElement('div');
        overlay.className = 'o_dashboard_modal_overlay';
        overlay.id = 'o_dashboard_modal';
        overlay.innerHTML =
            '<div class="o_dashboard_modal shadow">' +
            '<div class="o_dashboard_modal_header d-flex justify-content-between align-items-center p-3 border-bottom">' +
            '<h5 class="mb-0">' + escapeHtml(title) + '</h5>' +
            '<button type="button" class="btn-close" data-modal-close="1"></button></div>' +
            '<div class="o_dashboard_modal_body p-3">' +
            '<textarea class="form-control font-monospace" rows="8" readonly="readonly"></textarea></div>' +
            '<div class="o_dashboard_modal_footer p-3 border-top text-end">' +
            '<button type="button" class="btn btn-primary" data-modal-copy="1">Copy</button> ' +
            '<button type="button" class="btn btn-secondary" data-modal-close="1">Close</button></div></div>';
        overlay.querySelector('textarea').value = text || '';
        document.body.appendChild(overlay);
        overlay.addEventListener('click', function (event) {
            if (event.target === overlay || event.target.matches('[data-modal-close]')) {
                closeModal();
            }
            if (event.target.matches('[data-modal-copy]')) {
                var textarea = overlay.querySelector('textarea');
                textarea.select();
                try {
                    document.execCommand('copy');
                    toast('Copied to clipboard');
                } catch (error) {
                    toast('Unable to copy', 'warning');
                }
            }
        });
    }

    function showConfigModal(itemId, config) {
        closeModal();
        var overlay = document.createElement('div');
        overlay.className = 'o_dashboard_modal_overlay';
        overlay.id = 'o_dashboard_modal';
        overlay.innerHTML =
            '<div class="o_dashboard_modal shadow">' +
            '<div class="o_dashboard_modal_header d-flex justify-content-between align-items-center p-3 border-bottom">' +
            '<h5 class="mb-0">Widget Configuration</h5>' +
            '<button type="button" class="btn-close" data-modal-close="1"></button></div>' +
            '<div class="o_dashboard_modal_body p-3">' +
            '<p class="text-muted small">Edit the JSON configuration for this widget.</p>' +
            '<textarea class="form-control font-monospace" rows="14" spellcheck="false"></textarea>' +
            '<div class="text-danger small mt-2" data-modal-error="1" style="display:none;"></div></div>' +
            '<div class="o_dashboard_modal_footer p-3 border-top text-end">' +
            '<button type="button" class="btn btn-secondary" data-modal-close="1">Cancel</button> ' +
            '<button type="button" class="btn btn-primary" data-modal-save="1">Save</button></div></div>';
        var textarea = overlay.querySelector('textarea');
        textarea.value = JSON.stringify(config || {}, null, 2);
        document.body.appendChild(overlay);
        var errorNode = overlay.querySelector('[data-modal-error]');

        overlay.addEventListener('click', async function (event) {
            if (event.target === overlay || event.target.matches('[data-modal-close]')) {
                closeModal();
            }
            if (event.target.matches('[data-modal-save]')) {
                var parsed;
                try {
                    parsed = JSON.parse(textarea.value);
                } catch (error) {
                    errorNode.textContent = 'Invalid JSON: ' + error.message;
                    errorNode.style.display = 'block';
                    return;
                }
                try {
                    await jsonRpc('/dashboard/builder/api/items/' + itemId + '/configure', { config: parsed });
                    closeModal();
                    toast('Configuration saved');
                } catch (error) {
                    errorNode.textContent = error.message || String(error);
                    errorNode.style.display = 'block';
                }
            }
        });
    }

    function closeModal() {
        var existing = document.getElementById('o_dashboard_modal');
        if (existing) {
            existing.remove();
        }
    }

    // ------------------------------------------------------------------
    // Dashboard view
    // ------------------------------------------------------------------
    function setupView(root) {
        var dashboardId = root.dataset.dashboardId;
        var token = root.dataset.shareToken || '';
        var editable = root.dataset.editable === '1';

        setupDropdowns(root);

        root.addEventListener('click', async function (event) {
            var target = event.target.closest('[data-action]');
            if (!target) {
                return;
            }
            var action = target.dataset.action;
            if (target.tagName === 'A') {
                event.preventDefault();
            }
            var wrapper = target.closest('.o_dashboard_item_wrapper');
            if (wrapper && (action === 'configure' || action === 'duplicate' || action === 'remove')) {
                await handleItemAction(target, action);
                return;
            }
            if (action === 'refresh') {
                await loadAllWidgets(root, token);
                toast('Dashboard refreshed');
            } else if (action === 'toggle-theme') {
                // Toggle dark mode by setting a cookie or localStorage
                var isDark = localStorage.getItem('od_theme') === 'dark';
                localStorage.setItem('od_theme', isDark ? '' : 'dark');
                window.location.reload();
            } else if (action === 'fullscreen') {
                if (document.fullscreenElement) {
                    document.exitFullscreen();
                } else {
                    root.requestFullscreen();
                }
            } else if (action === 'edit') {
                window.location.href = '/dashboard/builder/' + dashboardId + '/edit';
            } else if (action === 'export-json') {
                window.location.href = '/dashboard/builder/export/' + dashboardId;
            } else if (action === 'export-pdf') {
                window.location.href = '/dashboard/builder/export/pdf/' + dashboardId;
            } else if (action === 'export-excel') {
                window.location.href = '/dashboard/builder/export/excel/' + dashboardId;
            } else if (action === 'duplicate') {
                try {
                    var result = await jsonRpc('/dashboard/builder/api/dashboard/' + dashboardId + '/duplicate', {});
                    if (result.error) {
                        throw new Error(result.error);
                    }
                    window.location.href = result.redirect;
                } catch (error) {
                    toast(error.message || String(error), 'danger');
                }
            } else if (action === 'delete') {
                if (!window.confirm('Delete this dashboard?')) {
                    return;
                }
                try {
                    var deleted = await jsonRpc('/dashboard/builder/api/dashboard/' + dashboardId + '/delete', {});
                    if (deleted.error) {
                        throw new Error(deleted.error);
                    }
                    window.location.href = deleted.redirect;
                } catch (error) {
                    toast(error.message || String(error), 'danger');
                }
            } else if (action === 'embed') {
                showTextModal('Embed Code', target.dataset.embed || '');
            } else if (action === 'configure') {
                handleItemAction(target, 'configure');
            } else if (action === 'duplicate') {
                handleItemAction(target, 'duplicate');
            } else if (action === 'remove') {
                handleItemAction(target, 'remove');
            } else if (action === 'apply-filters' || action === 'clear-filters') {
                await loadAllWidgets(root, token);
            }
        });

        var interval = Number(root.dataset.refreshInterval) || 0;
        if (interval > 0) {
            window.setInterval(function () {
                loadAllWidgets(root, token);
            }, interval * 1000);
        }

        loadAllWidgets(root, token);
    }

    async function handleItemAction(target, action) {
        var wrapper = target.closest('.o_dashboard_item_wrapper');
        if (!wrapper) {
            return;
        }
        var itemId = wrapper.dataset.itemId;
        var config = {};
        try {
            config = JSON.parse(wrapper.dataset.config || '{}');
        } catch (error) {
            config = {};
        }
        if (action === 'configure') {
            showConfigModal(itemId, config);
        } else if (action === 'duplicate') {
            try {
                var result = await jsonRpc('/dashboard/builder/api/items/' + itemId + '/duplicate', {});
                if (result.error) {
                    throw new Error(result.error);
                }
                window.location.reload();
            } catch (error) {
                toast(error.message || String(error), 'danger');
            }
        } else if (action === 'remove') {
            if (!window.confirm('Remove this widget from the dashboard?')) {
                return;
            }
            try {
                var removed = await jsonRpc('/dashboard/builder/api/items/' + itemId + '/delete', {});
                if (removed.error) {
                    throw new Error(removed.error);
                }
                wrapper.remove();
                toast('Widget removed');
            } catch (error) {
                toast(error.message || String(error), 'danger');
            }
        }
    }

    // ------------------------------------------------------------------
    // Shared/public dashboard
    // ------------------------------------------------------------------
    function setupShared(root) {
        var token = root.dataset.shareToken || '';
        setupDropdowns(root);
        root.addEventListener('click', function (event) {
            var target = event.target.closest('[data-action]');
            if (!target) {
                return;
            }
            var action = target.dataset.action;
            if (target.tagName === 'A') {
                event.preventDefault();
            }
            if (action === 'refresh') {
                loadAllWidgets(root, token);
            } else if (action === 'fullscreen') {
                if (document.fullscreenElement) {
                    document.exitFullscreen();
                } else {
                    root.requestFullscreen();
                }
            } else if (action === 'embed') {
                showTextModal('Embed Code', target.dataset.embed || '');
            }
        });
        loadAllWidgets(root, token);
    }

    // ------------------------------------------------------------------
    // Widget test page
    // ------------------------------------------------------------------
    function setupWidgetTest() {
        var grid = document.querySelector('#dashboard-grid[data-widget-test-id]');
        if (!grid) {
            return;
        }
        var widgetId = grid.dataset.widgetTestId;
        var content = grid.querySelector('.o_dashboard_item_content');
        content.innerHTML = spinner();
        jsonRpc('/dashboard/builder/api/widgets/' + widgetId + '/data', {}).then(function (result) {
            if (result.error) {
                throw new Error(result.error);
            }
            renderWidget(content, result.data, content.dataset.widgetComponent);
        }).catch(function (error) {
            content.innerHTML = errorBox(error.message || String(error));
        });
    }

    // ------------------------------------------------------------------
    // Editor
    // ------------------------------------------------------------------
    function setupEditor(root) {
        var dashboardId = root.dataset.dashboardId;
        var grid = document.getElementById('editor-grid');
        if (!grid) {
            return;
        }
        var canvas = document.getElementById('dashboard-canvas');
        var columns = Number(canvas.dataset.columns || 12) || 12;
        var rowHeight = Number(canvas.dataset.rowHeight || 100) || 100;

        function gridMetrics() {
            var rect = grid.getBoundingClientRect();
            var style = window.getComputedStyle(grid);
            var gap = parseFloat(style.columnGap || style.gap || '10') || 10;
            var colWidth = (rect.width - gap * (columns - 1)) / columns;
            return { rect: rect, gap: gap, colWidth: colWidth };
        }

        function cellFromEvent(event, width) {
            var metrics = gridMetrics();
            var x = Math.floor((event.clientX - metrics.rect.left) / (metrics.colWidth + metrics.gap));
            var y = Math.floor((event.clientY - metrics.rect.top) / (rowHeight + metrics.gap));
            x = Math.max(0, Math.min(columns - width, x));
            y = Math.max(0, y);
            return { x: x, y: y };
        }

        function applyGeometry(element, x, y, w, h) {
            element.dataset.x = x;
            element.dataset.y = y;
            element.dataset.w = w;
            element.dataset.h = h;
            element.style.gridColumn = (x + 1) + ' / span ' + w;
            element.style.gridRow = (y + 1) + ' / span ' + h;
        }

        function hideDropZone() {
            var dropZone = document.getElementById('drop-zone');
            if (dropZone) {
                dropZone.style.display = grid.querySelectorAll('.o_editor_item').length ? 'none' : '';
            }
        }
        hideDropZone();

        // Search in palette
        var search = document.getElementById('widget-search');
        if (search) {
            search.addEventListener('input', function () {
                var term = search.value.toLowerCase();
                root.querySelectorAll('.o_widget_palette_item').forEach(function (item) {
                    item.style.display = item.textContent.toLowerCase().indexOf(term) === -1 ? 'none' : '';
                });
            });
        }

        // Palette drag and click-to-add
        root.querySelectorAll('.o_widget_palette_item').forEach(function (item) {
            item.addEventListener('dragstart', function (event) {
                event.dataTransfer.effectAllowed = 'copy';
                event.dataTransfer.setData('text/x-dashboard-widget', item.dataset.widgetId);
                event.dataTransfer.setData(
                    'text/x-dashboard-widget-size',
                    (item.dataset.defaultWidth || 6) + 'x' + (item.dataset.defaultHeight || 4)
                );
            });
            item.addEventListener('click', async function () {
                var nextY = 0;
                root.querySelectorAll('.o_editor_item').forEach(function (existing) {
                    var bottom = Number(existing.dataset.y || 0) + Number(existing.dataset.h || 4);
                    if (bottom > nextY) {
                        nextY = bottom;
                    }
                });
                await createWidget(item.dataset.widgetId, 0, nextY, item.dataset.defaultWidth, item.dataset.defaultHeight);
            });
        });

        async function createWidget(widgetId, x, y, width, height) {
            try {
                var result = await jsonRpc('/dashboard/builder/api/items/create', {
                    dashboard_id: dashboardId,
                    widget_id: widgetId,
                    x: x,
                    y: y,
                    w: width || 6,
                    h: height || 4,
                });
                if (result.error) {
                    throw new Error(result.error);
                }
                window.location.href = result.redirect || window.location.href;
            } catch (error) {
                toast(error.message || String(error), 'danger');
            }
        }

        // Existing items: draggable + resize handles
        root.querySelectorAll('.o_editor_item').forEach(function (item) {
            item.draggable = true;
            item.addEventListener('dragstart', function (event) {
                if (event.target.closest('button, .resize-handle')) {
                    event.preventDefault();
                    return;
                }
                if (item.dataset.locked === 'True' || item.dataset.locked === 'true') {
                    event.preventDefault();
                    return;
                }
                event.dataTransfer.effectAllowed = 'move';
                event.dataTransfer.setData('text/x-dashboard-item', item.dataset.itemId);
            });

            item.querySelectorAll('.resize-handle').forEach(function (handle) {
                handle.addEventListener('mousedown', function (event) {
                    if (item.dataset.locked === 'True' || item.dataset.locked === 'true') {
                        return;
                    }
                    event.preventDefault();
                    event.stopPropagation();
                    startResize(item, handle, event);
                });
            });
        });

        function startResize(item, handle, startEvent) {
            var metrics = gridMetrics();
            var start = {
                x: Number(item.dataset.x || 0),
                y: Number(item.dataset.y || 0),
                w: Number(item.dataset.w || 6),
                h: Number(item.dataset.h || 4),
                clientX: startEvent.clientX,
                clientY: startEvent.clientY,
            };
            var direction = handle.dataset.dir || 'se';

            function onMove(event) {
                var dx = Math.round((event.clientX - start.clientX) / (metrics.colWidth + metrics.gap));
                var dy = Math.round((event.clientY - start.clientY) / (rowHeight + metrics.gap));
                var x = start.x;
                var y = start.y;
                var w = start.w;
                var h = start.h;

                if (direction.indexOf('e') !== -1) {
                    w = start.w + dx;
                }
                if (direction.indexOf('s') !== -1) {
                    h = start.h + dy;
                }
                if (direction.indexOf('w') !== -1) {
                    x = start.x + dx;
                    w = start.w - dx;
                }
                if (direction.indexOf('n') !== -1) {
                    y = start.y + dy;
                    h = start.h - dy;
                }

                w = Math.max(1, Math.min(columns, w));
                h = Math.max(1, h);
                x = Math.max(0, Math.min(columns - w, x));
                y = Math.max(0, y);
                applyGeometry(item, x, y, w, h);
            }

            async function onUp() {
                document.removeEventListener('mousemove', onMove);
                document.removeEventListener('mouseup', onUp);
                await persistGeometry(item);
            }

            document.addEventListener('mousemove', onMove);
            document.addEventListener('mouseup', onUp, { once: true });
        }

        async function persistGeometry(item) {
            try {
                var result = await jsonRpc('/dashboard/builder/api/items/' + item.dataset.itemId + '/update', {
                    values: {
                        pos_x: Number(item.dataset.x || 0),
                        pos_y: Number(item.dataset.y || 0),
                        width: Number(item.dataset.w || 6),
                        height: Number(item.dataset.h || 4),
                    },
                });
                if (result.error) {
                    throw new Error(result.error);
                }
            } catch (error) {
                toast(error.message || String(error), 'danger');
            }
        }

        grid.addEventListener('dragover', function (event) {
            event.preventDefault();
            var isMove = Array.prototype.indexOf.call(
                event.dataTransfer.types, 'text/x-dashboard-item'
            ) !== -1;
            event.dataTransfer.dropEffect = isMove ? 'move' : 'copy';
        });

        grid.addEventListener('drop', async function (event) {
            event.preventDefault();
            var itemId = event.dataTransfer.getData('text/x-dashboard-item');
            var widgetId = event.dataTransfer.getData('text/x-dashboard-widget');
            if (widgetId) {
                var size = (event.dataTransfer.getData('text/x-dashboard-widget-size') || '6x4').split('x');
                var width = Number(size[0]) || 6;
                var height = Number(size[1]) || 4;
                var position = cellFromEvent(event, width);
                await createWidget(widgetId, position.x, position.y, width, height);
                return;
            }
            if (!itemId) {
                return;
            }
            var item = grid.querySelector('.o_editor_item[data-item-id="' + itemId + '"]');
            if (!item || item.dataset.locked === 'True' || item.dataset.locked === 'true') {
                return;
            }
            var width = Number(item.dataset.w || 6);
            var cell = cellFromEvent(event, width);
            applyGeometry(item, cell.x, cell.y, width, Number(item.dataset.h || 4));
            await persistGeometry(item);
        });

        // Item controls
        root.addEventListener('click', async function (event) {
            var target = event.target.closest('[data-action]');
            if (!target) {
                return;
            }
            var action = target.dataset.action;
            if (action === 'save') {
                var payload = Array.prototype.slice.call(grid.querySelectorAll('.o_editor_item')).map(function (item) {
                    return {
                        id: Number(item.dataset.itemId),
                        x: Number(item.dataset.x || 0),
                        y: Number(item.dataset.y || 0),
                        w: Number(item.dataset.w || 6),
                        h: Number(item.dataset.h || 4),
                    };
                });
                try {
                    await jsonRpc('/dashboard/builder/api/items/reorder', { items: payload });
                    toast('Layout saved');
                } catch (error) {
                    toast(error.message || String(error), 'danger');
                }
                return;
            }
            if (action === 'preview') {
                window.location.href = '/dashboard/builder/' + dashboardId;
                return;
            }
            var item = target.closest('.o_editor_item');
            if (!item) {
                return;
            }
            var itemId = item.dataset.itemId;
            if (action === 'configure') {
                var config = {};
                try {
                    config = JSON.parse(item.dataset.config || '{}');
                } catch (error) {
                    config = {};
                }
                showConfigModal(itemId, config);
            } else if (action === 'lock') {
                var locked = item.dataset.locked === 'True' || item.dataset.locked === 'true';
                try {
                    await jsonRpc('/dashboard/builder/api/items/' + itemId + '/update', { values: { is_locked: !locked } });
                    window.location.reload();
                } catch (error) {
                    toast(error.message || String(error), 'danger');
                }
            } else if (action === 'visibility') {
                var style = window.getComputedStyle(item);
                var visible = style.display !== 'none';
                try {
                    await jsonRpc('/dashboard/builder/api/items/' + itemId + '/update', { values: { is_visible: !visible } });
                    item.style.display = visible ? 'none' : '';
                } catch (error) {
                    toast(error.message || String(error), 'danger');
                }
            } else if (action === 'remove') {
                if (!window.confirm('Remove this widget?')) {
                    return;
                }
                try {
                    await jsonRpc('/dashboard/builder/api/items/' + itemId + '/delete', {});
                    item.remove();
                    hideDropZone();
                    toast('Widget removed');
                } catch (error) {
                    toast(error.message || String(error), 'danger');
                }
            }
        });
    }

    // ------------------------------------------------------------------
    // Bootstrap
    // ------------------------------------------------------------------
    document.addEventListener('DOMContentLoaded', function () {
        var view = document.getElementById('o_dashboard_root');
        if (view) {
            if (view.classList.contains('o_dashboard_shared_view')) {
                setupShared(view);
            } else {
                setupView(view);
            }
        }
        var editor = document.getElementById('o_dashboard_editor_root');
        if (editor) {
            setupEditor(editor);
        }
        setupWidgetTest();
    });
})();
