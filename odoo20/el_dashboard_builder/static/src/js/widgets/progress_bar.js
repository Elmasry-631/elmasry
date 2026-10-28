/**
 * Dashboard Builder - Progress Bar Widget
 * 
 * Renders a progress bar for completion tracking.
 */

odoo.define('el_dashboard_builder.widgets.ProgressBar', function (require) {
    "use strict";

    var AbstractWidget = require('el_dashboard_builder.widgets.AbstractWidget');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var _t = core._t;
    var qweb = core.qweb;

    var ProgressBarWidget = AbstractWidget.extend({
        template: 'el_dashboard_builder.ProgressBarWidget',

        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.model = options.config.model;
            this.valueField = options.config.value_field;
            this.targetField = options.config.target_field;
            this.aggregation = options.config.aggregation || 'sum';
            this.domain = options.config.domain || [];
            this.label = options.config.label || 'Progress';
            this.showPercentage = options.config.show_percentage !== false;
            this.showValues = options.config.show_values !== false;
            this.color = options.config.color || '#3498db';
            this.backgroundColor = options.config.background_color || '#ecf0f1';
            this.height = options.config.height || 24;
            this.striped = options.config.striped || false;
            this.animated = options.config.animated || false;
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

            return Promise.all([
                rpc.query({
                    model: this.model,
                    method: 'read_group',
                    args: [domain, [this.valueField + ':' + this.aggregation], []],
                    kwargs: { lazy: false },
                }),
                rpc.query({
                    model: this.model,
                    method: 'read_group',
                    args: [domain, [this.targetField + ':' + this.aggregation], []],
                    kwargs: { lazy: false },
                }),
            ]).then(function (results) {
                var valueKey = self.valueField + ':' + self.aggregation;
                var targetKey = self.targetField + ':' + self.aggregation;
                
                self.currentValue = results[0].length > 0 ? (results[0][0][valueKey] || 0) : 0;
                self.targetValue = results[1].length > 0 ? (results[1][0][targetKey] || 0) : 0;
            });
        },

        _getPercentage: function () {
            if (!this.targetValue || this.targetValue === 0) return 0;
            return Math.min(100, (this.currentValue / this.targetValue) * 100);
        },

        _formatValue: function (value) {
            return value.toLocaleString();
        },

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self._renderProgress();
            });
        },

        _renderProgress: function () {
            var percentage = this._getPercentage();
            var $bar = this.$('.o_progress_bar');
            var $fill = this.$('.o_progress_fill');
            var $label = this.$('.o_progress_label');
            var $percentage = this.$('.o_progress_percentage');
            var $values = this.$('.o_progress_values');
            
            // Set styles
            $bar.css('height', this.height + 'px');
            $bar.css('background-color', this.backgroundColor);
            $fill.css('background-color', this.color);
            $fill.css('height', '100%');
            
            if (this.striped) $fill.addClass('progress-bar-striped');
            if (this.animated) $fill.addClass('progress-bar-animated');
            
            // Animate width
            setTimeout(function () {
                $fill.css('width', percentage + '%');
            }, 50);
            
            // Update labels
            if (this.showPercentage) {
                $percentage.text(percentage.toFixed(1) + '%').show();
            } else {
                $percentage.hide();
            }
            
            if (this.showValues) {
                $values.text(this._formatValue(this.currentValue) + ' / ' + this._formatValue(this.targetValue)).show();
            } else {
                $values.hide();
            }
            
            $label.text(this.label);
        },
    });

    window.DashboardProgressBar = ProgressBarWidget;
    return ProgressBarWidget;
});