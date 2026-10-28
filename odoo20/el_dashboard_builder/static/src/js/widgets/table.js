/**
 * Dashboard Builder - Data Table Widget
 * 
 * Renders tabular data with sorting, pagination, and formatting.
 */

odoo.define('el_dashboard_builder.widgets.Table', function (require) {
    "use strict";

    var AbstractWidget = require('el_dashboard_builder.widgets.AbstractWidget');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var _t = core._t;
    var qweb = core.qweb;

    var TableWidget = AbstractWidget.extend({
        template: 'el_dashboard_builder.TableWidget',
        events: {
            'click th[data-sort]': '_onSortClick',
            'click .o_pagination a': '_onPageClick',
            'input .o_search_input': '_onSearchInput',
            'click [data-action="drill-down"]': '_onDrillDownClick',
        },

        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.model = options.config.model;
            this.fields = options.config.fields || [];
            this.domain = options.config.domain || [];
            this.order = options.config.order || 'id desc';
            this.limit = options.config.limit || 20;
            this.showPagination = options.config.show_pagination !== false;
            this.showSearch = options.config.show_search !== false;
            this.striped = options.config.striped !== false;
            this.hover = options.config.hover !== false;
            this.bordered = options.config.bordered || false;
            this.compact = options.config.compact || false;
            this.currentPage = 1;
            this.totalCount = 0;
            this.sortField = null;
            this.sortOrder = 'asc';
            this.searchQuery = '';
        },

        willStart: function () {
            return this._super.apply(this, arguments).then(function () {
                return this._fetchData();
            }.bind(this));
        },

        _fetchData: function () {
            var self = this;
            var domain = this.domain.slice();
            
            if (this.globalFilters) {
                domain = domain.concat(this.globalFilters);
            }

            if (this.searchQuery) {
                // Add search across visible fields
                var searchFields = this.fields.filter(function (f) { return f.searchable !== false; })
                    .map(function (f) { return f.name; });
                if (searchFields.length) {
                    var orDomain = [];
                    searchFields.forEach(function (field) {
                        orDomain.push('|');
                        orDomain.push([field, 'ilike', self.searchQuery]);
                    });
                    // Remove last '|'
                    orDomain.pop();
                    domain = ['&'].concat(domain).concat(orDomain);
                }
            }

            var order = this.sortField ? (this.sortField + ' ' + this.sortOrder) : this.order;

            return Promise.all([
                rpc.query({
                    model: this.model,
                    method: 'search_read',
                    args: [domain, this.fields.map(function (f) { return f.name; })],
                    kwargs: {
                        offset: (this.currentPage - 1) * this.limit,
                        limit: this.limit,
                        order: order,
                    },
                }),
                rpc.query({
                    model: this.model,
                    method: 'search_count',
                    args: [domain],
                }),
            ]).then(function (results) {
                self.records = results[0];
                self.totalCount = results[1];
            });
        },

        _formatCellValue: function (record, field) {
            var value = record[field.name];
            var format = field.format || 'text';
            
            if (value === false || value === null || value === undefined) {
                return '<span class="text-muted">—</span>';
            }
            
            switch (format) {
                case 'number':
                    return value.toLocaleString();
                case 'currency':
                    return this._formatCurrency(value, field.currency);
                case 'percentage':
                    return (value * 100).toFixed(field.precision || 1) + '%';
                case 'date':
                    return this._formatDate(value);
                case 'datetime':
                    return this._formatDate(value, 'datetime');
                case 'boolean':
                    return value ? '<i class="fa fa-check text-success"></i>' : '<i class="fa fa-times text-muted"></i>';
                case 'many2one':
                    return Array.isArray(value) ? value[1] : value;
                default:
                    return _.escape(String(value));
            }
        },

        _formatCurrency: function (value, currency) {
            var fmt = new Intl.NumberFormat(undefined, {
                style: 'currency',
                currency: currency || 'USD',
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
            });
            return fmt.format(value);
        },

        _formatDate: function (value, format) {
            var date = new Date(value);
            if (isNaN(date.getTime())) return value;
            
            var options = { year: 'numeric', month: 'short', day: 'numeric' };
            if (format === 'datetime') {
                options.hour = '2-digit';
                options.minute = '2-digit';
            }
            return date.toLocaleDateString(undefined, options);
        },

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self._renderTable();
            });
        },

        _renderTable: function () {
            var $table = this.$('.o_table_widget');
            
            // Build header
            var headerHtml = '<thead><tr>';
            this.fields.forEach(function (field) {
                var sortable = field.sortable !== false ? ' data-sort="' + field.name + '"' : '';
                var width = field.width ? ' style="width: ' + field.width + 'px"' : '';
                var align = field.align ? ' class="text-' + field.align + '"' : '';
                headerHtml += '<th' + sortable + width + align + '>' + (field.label || field.name) + '</th>';
            });
            headerHtml += '</tr></thead>';
            
            // Build body
            var bodyHtml = '<tbody>';
            this.records.forEach(function (record) {
                bodyHtml += '<tr>';
                this.fields.forEach(function (field) {
                    var align = field.align ? ' class="text-' + field.align + '"' : '';
                    bodyHtml += '<td' + align + '>' + this._formatCellValue(record, field) + '</td>';
                }.bind(this));
                bodyHtml += '</tr>';
            }.bind(this));
            bodyHtml += '</tbody>';
            
            $table.html(headerHtml + bodyHtml);
            
            // Apply table classes
            $table.toggleClass('table-striped', this.striped);
            $table.toggleClass('table-hover', this.hover);
            $table.toggleClass('table-bordered', this.bordered);
            $table.toggleClass('table-sm', this.compact);
            
            // Render pagination
            this._renderPagination();
            
            // Render search
            this._renderSearch();
        },

        _renderPagination: function () {
            if (!this.showPagination) return;
            
            var totalPages = Math.ceil(this.totalCount / this.limit);
            if (totalPages <= 1) {
                this.$('.o_pagination').hide();
                return;
            }
            
            this.$('.o_pagination').show();
            var html = '';
            
            // Previous
            html += '<li class="page-item' + (this.currentPage === 1 ? ' disabled' : '') + '">';
            html += '<a class="page-link" href="#" data-page="' + (this.currentPage - 1) + '">&laquo;</a>';
            html += '</li>';
            
            // Page numbers
            var start = Math.max(1, this.currentPage - 2);
            var end = Math.min(totalPages, this.currentPage + 2);
            
            if (start > 1) {
                html += '<li class="page-item"><a class="page-link" href="#" data-page="1">1</a></li>';
                if (start > 2) {
                    html += '<li class="page-item disabled"><span class="page-link">...</span></li>';
                }
            }
            
            for (var i = start; i <= end; i++) {
                html += '<li class="page-item' + (i === this.currentPage ? ' active' : '') + '">';
                html += '<a class="page-link" href="#" data-page="' + i + '">' + i + '</a>';
                html += '</li>';
            }
            
            if (end < totalPages) {
                if (end < totalPages - 1) {
                    html += '<li class="page-item disabled"><span class="page-link">...</span></li>';
                }
                html += '<li class="page-item"><a class="page-link" href="#" data-page="' + totalPages + '">' + totalPages + '</a></li>';
            }
            
            // Next
            html += '<li class="page-item' + (this.currentPage === totalPages ? ' disabled' : '') + '">';
            html += '<a class="page-link" href="#" data-page="' + (this.currentPage + 1) + '">&raquo;</a>';
            html += '</li>';
            
            this.$('.o_pagination ul').html(html);
        },

        _renderSearch: function () {
            if (!this.showSearch) {
                this.$('.o_search_wrapper').hide();
                return;
            }
            
            this.$('.o_search_wrapper').show();
            this.$('.o_search_input').val(this.searchQuery);
        },

        _onSortClick: function (ev) {
            var $th = $(ev.currentTarget);
            var field = $th.data('sort');
            
            if (this.sortField === field) {
                this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
            } else {
                this.sortField = field;
                this.sortOrder = 'asc';
            }
            
            this.currentPage = 1;
            this._fetchData().then(function () {
                this._renderTable();
            }.bind(this));
        },

        _onPageClick: function (ev) {
            ev.preventDefault();
            var $link = $(ev.currentTarget);
            var page = parseInt($link.data('page'));
            
            if (page >= 1 && page <= Math.ceil(this.totalCount / this.limit)) {
                this.currentPage = page;
                this._fetchData().then(function () {
                    this._renderTable();
                }.bind(this));
            }
        },

        _onSearchInput: function (ev) {
            var query = $(ev.currentTarget).val().trim();
            if (query !== this.searchQuery) {
                this.searchQuery = query;
                this.currentPage = 1;
                this._fetchData().then(function () {
                    this._renderTable();
                }.bind(this));
            }
        },

        _onDrillDownClick: function (ev) {
            // Handle row click for drill down
        },
    });

    window.DashboardTable = TableWidget;
    return TableWidget;
});