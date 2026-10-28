/**
 * Dashboard Builder - Gauge Widget
 * 
 * Renders a gauge/speedometer chart.
 */

odoo.define('el_dashboard_builder.widgets.Gauge', function (require) {
    "use strict";

    var AbstractWidget = require('el_dashboard_builder.widgets.AbstractWidget');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var _t = core._t;
    var qweb = core.qweb;

    var GaugeWidget = AbstractWidget.extend({
        template: 'el_dashboard_builder.GaugeWidget',
        chart: null,

        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.model = options.config.model;
            this.field = options.config.field;
            this.aggregation = options.config.aggregation || 'avg';
            this.domain = options.config.domain || [];
            this.minValue = options.config.min_value || 0;
            this.maxValue = options.config.max_value || 100;
            this.label = options.config.label || 'Value';
            this.suffix = options.config.suffix || '';
            this.precision = options.config.precision || 1;
            this.zones = options.config.zones || [
                { from: 0, to: 50, color: '#e74c3c', label: 'Low' },
                { from: 50, to: 80, color: '#f39c12', label: 'Medium' },
                { from: 80, to: 100, color: '#2ecc71', label: 'High' },
            ];
            this.showNeedle = options.config.show_needle !== false;
            this.showTicks = options.config.show_ticks !== false;
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
                args: [domain, [this.field + ':' + this.aggregation], []],
                kwargs: { lazy: false },
            }).then(function (result) {
                var key = self.field + ':' + self.aggregation;
                self.currentValue = result.length > 0 ? (result[0][key] || 0) : 0;
            });
        },

        _formatValue: function (value) {
            return value.toFixed(this.precision) + this.suffix;
        },

        _getZoneForValue: function (value) {
            for (var i = 0; i < this.zones.length; i++) {
                var zone = this.zones[i];
                if (value >= zone.from && value <= zone.to) {
                    return zone;
                }
            }
            return this.zones[this.zones.length - 1];
        },

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self._renderGauge();
            });
        },

        _renderGauge: function () {
            var $canvas = this.$('.o_gauge_canvas')[0];
            if (!$canvas) return;
            
            var ctx = $canvas.getContext('2d');
            var width = $canvas.width = $canvas.offsetWidth;
            var height = $canvas.height = $canvas.offsetHeight;
            var centerX = width / 2;
            var centerY = height * 0.85;
            var radius = Math.min(width, height) * 0.4;
            
            // Clear canvas
            ctx.clearRect(0, 0, width, height);
            
            // Draw zones (arcs)
            var startAngle = -Math.PI;
            var endAngle = 0;
            var totalRange = this.maxValue - this.minValue;
            
            this.zones.forEach(function (zone) {
                var zoneStart = startAngle + ((zone.from - this.minValue) / totalRange) * Math.PI;
                var zoneEnd = startAngle + ((zone.to - this.minValue) / totalRange) * Math.PI;
                
                ctx.beginPath();
                ctx.arc(centerX, centerY, radius, zoneStart, zoneEnd);
                ctx.lineWidth = radius * 0.15;
                ctx.strokeStyle = zone.color;
                ctx.lineCap = 'round';
                ctx.stroke();
            }.bind(this));
            
            // Draw ticks
            if (this.showTicks) {
                var tickCount = 10;
                for (var i = 0; i <= tickCount; i++) {
                    var value = this.minValue + (i / tickCount) * totalRange;
                    var angle = startAngle + (i / tickCount) * Math.PI;
                    
                    var tickLength = radius * 0.1;
                    var tickX1 = centerX + Math.cos(angle) * (radius - tickLength);
                    var tickY1 = centerY + Math.sin(angle) * (radius - tickLength);
                    var tickX2 = centerX + Math.cos(angle) * radius;
                    var tickY2 = centerY + Math.sin(angle) * radius;
                    
                    ctx.beginPath();
                    ctx.moveTo(tickX1, tickY1);
                    ctx.lineTo(tickX2, tickY2);
                    ctx.lineWidth = 2;
                    ctx.strokeStyle = '#666';
                    ctx.stroke();
                    
                    // Tick labels
                    if (i % 2 === 0) {
                        var labelX = centerX + Math.cos(angle) * (radius + 20);
                        var labelY = centerY + Math.sin(angle) * (radius + 20);
                        ctx.font = '12px Arial';
                        ctx.fillStyle = '#666';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.fillText(value.toFixed(0), labelX, labelY);
                    }
                }
            }
            
            // Draw needle
            if (this.showNeedle) {
                var valueRatio = (this.currentValue - this.minValue) / totalRange;
                valueRatio = Math.max(0, Math.min(1, valueRatio));
                var needleAngle = startAngle + valueRatio * Math.PI;
                
                var needleLength = radius * 0.85;
                var needleX = centerX + Math.cos(needleAngle) * needleLength;
                var needleY = centerY + Math.sin(needleAngle) * needleLength;
                
                ctx.beginPath();
                ctx.moveTo(centerX, centerY);
                ctx.lineTo(needleX, needleY);
                ctx.lineWidth = 3;
                ctx.strokeStyle = '#333';
                ctx.lineCap = 'round';
                ctx.stroke();
                
                // Needle center
                ctx.beginPath();
                ctx.arc(centerX, centerY, 8, 0, 2 * Math.PI);
                ctx.fillStyle = '#333';
                ctx.fill();
            }
            
            // Update value display
            this.$('.o_gauge_value').text(this._formatValue(this.currentValue));
            this.$('.o_gauge_label').text(this.label);
            
            // Update zone indicator
            var zone = this._getZoneForValue(this.currentValue);
            this.$('.o_gauge_zone').text(zone.label).css('color', zone.color);
        },
    });

    window.DashboardGauge = GaugeWidget;
    return GaugeWidget;
});