/**
 * Dashboard Builder - Bar Chart Widget
 * 
 * Renders bar/column charts using Chart.js
 */

odoo.define('el_dashboard_builder.widgets.BarChart', function (require) {
    "use strict";

    var AbstractWidget = require('el_dashboard_builder.widgets.AbstractWidget');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var _t = core._t;
    var qweb = core.qweb;

    var BarChartWidget = AbstractWidget.extend({
        template: 'el_dashboard_builder.BarChartWidget',
        chart: null,

        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.model = options.config.model;
            this.xField = options.config.x_field;
            this.yField = options.config.y_field;
            this.aggregation = options.config.aggregation || 'sum';
            this.domain = options.config.domain || [];
            this.orientation = options.config.orientation || 'vertical';
            this.stacked = options.config.stacked || false;
            this.groupBy = options.config.group_by;
            this.colors = options.config.colors || [
                '#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6',
                '#1abc9c', '#e67e22', '#34495e', '#16a085', '#c0392b'
            ];
            this.showLegend = options.config.show_legend !== false;
            this.showDataLabels = options.config.show_data_labels || false;
            this.yAxisLabel = options.config.y_axis_label;
            this.xAxisLabel = options.config.x_axis_label;
            this.limit = options.config.limit || 20;
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

            var fields = [this.xField, this.yField];
            if (this.groupBy) {
                fields.push(this.groupBy);
            }

            var groupBy = [this.xField];
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
                // Grouped bar chart
                var series = {};
                var labelsSet = new Set();
                
                groups.forEach(function (g) {
                    var label = g[self.xField];
                    var seriesKey = g[self.groupBy];
                    
                    if (Array.isArray(label)) label = label[1]; // many2one
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
                        return series[key][label] || 0;
                    });
                    return {
                        label: key,
                        data: data,
                        backgroundColor: self.colors[index % self.colors.length],
                        borderColor: self.colors[index % self.colors.length],
                        borderWidth: 1,
                    };
                });
                
                this.chartData = {
                    labels: labels,
                    datasets: datasets,
                };
            } else {
                // Simple bar chart
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
                        backgroundColor: this.colors[0],
                        borderColor: this.colors[0],
                        borderWidth: 1,
                    }],
                };
            }
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
            
            var isHorizontal = this.orientation === 'horizontal';
            
            this.chart = new Chart(ctx, {
                type: 'bar',
                data: this.chartData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    indexAxis: isHorizontal ? 'y' : 'x',
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
                                    return context.dataset.label + ': ' + value.toLocaleString();
                                },
                            },
                        },
                        datalabels: {
                            display: this.showDataLabels,
                            color: '#333',
                            font: {
                                weight: 'bold',
                            },
                            formatter: function (value) {
                                return value.toLocaleString();
                            },
                        },
                    },
                    scales: {
                        x: {
                            stacked: this.stacked,
                            title: {
                                display: !!this.xAxisLabel,
                                text: this.xAxisLabel,
                            },
                            grid: {
                                display: isHorizontal,
                            },
                        },
                        y: {
                            stacked: this.stacked,
                            beginAtZero: true,
                            title: {
                                display: !!this.yAxisLabel,
                                text: this.yAxisLabel,
                            },
                            grid: {
                                display: !isHorizontal,
                            },
                        },
                    },
                },
                plugins: [ChartDataLabels],
            });
        },

        destroy: function () {
            if (this.chart) {
                this.chart.destroy();
            }
            this._super.apply(this, arguments);
        },
    });

    window.DashboardBarChart = BarChartWidget;
    return BarChartWidget;
});