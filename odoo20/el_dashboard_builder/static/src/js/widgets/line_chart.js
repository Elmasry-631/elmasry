/**
 * Dashboard Builder - Line Chart Widget
 * 
 * Renders line/area charts for time series data.
 */

odoo.define('el_dashboard_builder.widgets.LineChart', function (require) {
    "use strict";

    var AbstractWidget = require('el_dashboard_builder.widgets.AbstractWidget');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var _t = core._t;
    var qweb = core.qweb;

    var LineChartWidget = AbstractWidget.extend({
        template: 'el_dashboard_builder.LineChartWidget',
        chart: null,

        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.model = options.config.model;
            this.xField = options.config.x_field;
            this.yField = options.config.y_field;
            this.aggregation = options.config.aggregation || 'sum';
            this.domain = options.config.domain || [];
            this.groupBy = options.config.group_by;
            this.timeGranularity = options.config.time_granularity || 'month';
            this.fillArea = options.config.fill_area || false;
            this.smoothLines = options.config.smooth_lines !== false;
            this.showPoints = options.config.show_points !== false;
            this.colors = options.config.colors || [
                '#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6',
                '#1abc9c', '#e67e22', '#34495e', '#16a085', '#c0392b'
            ];
            this.showLegend = options.config.show_legend !== false;
            this.yAxisLabel = options.config.y_axis_label;
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

            // Build read_group domain with date truncation
            var groupByField = this.xField;
            if (['day', 'week', 'month', 'quarter', 'year'].includes(this.timeGranularity)) {
                groupByField = this.xField + ':' + this.timeGranularity;
            }

            var groupBy = [groupByField];
            if (this.groupBy) {
                groupBy.push(this.groupBy);
            }

            return rpc.query({
                model: this.model,
                method: 'read_group',
                args: [domain, [this.yField + ':' + this.aggregation], groupBy],
                kwargs: {
                    lazy: false,
                    limit: this.limit,
                },
            }).then(function (result) {
                self._processChartData(result);
            });
        },

        _processChartData: function (groups) {
            var self = this;
            
            if (this.groupBy) {
                // Multi-series line chart
                var series = {};
                var labelsSet = new Set();
                
                groups.forEach(function (g) {
                    var label = g[self.xField];
                    if (Array.isArray(label)) label = label[1];
                    var seriesKey = g[self.groupBy];
                    if (Array.isArray(seriesKey)) seriesKey = seriesKey[1];
                    
                    labelsSet.add(label);
                    
                    if (!series[seriesKey]) {
                        series[seriesKey] = {};
                    }
                    series[seriesKey][label] = g[self.yField + ':' + self.aggregation] || 0;
                });
                
                var labels = Array.from(labelsSet).sort();
                var datasets = Object.keys(series).map(function (key, index) {
                    var data = labels.map(function (label) {
                        return series[key][label] || null; // null for gaps
                    });
                    return {
                        label: key,
                        data: data,
                        borderColor: self.colors[index % self.colors.length],
                        backgroundColor: self.fillArea ? self._hexToRgba(self.colors[index % self.colors.length], 0.1) : 'transparent',
                        fill: self.fillArea,
                        tension: self.smoothLines ? 0.4 : 0,
                        pointRadius: self.showPoints ? 4 : 0,
                        pointHoverRadius: 6,
                        borderWidth: 2,
                    };
                });
                
                this.chartData = {
                    labels: labels,
                    datasets: datasets,
                };
            } else {
                // Single series line chart
                var labels = [];
                var data = [];
                
                groups.forEach(function (g) {
                    var label = g[self.xField];
                    if (Array.isArray(label)) label = label[1];
                    labels.push(label);
                    data.push(g[self.yField + ':' + self.aggregation] || 0);
                });
                
                this.chartData = {
                    labels: labels,
                    datasets: [{
                        label: this.yField,
                        data: data,
                        borderColor: this.colors[0],
                        backgroundColor: this.fillArea ? this._hexToRgba(this.colors[0], 0.1) : 'transparent',
                        fill: this.fillArea,
                        tension: this.smoothLines ? 0.4 : 0,
                        pointRadius: this.showPoints ? 4 : 0,
                        pointHoverRadius: 6,
                        borderWidth: 2,
                    }],
                };
            }
        },

        _hexToRgba: function (hex, alpha) {
            var r = parseInt(hex.slice(1, 3), 16);
            var g = parseInt(hex.slice(3, 5), 16);
            var b = parseInt(hex.slice(5, 7), 16);
            return 'rgba(' + r + ', ' + g + ', ' + b + ', ' + alpha + ')';
        },

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self._renderChart();
            });
        },

        _renderChart: function () {
            var ctx = this.$('.o_chart_canvas')[0];
            if (!ctx) return;
            
            ctx = ctx.getContext('2d');
            
            if (this.chart) {
                this.chart.destroy();
            }
            
            this.chart = new Chart(ctx, {
                type: 'line',
                data: this.chartData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {
                        mode: 'index',
                        intersect: false,
                    },
                    plugins: {
                        legend: {
                            display: this.showLegend,
                            position: 'top',
                        },
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    var value = context.raw;
                                    if (value === null) return context.dataset.label + ': No data';
                                    return context.dataset.label + ': ' + value.toLocaleString();
                                },
                            },
                        },
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: this.xField,
                            },
                            grid: {
                                display: false,
                            },
                        },
                        y: {
                            beginAtZero: true,
                            title: {
                                display: !!this.yAxisLabel,
                                text: this.yAxisLabel,
                            },
                        },
                    },
                },
            });
        },

        destroy: function () {
            if (this.chart) {
                this.chart.destroy();
            }
            this._super.apply(this, arguments);
        },
    });

    window.DashboardLineChart = LineChartWidget;
    return LineChartWidget;
});