/**
 * Dashboard Builder - KPI Card Widget
 * 
 * Displays a single key metric with trend and target.
 */

odoo.define('el_dashboard_builder.widgets.KpiCard', function (require) {
    "use strict";

    var AbstractWidget = require('el_dashboard_builder.widgets.AbstractWidget');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var _t = core._t;
    var qweb = core.qweb;

    var KpiCardWidget = AbstractWidget.extend({
        template: 'el_dashboard_builder.KpiCardWidget',
        events: {
            'click [data-action="drill-down"]': '_onDrillDownClick',
        },

        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.model = options.config.model;
            this.field = options.config.field;
            this.aggregation = options.config.aggregation || 'sum';
            this.domain = options.config.domain || [];
            this.label = options.config.label || 'Value';
            this.prefix = options.config.prefix || '';
            this.suffix = options.config.suffix || '';
            this.precision = options.config.precision || 0;
            this.trendField = options.config.trend_field;
            this.trendType = options.config.trend_type || 'percentage';
            this.targetValue = options.config.target_value;
            this.targetLabel = options.config.target_label || 'Target';
            this.colorThresholds = options.config.color_thresholds || [];
        },

        willStart: function () {
            return this._super.apply(this, arguments).then(function () {
                return this._fetchData();
            }.bind(this));
        },

        _fetchData: function () {
            var self = this;
            var domain = this.domain.slice();
            
            // Add global filters if any
            if (this.globalFilters) {
                domain = domain.concat(this.globalFilters);
            }

            var params = {
                model: this.model,
                method: 'web_search_read',
                args: [[], [this.field]],
                kwargs: {
                    domain: domain,
                    limit: 1,
                },
            };

            // For aggregation, we need read_group
            if (this.aggregation !== 'count') {
                params = {
                    model: this.model,
                    method: 'read_group',
                    args: [domain, [this.field + ':' + this.aggregation], []],
                    kwargs: { lazy: false },
                };
            }

            return rpc.query(params).then(function (result) {
                self.currentValue = self._extractValue(result);
                self.formattedValue = self._formatValue(self.currentValue);
                
                // Fetch trend if configured
                if (self.trendField) {
                    return self._fetchTrend().then(function (trendValue) {
                        self.trendValue = trendValue;
                        self.trendPercentage = self._calculateTrend(self.currentValue, trendValue);
                    });
                }
            });
        },

        _extractValue: function (result) {
            if (this.aggregation === 'count') {
                return result.length || 0;
            }
            
            if (Array.isArray(result) && result.length > 0) {
                var key = this.field + ':' + this.aggregation;
                return result[0][key] || 0;
            }
            
            return 0;
        },

        _fetchTrend: function () {
            // Fetch previous period value for trend comparison
            // This would need a date field in the domain
            var self = this;
            var domain = this.domain.slice();
            
            // Try to find a date field to filter previous period
            return rpc.query({
                model: this.model,
                method: 'search_read',
                args: [domain, [this.trendField]],
                kwargs: { limit: 1, order: this.trendField + ' desc' },
            }).then(function (records) {
                if (records.length > 0) {
                    return records[0][self.trendField] || 0;
                }
                return 0;
            });
        },

        _calculateTrend: function (current, previous) {
            if (previous === 0) return null;
            if (this.trendType === 'percentage') {
                return ((current - previous) / Math.abs(previous)) * 100;
            }
            return current - previous;
        },

        _formatValue: function (value) {
            if (value === null || value === undefined) return '—';
            
            var formatted = value.toLocaleString(undefined, {
                minimumFractionDigits: this.precision,
                maximumFractionDigits: this.precision,
            });
            
            return this.prefix + formatted + this.suffix;
        },

        _getValueColor: function () {
            if (!this.colorThresholds.length) return '';
            
            for (var i = this.colorThresholds.length - 1; i >= 0; i--) {
                var threshold = this.colorThresholds[i];
                if (this.currentValue >= threshold.value) {
                    return threshold.color;
                }
            }
            return '';
        },

        _getTrendIcon: function () {
            if (this.trendPercentage === null || this.trendPercentage === undefined) return '';
            if (this.trendPercentage > 0) return 'fa fa-arrow-up text-success';
            if (this.trendPercentage < 0) return 'fa fa-arrow-down text-danger';
            return 'fa fa-minus text-muted';
        },

        _getTrendText: function () {
            if (this.trendPercentage === null || this.trendPercentage === undefined) return '';
            
            var abs = Math.abs(this.trendPercentage);
            if (this.trendType === 'percentage') {
                return abs.toFixed(1) + '%';
            }
            return this._formatValue(abs);
        },

        _onDrillDownClick: function () {
            if (this.config.drill_down_action) {
                // Handle drill down action
                this.do_action(this.config.drill_down_action);
            } else if (this.model) {
                // Default: open list view of the model
                this.do_action({
                    type: 'ir.actions.act_window',
                    res_model: this.model,
                    view_mode: 'list,form',
                    domain: this.domain,
                });
            }
        },

        getWidgetData: function () {
            return {
                value: this.currentValue,
                formatted_value: this.formattedValue,
                label: this.label,
                trend: this.trendPercentage,
                trend_formatted: this._getTrendText(),
                trend_icon: this._getTrendIcon(),
                target: this.targetValue,
                target_label: this.targetLabel,
                target_progress: this.targetValue ? (this.currentValue / this.targetValue) * 100 : null,
                color: this._getValueColor(),
            };
        },
    });

    // Register widget component
    window.DashboardKpiCard = KpiCardWidget;
    return KpiCardWidget;
});