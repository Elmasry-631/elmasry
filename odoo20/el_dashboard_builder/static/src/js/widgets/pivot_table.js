/**
 * Dashboard Builder - Pivot Table Widget
 * 
 * Renders pivot table for multi-dimensional data analysis.
 */

odoo.define('el_dashboard_builder.widgets.PivotTable', function (require) {
    "use strict";

    var AbstractWidget = require('el_dashboard_builder.widgets.AbstractWidget');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var _t = core._t;
    var qweb = core.qweb;

    var PivotTableWidget = AbstractWidget.extend({
        template: 'el_dashboard_builder.PivotTableWidget',

        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.model = options.config.model;
            this.rowFields = options.config.row_fields || [];
            this.colFields = options.config.col_fields || [];
            this.measureFields = options.config.measure_fields || [];
            this.domain = options.config.domain || [];
            this.subtotals = options.config.subtotals !== false;
            this.grandTotals = options.config.grand_totals !== false;
            this.limit = options.config.limit || 100;
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

            // Build measure fields for read_group
            var measures = this.measureFields.map(function (m) {
                return m.field + ':' + (m.aggregation || 'sum');
            });

            var groupBy = this.rowFields.slice();
            if (this.colFields.length > 0) {
                groupBy = groupBy.concat(this.colFields);
            }

            return rpc.query({
                model: this.model,
                method: 'read_group',
                args: [domain, measures, groupBy],
                kwargs: {
                    lazy: false,
                    limit: this.limit,
                },
            }).then(function (result) {
                self._processPivotData(result);
            });
        },

        _processPivotData: function (groups) {
            var self = this;
            
            // Build pivot structure
            var rows = {};
            var cols = new Set();
            var measures = this.measureFields.map(function (m) { return m.field + ':' + (m.aggregation || 'sum'); });
            
            groups.forEach(function (g) {
                var rowKey = self.rowFields.map(function (f) {
                    var val = g[f];
                    return Array.isArray(val) ? val[1] : val;
                }).join('|');
                
                var colKey = self.colFields.map(function (f) {
                    var val = g[f];
                    return Array.isArray(val) ? val[1] : val;
                }).join('|');
                
                cols.add(colKey);
                
                if (!rows[rowKey]) {
                    rows[rowKey] = { _rowLabel: rowKey };
                }
                
                measures.forEach(function (measure) {
                    var colMeasureKey = colKey + '|' + measure;
                    rows[rowKey][colMeasureKey] = g[measure] || 0;
                });
            });
            
            // Sort columns
            var sortedCols = Array.from(cols).sort();
            
            // Build headers
            var headers = [''].concat(sortedCols.map(function (col) {
                return measures.map(function (measure) {
                    return { col: col, measure: measure };
                });
            }).flat());
            
            // Build data rows
            var dataRows = Object.keys(rows).map(function (rowKey) {
                var row = rows[rowKey];
                var rowData = [row._rowLabel];
                sortedCols.forEach(function (col) {
                    measures.forEach(function (measure) {
                        var key = col + '|' + measure;
                        rowData.push(row[key] || 0);
                    });
                });
                return { label: row._rowLabel, values: rowData.slice(1) };
            });
            
            // Calculate totals if enabled
            var colTotals = [];
            var grandTotals = {};
            if (self.grandTotals) {
                measures.forEach(function (measure) {
                    var total = 0;
                    Object.keys(rows).forEach(function (rowKey) {
                        sortedCols.forEach(function (col) {
                            var key = col + '|' + measure;
                            total += rows[rowKey][key] || 0;
                        });
                    });
                    grandTotals[measure] = total;
                });
            }
            
            if (self.subtotals) {
                sortedCols.forEach(function (col) {
                    var colTotal = {};
                    measures.forEach(function (measure) {
                        var total = 0;
                        Object.keys(rows).forEach(function (rowKey) {
                            var key = col + '|' + measure;
                            total += rows[rowKey][key] || 0;
                        });
                        colTotal[measure] = total;
                    });
                    colTotals.push({ col: col, totals: colTotal });
                });
            }
            
            self.pivotData = {
                headers: headers,
                rows: dataRows,
                colTotals: colTotals,
                grandTotals: grandTotals,
                measures: measures,
            };
        },

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self._renderPivot();
            });
        },

        _renderPivot: function () {
            var $container = this.$('.o_pivot_container');
            var data = this.pivotData;
            
            if (!data) {
                $container.html('<div class="text-center text-muted py-4">No data available</div>');
                return;
            }
            
            var html = '<table class="table table-sm table-bordered o_pivot_table mb-0">';
            
            // Header row
            html += '<thead><tr>';
            this.pivotData.headers.forEach(function (header) {
                if (typeof header === 'string') {
                    html += '<th class="text-center fw-bold">' + header + '</th>';
                } else {
                    html += '<th class="text-center fw-bold">' + header.col + ' - ' + header.measure + '</th>';
                }
            });
            html += '</tr></thead>';
            
            // Data rows
            html += '<tbody>';
            this.pivotData.rows.forEach(function (row) {
                html += '<tr>';
                html += '<td class="fw-bold">' + row.label + '</td>';
                row.values.forEach(function (value) {
                    html += '<td class="text-end">' + value.toLocaleString() + '</td>';
                });
                html += '</tr>';
            });
            html += '</tbody>';
            
            // Grand totals
            if (this.grandTotals && Object.keys(this.pivotData.grandTotals).length > 0) {
                html += '<tfoot><tr class="table-active fw-bold">';
                html += '<td>Grand Total</td>';
                this.pivotData.headers.slice(1).forEach(function (header) {
                    if (typeof header === 'object') {
                        var total = self.pivotData.grandTotals[header.measure] || 0;
                        html += '<td class="text-end">' + total.toLocaleString() + '</td>';
                    } else {
                        html += '<td></td>';
                    }
                });
                html += '</tr></tfoot>';
            }
            
            html += '</table>';
            $container.html(html);
        },
    });

    // Register widget component
    window.DashboardPivotTable = PivotTableWidget;
    return PivotTableWidget;
});