/**
 * Dashboard Builder - Pie/Donut Chart Widget
 * 
 * Renders pie and doughnut charts for proportional data.
 */

odoo.define('el_dashboard_builder.widgets.PieChart', function (require) {
    "use strict";

    var AbstractWidget = require('el_dashboard_builder.widgets.AbstractWidget');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var _t = core._t;
    var qweb = core.qweb;

    var PieChartWidget = AbstractWidget.extend({
        template: 'el_dashboard_builder.PieChartWidget',
        chart: null,

        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.model = options.config.model;
            this.labelField = options.config.label_field;
            this.valueField = options.config.value_field;
            this.aggregation = options.config.aggregation || 'sum';
            this.domain = options.config.domain || [];
            this.chartType = options.config.chart_type || 'doughnut';
            this.showLegend = options.config.show_legend !== false;
            this.legendPosition = options.config.legend_position || 'right';
            this.showDataLabels = options.config.show_data_labels !== false;
            this.labelFormat = options.config.label_format || 'percentage';
            this.colors = options.config.colors || [
                '#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6',
                '#1abc9c', '#e67e22', '#34495e', '#16a085', '#c0392b',
                '#27ae60', '#8e44ad', '#2c3e50', '#d35400', '#7f8c8d'
            ];
            this.limit = options.config.limit || 10;
            this.groupOthers = options.config.group_others !== false;
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

            return rpc.query({
                model: this.model,
                method: 'read_group',
                args: [domain, [this.valueField + ':' + this.aggregation], [this.labelField]],
                kwargs: {
                    lazy: false,
                    limit: this.limit + 1, // +1 to detect if there are more
                },
            }).then(function (result) {
                self._processChartData(result);
            });
        },

        _processChartData: function (groups) {
            var self = this;
            
            // Sort by value descending
            groups.sort(function (a, b) {
                var valA = a[self.valueField + ':' + self.aggregation] || 0;
                var valB = b[self.valueField + ':' + self.aggregation] || 0;
                return valB - valA;
            });
            
            var labels = [];
            var data = [];
            var total = 0;
            
            groups.forEach(function (g) {
                var label = g[self.labelField];
                if (Array.isArray(label)) label = label[1];
                var value = g[self.valueField + ':' + self.aggregation] || 0;
                
                labels.push(label);
                data.push(value);
                total += value;
            });
            
            // Group others if enabled and over limit
            if (this.groupOthers && labels.length > this.limit) {
                var othersData = data.slice(this.limit);
                var othersSum = othersData.reduce(function (a, b) { return a + b; }, 0);
                
                labels = labels.slice(0, this.limit - 1);
                data = data.slice(0, this.limit - 1);
                
                labels.push(_t('Others'));
                data.push(othersSum);
            } else if (labels.length > this.limit) {
                labels = labels.slice(0, this.limit);
                data = data.slice(0, this.limit);
            }
            
            // Calculate percentages
            var percentages = data.map(function (v) {
                return total > 0 ? ((v / total) * 100).toFixed(1) : 0;
            });
            
            this.chartData = {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: this.colors.slice(0, labels.length),
                    borderWidth: 2,
                    borderColor: '#fff',
                }],
            };
            
            this.total = total;
            this.percentages = percentages;
        },

        _getTooltipLabel: function (context) {
            var value = context.raw;
            var percentage = this.percentages[context.dataIndex] || 0;
            
            switch (this.labelFormat) {
                case 'value':
                    return context.label + ': ' + value.toLocaleString();
                case 'percentage':
                    return context.label + ': ' + percentage + '%';
                case 'both':
                default:
                    return context.label + ': ' + value.toLocaleString() + ' (' + percentage + '%)';
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
            
            this.chart = new Chart(ctx, {
                type: this.chartType,
                data: this.chartData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: this.showLegend,
                            position: this.legendPosition,
                        },
                        tooltip: {
                            callbacks: {
                                label: this._getTooltipLabel.bind(this),
                            },
                        },
                        datalabels: {
                            display: this.showDataLabels,
                            color: '#fff',
                            font: {
                                weight: 'bold',
                                size: 12,
                            },
                            formatter: function (value, context) {
                                var percentage = context.chart.data.percentages[context.dataIndex] || 0;
                                switch (context.chart.data.labelFormat) {
                                    case 'value':
                                        return value.toLocaleString();
                                    case 'percentage':
                                        return percentage + '%';
                                    case 'both':
                                    default:
                                        return percentage + '%';
                                }
                            },
                        },
                    },
                    cutout: this.chartType === 'doughnut' ? '60%' : 0,
                },
                plugins: [ChartDataLabels],
            });
            
            // Store labelFormat for plugin
            this.chart.data.labelFormat = this.labelFormat;
            this.chart.data.percentages = this.percentages;
        },

        destroy: function () {
            if (this.chart) {
                this.chart.destroy();
            }
            this._super.apply(this, arguments);
        },
    });

    window.DashboardPieChart = PieChartWidget;
    return PieChartWidget;
});