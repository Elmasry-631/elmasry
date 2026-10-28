/**
 * Dashboard Builder - Main JavaScript Module
 * 
 * Handles dashboard rendering, editing, and widget management.
 */

odoo.define('el_dashboard_builder.DashboardBuilder', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var Widget = require('web.Widget');
    var rpc = require('web.rpc');
    var session = require('web.session');
    var Dialog = require('web.Dialog');

    var _t = core._t;
    var qweb = core.qweb;

    var DashboardBuilder = AbstractAction.extend({
        template: 'DashboardBuilderView',
        events: {
            'click [data-action="edit"]': '_onEditClick',
            'click [data-action="refresh"]': '_onRefreshClick',
            'click [data-action="fullscreen"]': '_onFullscreenClick',
            'click [data-action="export-pdf"]': '_onExportPdfClick',
            'click [data-action="export-excel"]': '_onExportExcelClick',
            'click [data-action="duplicate"]': '_onDuplicateClick',
            'click [data-action="delete"]': '_onDeleteClick',
            'click [data-action="apply-filters"]': '_onApplyFiltersClick',
            'click [data-action="clear-filters"]': '_onClearFiltersClick',
            'click [data-action="add-widget"]': '_onAddWidgetClick',
            'change [data-filter-id]': '_onFilterChange',
        },

        init: function (parent, params) {
            this._super.apply(this, arguments);
            this.dashboardId = params.dashboard_id;
            this.dashboard = params.dashboard;
            this.items = params.items || [];
            this.filters = params.filters || [];
            this.editable = params.editable || false;
            this.layoutConfig = params.layout_config || {};
            this.widgetsData = {};
            this.gridStack = null;
        },

        willStart: function () {
            return this._super.apply(this, arguments).then(function () {
                return this._loadWidgetData();
            }.bind(this));
        },

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self._initGrid();
                self._renderWidgets();
                self._setupEventListeners();
                self._applyCustomCSS();
            });
        },

        _loadWidgetData: function () {
            var self = this;
            var defs = this.items.map(function (item) {
                return self._fetchWidgetData(item.id).then(function (data) {
                    self.widgetsData[item.id] = data;
                }).catch(function (error) {
                    console.error('Failed to load widget data:', error);
                    self.widgetsData[item.id] = { error: error.message };
                });
            });
            return Promise.all(defs);
        },

        _fetchWidgetData: function (itemId) {
            return rpc.query({
                route: '/dashboard/builder/api/items/' + itemId + '/data',
                params: {}
            });
        },

        _initGrid: function () {
            var self = this;
            var $grid = this.$('#dashboard-grid');
            
            if (this.editable && typeof GridStack !== 'undefined') {
                this.gridStack = GridStack.init({
                    column: this.layoutConfig.columns || 12,
                    cellHeight: this.layoutConfig.rowHeight || 100,
                    margin: this.layoutConfig.margin || [10, 10],
                    float: true,
                    animate: true,
                    draggable: {
                        handle: '.o_dashboard_item_header',
                        appendTo: 'body',
                    },
                    resizable: {
                        handles: 'se, sw, ne, nw',
                    },
                    acceptWidgets: true,
                }, $grid[0]);

                this.gridStack.on('change', function (event, items) {
                    self._onGridChange(items);
                });

                this.gridStack.on('added', function (event, items) {
                    self._onWidgetAdded(items);
                });

                this.gridStack.on('removed', function (event, items) {
                    self._onWidgetRemoved(items);
                });
            }

            // Set initial positions
            this.items.forEach(function (item) {
                var el = $grid.find('[data-item-id="' + item.id + '"]')[0];
                if (el && self.gridStack) {
                    self.gridStack.move(el, item.pos_x, item.pos_y);
                    self.gridStack.resize(el, item.width, item.height);
                }
            });
        },

        _renderWidgets: function () {
            var self = this;
            this.items.forEach(function (item) {
                self._renderWidget(item);
            });
        },

        _renderWidget: function (item) {
            var $container = this.$('[data-item-id="' + item.id + '"] .o_dashboard_item_content');
            var widgetData = this.widgetsData[item.id] || {};
            
            if (widgetData.error) {
                $container.html(qweb.render('el_dashboard_builder.WidgetError', {
                    error_message: widgetData.error
                }));
                return;
            }

            var componentName = item.component_name;
            if (componentName && window[componentName]) {
                // Instantiate Owl component if available
                var Component = window[componentName];
                var widget = new Component($container[0], {
                    data: widgetData.data,
                    config: item.config,
                    meta: widgetData.meta,
                });
                widget.mount($container[0]);
            } else {
                // Fallback rendering
                $container.html('<div class="text-center text-muted py-4"><i class="fa fa-puzzle-piece fa-2x"/><br/>Widget: ' + item.widget_name + '</div>');
            }
        },

        _onGridChange: function (items) {
            var updates = items.map(function (gridItem) {
                var itemId = parseInt(gridItem.el.dataset.itemId);
                return {
                    id: itemId,
                    x: gridItem.x,
                    y: gridItem.y,
                    w: gridItem.w,
                    h: gridItem.h,
                };
            });
            
            this._savePositions(updates);
        },

        _onWidgetAdded: function (items) {
            // Handle new widget added via drag from palette
        },

        _onWidgetRemoved: function (items) {
            // Handle widget removed
        },

        _savePositions: function (updates) {
            rpc.query({
                route: '/dashboard/builder/api/items/reorder',
                params: { items: updates }
            }).catch(function (error) {
                console.error('Failed to save positions:', error);
                // Optionally show notification
            });
        },

        _onEditClick: function () {
            window.location.href = '/dashboard/builder/' + this.dashboardId + '/edit';
        },

        _onRefreshClick: function () {
            var self = this;
            this.$('[data-action="refresh"]').prop('disabled', true).html('<i class="fa fa-spinner fa-spin"/>');
            
            this._loadWidgetData().then(function () {
                self._renderWidgets();
                self.$('[data-action="refresh"]').prop('disabled', false).html('<i class="fa fa-refresh"/> Refresh');
            });
        },

        _onFullscreenClick: function () {
            var elem = document.documentElement;
            if (!document.fullscreenElement) {
                elem.requestFullscreen().catch(function (err) {
                    console.error('Fullscreen error:', err);
                });
            } else {
                document.exitFullscreen();
            }
        },

        _onExportPdfClick: function () {
            // Trigger browser print for PDF export
            window.print();
        },

        _onExportExcelClick: function () {
            // Export dashboard data to Excel
            var self = this;
            var exportData = this.items.map(function (item) {
                return {
                    widget: item.widget_name,
                    data: self.widgetsData[item.id],
                };
            });
            
            // Create CSV/Excel download
            var csv = 'Widget,Data\n' + exportData.map(function (d) {
                return '"' + d.widget + '","' + JSON.stringify(d.data).replace(/"/g, '""') + '"';
            }).join('\n');
            
            var blob = new Blob([csv], { type: 'text/csv' });
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'dashboard_' + this.dashboard.name.replace(/\s+/g, '_') + '.csv';
            a.click();
            URL.revokeObjectURL(url);
        },

        _onDuplicateClick: function () {
            var self = this;
            rpc.query({
                route: '/dashboard/builder/' + this.dashboardId + '/duplicate',
                params: {}
            }).then(function (result) {
                if (result.res_id) {
                    window.location.href = '/dashboard/builder/' + result.res_id + '/edit';
                }
            });
        },

        _onDeleteClick: function () {
            var self = this;
            Dialog.confirm(this, _t('Are you sure you want to delete this dashboard?'), {
                confirm_callback: function () {
                    rpc.query({
                        model: 'dashboard.builder',
                        method: 'unlink',
                        args: [[self.dashboardId]],
                    }).then(function () {
                        window.location.href = '/web#action=el_dashboard_builder.action_dashboard_builder_list';
                    });
                },
            });
        },

        _onApplyFiltersClick: function () {
            var filterValues = {};
            this.$('[data-filter-id]').each(function () {
                var $select = $(this);
                var filterId = $select.data('filter-id');
                var value = $select.val();
                if (value) {
                    filterValues[filterId] = value;
                }
            });
            
            // Reload widgets with filters
            this._loadWidgetData().then(function () {
                this._renderWidgets();
            }.bind(this));
        },

        _onClearFiltersClick: function () {
            this.$('[data-filter-id]').val('');
            this._onApplyFiltersClick();
        },

        _onFilterChange: function (ev) {
            // Optional: auto-apply on change
        },

        _onAddWidgetClick: function () {
            // Open add widget modal
            this._showAddWidgetModal();
        },

        _showAddWidgetModal: function () {
            var self = this;
            var $modal = $(qweb.render('el_dashboard_builder.AddWidgetModal', {
                widget_categories: self._getWidgetCategories(),
            }));
            
            $modal.on('click', '.o_add_widget_option', function () {
                var widgetId = $(this).data('widget-id');
                var widgetXmlId = $(this).data('widget-xml-id');
                var component = $(this).data('component');
                $modal.modal('hide');
                self._addWidgetToDashboard(widgetId, widgetXmlId, component);
            });
            
            $modal.modal('show');
        },

        _getWidgetCategories: function () {
            // Return widget categories from the template context
            return [
                { key: 'kpi', label: 'KPI / Metrics' },
                { key: 'chart', label: 'Charts' },
                { key: 'table', label: 'Tables / Lists' },
                { key: 'pivot', label: 'Pivot Tables' },
                { key: 'gauge', label: 'Gauges / Progress' },
                { key: 'custom', label: 'Custom / HTML' },
                { key: 'action', label: 'Action Buttons' },
                { key: 'calendar', label: 'Calendar / Timeline' },
            ];
        },

        _addWidgetToDashboard: function (widgetId, widgetXmlId, component) {
            var self = this;
            rpc.query({
                model: 'dashboard.builder.item',
                method: 'create',
                args: [{
                    dashboard_id: this.dashboardId,
                    widget_id: widgetId,
                    pos_x: 0,
                    pos_y: this.items.length * 2,
                    width: 6,
                    height: 4,
                }],
            }).then(function (newItemId) {
                // Reload page or add dynamically
                window.location.reload();
            });
        },

        _setupEventListeners: function () {
            var self = this;
            
            // Handle window resize
            $(window).on('resize', function () {
                if (self.gridStack) {
                    self.gridStack.resizeAll();
                }
            });

            // Handle keyboard shortcuts
            $(document).on('keydown', function (e) {
                if (e.ctrlKey && e.key === 's') {
                    e.preventDefault();
                    if (self.editable) {
                        self._saveLayout();
                    }
                }
            });
        },

        _saveLayout: function () {
            if (!this.gridStack) return;
            
            var layout = this.gridStack.save();
            var layoutConfig = $.extend({}, this.layoutConfig, {
                items: layout,
            });
            
            rpc.query({
                route: '/dashboard/builder/api/dashboard/' + this.dashboardId + '/layout',
                params: { layout_config: layoutConfig }
            }).then(function () {
                // Show saved notification
                self.displayNotification({
                    title: _t('Success'),
                    message: _t('Layout saved successfully'),
                    type: 'success',
                });
            });
        },

        _applyCustomCSS: function () {
            if (this.dashboard.custom_css) {
                var styleId = 'dashboard-custom-css-' + this.dashboardId;
                var $style = $('#' + styleId);
                if (!$style.length) {
                    $style = $('<style id="' + styleId + '"></style>').appendTo('head');
                }
                $style.text(this.dashboard.custom_css);
            }
        },

        destroy: function () {
            if (this.gridStack) {
                this.gridStack.destroy();
            }
            $(window).off('resize');
            this._super.apply(this, arguments);
        },
    });

    core.action_registry.add('dashboard_builder_view', DashboardBuilder);
    return DashboardBuilder;
});


// Dashboard Editor Component
odoo.define('el_dashboard_builder.DashboardEditor', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var Dialog = require('web.Dialog');

    var _t = core._t;
    var qweb = core.qweb;

    var DashboardEditor = AbstractAction.extend({
        template: 'DashboardBuilderEditor',
        events: {
            'click [data-action="preview"]': '_onPreviewClick',
            'click [data-action="save"]': '_onSaveClick',
            'click [data-action="exit"]': '_onExitClick',
            'click [data-action="close-config"]': '_onCloseConfigClick',
            'click [data-action="save-config"]': '_onSaveConfigClick',
            'dragstart .o_widget_palette_item': '_onWidgetDragStart',
            'dragover #editor-grid': '_onGridDragOver',
            'drop #editor-grid': '_onGridDrop',
            'dragleave #editor-grid': '_onGridDragLeave',
            'click [data-action="configure"]': '_onConfigureClick',
            'click [data-action="lock"]': '_onLockClick',
            'click [data-action="visibility"]': '_onVisibilityClick',
            'click [data-action="remove"]': '_onRemoveClick',
            'mousedown .resize-handle': '_onResizeStart',
            'input #widget-search': '_onWidgetSearch',
        },

        init: function (parent, params) {
            this._super.apply(this, arguments);
            this.dashboardId = params.dashboard_id;
            this.dashboard = params.dashboard;
            this.items = params.items || [];
            this.widgetCategories = params.widget_categories || [];
            this.widgetsByCategory = params.widgets_by_category || {};
            this.layoutConfig = params.layout_config || {};
            this.gridStack = null;
            this.selectedItem = null;
            this.dragItem = null;
        },

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self._initEditorGrid();
                self._renderWidgetPalette();
                self._setupResizeHandlers();
            });
        },

        _initEditorGrid: function () {
            var self = this;
            var $grid = this.$('#editor-grid');
            
            if (typeof GridStack !== 'undefined') {
                this.gridStack = GridStack.init({
                    column: this.layoutConfig.columns || 12,
                    cellHeight: this.layoutConfig.rowHeight || 100,
                    margin: this.layoutConfig.margin || [10, 10],
                    float: true,
                    animate: true,
                    draggable: {
                        handle: '.o_dashboard_item_header',
                    },
                    resizable: {
                        handles: 'se, sw, ne, nw',
                    },
                    acceptWidgets: true,
                }, $grid[0]);

                this.gridStack.on('change', function (event, items) {
                    self._onGridChange(items);
                });

                this.gridStack.on('resizestop', function (event, items) {
                    self._onGridResize(items);
                });
            }

            // Set initial positions
            this.items.forEach(function (item) {
                var el = $grid.find('[data-item-id="' + item.id + '"]')[0];
                if (el && self.gridStack) {
                    self.gridStack.move(el, item.pos_x, item.pos_y);
                    self.gridStack.resize(el, item.width, item.height);
                }
            });
        },

        _renderWidgetPalette: function () {
            var self = this;
            var $palette = this.$('#widget-palette');
            var html = '';
            
            this.widgetCategories.forEach(function (category) {
                var widgets = self.widgetsByCategory[category.key] || [];
                if (widgets.length === 0) return;
                
                html += '<div class="o_widget_category mb-3" data-category="' + category.key + '">';
                html += '<h6 class="text-uppercase text-muted small mb-2">' + category.label + '</h6>';
                html += '<div class="o_widget_list" data-category="' + category.key + '">';
                
                widgets.forEach(function (widget) {
                    html += '<div class="o_widget_palette_item p-2 mb-2 border rounded bg-white cursor-grab shadow-sm" ' +
                        'data-widget-id="' + widget.id + '" ' +
                        'data-widget-xml-id="' + widget.xml_id + '" ' +
                        'data-component="' + widget.component_name + '" ' +
                        'draggable="true">';
                    html += '<div class="d-flex align-items-center">';
                    html += '<i class="fa fa-grip-lines me-2 text-muted" title="Drag to dashboard"></i>';
                    html += '<i class="fa ' + widget.icon + ' me-2" style="color: ' + widget.color + '"></i>';
                    html += '<span class="flex-grow-1 text-truncate">' + widget.name + '</span>';
                    html += '</div>';
                    html += '<small class="text-muted d-block mt-1">' + (widget.description || '') + '</small>';
                    html += '</div>';
                });
                
                html += '</div></div>';
            });
            
            $palette.html(html);
        },

        _onWidgetDragStart: function (ev) {
            var $item = $(ev.currentTarget);
            this.dragItem = {
                widgetId: $item.data('widget-id'),
                widgetXmlId: $item.data('widget-xml-id'),
                component: $item.data('component'),
            };
            ev.originalEvent.dataTransfer.setData('text/plain', JSON.stringify(this.dragItem));
            ev.originalEvent.dataTransfer.effectAllowed = 'copy';
        },

        _onGridDragOver: function (ev) {
            ev.preventDefault();
            ev.originalEvent.dataTransfer.dropEffect = 'copy';
            this.$('#editor-grid').addClass('drag-over');
        },

        _onGridDragLeave: function (ev) {
            this.$('#editor-grid').removeClass('drag-over');
        },

        _onGridDrop: function (ev) {
            ev.preventDefault();
            this.$('#editor-grid').removeClass('drag-over');
            
            if (!this.dragItem) return;
            
            var grid = this.gridStack;
            if (!grid) return;
            
            // Calculate grid position from mouse coordinates
            var rect = ev.currentTarget.getBoundingClientRect();
            var x = Math.floor((ev.originalEvent.clientX - rect.left) / (grid.cellWidth() + grid.opts.margin[0]));
            var y = Math.floor((ev.originalEvent.clientY - rect.top) / (grid.cellHeight() + grid.opts.margin[1]));
            
            x = Math.max(0, Math.min(x, grid.opts.column - 1));
            y = Math.max(0, y);
            
            this._addWidgetAtPosition(this.dragItem, x, y);
            this.dragItem = null;
        },

        _addWidgetAtPosition: function (dragItem, x, y) {
            var self = this;
            var defaultWidth = 6;
            var defaultHeight = 4;
            
            rpc.query({
                model: 'dashboard.builder.item',
                method: 'create',
                args: [{
                    dashboard_id: this.dashboardId,
                    widget_id: dragItem.widgetId,
                    pos_x: x,
                    pos_y: y,
                    width: defaultWidth,
                    height: defaultHeight,
                }],
            }).then(function (newItemId) {
                // Add to grid
                var el = $(qweb.render('el_dashboard_builder.EditorItem', {
                    item: {
                        id: newItemId,
                        widget_xml_id: dragItem.widgetXmlId,
                        widget_name: dragItem.component,
                        component_name: dragItem.component,
                        pos_x: x,
                        pos_y: y,
                        width: defaultWidth,
                        height: defaultHeight,
                        is_locked: false,
                        is_visible: true,
                        widget_icon: 'fa fa-square-o',
                        widget_color: '#3498db',
                    }
                }));
                
                grid.addWidget(el[0], x, y, defaultWidth, defaultHeight);
                self.items.push({
                    id: newItemId,
                    widget_xml_id: dragItem.widgetXmlId,
                    widget_name: dragItem.component,
                    component_name: dragItem.component,
                    pos_x: x,
                    pos_y: y,
                    width: defaultWidth,
                    height: defaultHeight,
                    is_locked: false,
                    is_visible: true,
                });
            });
        },

        _onGridChange: function (items) {
            var updates = items.map(function (gridItem) {
                var itemId = parseInt(gridItem.el.dataset.itemId);
                return {
                    id: itemId,
                    x: gridItem.x,
                    y: gridItem.y,
                    w: gridItem.w,
                    h: gridItem.h,
                };
            });
            
            rpc.query({
                route: '/dashboard/builder/api/items/reorder',
                params: { items: updates }
            });
        },

        _onGridResize: function (items) {
            // Same as change for now
            this._onGridChange(items);
        },

        _onConfigureClick: function (ev) {
            var $btn = $(ev.currentTarget);
            var itemId = parseInt($btn.closest('[data-item-id]').data('item-id'));
            this._openConfigModal(itemId);
        },

        _onLockClick: function (ev) {
            var $btn = $(ev.currentTarget);
            var itemId = parseInt($btn.closest('[data-item-id]').data('item-id'));
            var item = this.items.find(function (i) { return i.id === itemId; });
            if (item) {
                item.is_locked = !item.is_locked;
                $btn.toggleClass('active');
                this._updateItem(itemId, { is_locked: item.is_locked });
            }
        },

        _onVisibilityClick: function (ev) {
            var $btn = $(ev.currentTarget);
            var itemId = parseInt($btn.closest('[data-item-id]').data('item-id'));
            var item = this.items.find(function (i) { return i.id === itemId; });
            if (item) {
                item.is_visible = !item.is_visible;
                $btn.toggleClass('text-muted').find('i').toggleClass('fa-eye fa-eye-slash');
                this._updateItem(itemId, { is_visible: item.is_visible });
            }
        },

        _onRemoveClick: function (ev) {
            var self = this;
            var $btn = $(ev.currentTarget);
            var itemId = parseInt($btn.closest('[data-item-id]').data('item-id'));
            
            Dialog.confirm(this, _t('Remove this widget from the dashboard?'), {
                confirm_callback: function () {
                    self._removeItem(itemId);
                },
            });
        },

        _removeItem: function (itemId) {
            var self = this;
            rpc.query({
                model: 'dashboard.builder.item',
                method: 'unlink',
                args: [[itemId]],
            }).then(function () {
                // Remove from grid
                if (self.gridStack) {
                    var el = self.$('[data-item-id="' + itemId + '"]')[0];
                    if (el) {
                        self.gridStack.removeWidget(el);
                    }
                }
                // Remove from items array
                self.items = self.items.filter(function (i) { return i.id !== itemId; });
            });
        },

        _updateItem: function (itemId, values) {
            rpc.query({
                model: 'dashboard.builder.item',
                method: 'write',
                args: [[itemId], values],
            });
        },

        _openConfigModal: function (itemId) {
            var item = this.items.find(function (i) { return i.id === itemId; });
            if (!item || !item.widget_id) return;
            
            var widget = item.widget_id;
            var configSchema = widget.config_schema || {};
            var currentConfig = item.config || {};
            
            // Build form fields from schema
            var fieldsHtml = this._buildConfigForm(configSchema, currentConfig);
            
            var $modal = $(qweb.render('el_dashboard_builder.WidgetConfigModal', {
                fields_html: fieldsHtml,
            }));
            
            var self = this;
            $modal.on('click', '[data-action="save-config"]', function () {
                var newConfig = self._collectConfigForm($modal);
                self._saveWidgetConfig(itemId, newConfig);
                $modal.modal('hide');
            });
            
            $modal.modal('show');
        },

        _buildConfigForm: function (schema, currentConfig) {
            // Generate form HTML from JSON schema
            // Simplified implementation
            return '<div class="alert alert-info">Widget configuration form would be generated here based on the widget\'s JSON schema.</div>';
        },

        _collectConfigForm: function ($modal) {
            // Collect form values
            return {};
        },

        _saveWidgetConfig: function (itemId, config) {
            rpc.query({
                route: '/dashboard/builder/api/items/' + itemId + '/configure',
                params: { config: config }
            });
        },

        _onPreviewClick: function () {
            window.open('/dashboard/builder/' + this.dashboardId, '_blank');
        },

        _onSaveClick: function () {
            var self = this;
            this._saveLayout();
            
            this.displayNotification({
                title: _t('Saved'),
                message: _t('Dashboard saved successfully'),
                type: 'success',
            });
        },

        _onExitClick: function () {
            window.location.href = '/dashboard/builder/' + this.dashboardId;
        },

        _onCloseConfigClick: function () {
            this.$('#widget-config').hide();
            this.$('#widget-palette').show();
        },

        _onSaveConfigClick: function () {
            // Handled in _openConfigModal
        },

        _onWidgetSearch: function (ev) {
            var query = $(ev.currentTarget).val().toLowerCase();
            this.$('.o_widget_palette_item').each(function () {
                var $item = $(this);
                var name = $item.find('span').text().toLowerCase();
                var desc = $item.find('small').text().toLowerCase();
                $item.toggle(name.includes(query) || desc.includes(query));
            });
        },

        _setupResizeHandlers: function () {
            // Grid overlay toggle
            this.$('#editor-grid').on('mouseenter', function () {
                if (this.gridStack) {
                    this.$('#grid-overlay').show();
                }
            }.bind(this));
            
            this.$('#editor-grid').on('mouseleave', function () {
                this.$('#grid-overlay').hide();
            }.bind(this));
        },

        _saveLayout: function () {
            if (!this.gridStack) return;
            
            var layout = this.gridStack.save();
            var layoutConfig = $.extend({}, this.layoutConfig, {
                items: layout,
            });
            
            rpc.query({
                route: '/dashboard/builder/api/dashboard/' + this.dashboardId + '/layout',
                params: { layout_config: layoutConfig }
            });
        },

        _onResizeStart: function (ev) {
            // Custom resize handling if needed
        },

        destroy: function () {
            if (this.gridStack) {
                this.gridStack.destroy();
            }
            this._super.apply(this, arguments);
        },
    });

    core.action_registry.add('dashboard_builder_editor', DashboardEditor);
    return DashboardEditor;
});