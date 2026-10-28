/**
 * Dashboard Builder - Abstract Widget Base Class
 * 
 * Base class for all dashboard widgets providing common functionality.
 */

odoo.define('el_dashboard_builder.widgets.AbstractWidget', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var _t = core._t;
    var qweb = core.qweb;

    var AbstractWidget = Widget.extend({
        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.data = options.data || {};
            this.config = options.config || {};
            this.meta = options.meta || {};
            this.globalFilters = options.globalFilters || [];
            this.globalContext = options.globalContext || {};
            this.loading = true;
            this.error = null;
        },

        willStart: function () {
            return this._super.apply(this, arguments);
        },

        start: function () {
            this.loading = false;
            this.$el.addClass('o_widget_loaded');
            return this._super.apply(this, arguments);
        },

        _showLoading: function () {
            this.loading = true;
            this.$('.o_widget_content').hide();
            this.$('.o_widget_loading').show();
        },

        _hideLoading: function () {
            this.loading = false;
            this.$('.o_widget_loading').hide();
            this.$('.o_widget_content').show();
        },

        _showError: function (message) {
            this.error = message;
            this.loading = false;
            this.$('.o_widget_loading').hide();
            this.$('.o_widget_content').hide();
            this.$('.o_widget_error').show().find('.o_error_message').text(message);
        },

        _retry: function () {
            this._showLoading();
            this.$('.o_widget_error').hide();
            this._fetchData().then(function () {
                this._hideLoading();
                this._render();
            }.bind(this)).catch(function (error) {
                this._showError(error.message || _t('Failed to load widget data'));
            }.bind(this));
        },

        _fetchData: function () {
            // Override in subclasses
            return Promise.resolve();
        },

        _render: function () {
            // Override in subclasses
        },

        _formatNumber: function (value, options) {
            options = options || {};
            var precision = options.precision || 0;
            var prefix = options.prefix || '';
            var suffix = options.suffix || '';
            
            if (value === null || value === undefined) return '—';
            
            var formatted = Number(value).toLocaleString(undefined, {
                minimumFractionDigits: precision,
                maximumFractionDigits: precision,
            });
            
            return prefix + formatted + suffix;
        },

        _formatCurrency: function (value, currency) {
            if (value === null || value === undefined) return '—';
            
            var fmt = new Intl.NumberFormat(undefined, {
                style: 'currency',
                currency: currency || 'USD',
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
            });
            
            return fmt.format(value);
        },

        _formatDate: function (value, format) {
            if (!value) return '—';
            
            var date = new Date(value);
            if (isNaN(date.getTime())) return value;
            
            var options = { year: 'numeric', month: 'short', day: 'numeric' };
            if (format === 'datetime') {
                options.hour = '2-digit';
                options.minute = '2-digit';
            }
            
            return date.toLocaleDateString(undefined, options);
        },

        _getColorForValue: function (value, thresholds) {
            if (!thresholds || !thresholds.length) return '';
            
            for (var i = thresholds.length - 1; i >= 0; i--) {
                if (value >= thresholds[i].value) {
                    return thresholds[i].color;
                }
            }
            return '';
        },

        _applyFilters: function (domain) {
            if (this.globalFilters) {
                return domain.concat(this.globalFilters);
            }
            return domain;
        },

        _applyContext: function (context) {
            return Object.assign({}, this.globalContext, context || {});
        },
    });

    return AbstractWidget;
});