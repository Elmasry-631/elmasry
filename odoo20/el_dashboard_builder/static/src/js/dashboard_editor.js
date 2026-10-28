/**
 * Dashboard Builder - Editor JavaScript Module
 * 
 * Additional editor-specific functionality.
 */

odoo.define('el_dashboard_builder.DashboardEditorWidgets', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var qweb = core.qweb;

    // Widget Palette Item Component
    var WidgetPaletteItem = Widget.extend({
        template: 'el_dashboard_builder.WidgetPaletteItem',
        events: {
            'click': '_onClick',
        },

        init: function (parent, widgetData) {
            this._super.apply(this, arguments);
            this.widgetData = widgetData;
        },

        _onClick: function () {
            this.trigger_up('widget_selected', this.widgetData);
        },
    });

    // Widget Configuration Form Component
    var WidgetConfigForm = Widget.extend({
        template: 'el_dashboard_builder.WidgetConfigForm',
        events: {
            'change input, select, textarea': '_onFieldChange',
            'click [data-action="reset"]': '_onResetClick',
        },

        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.schema = options.schema || {};
            this.config = options.config || {};
            this.fields = {};
        },

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self._renderFields();
            });
        },

        _renderFields: function () {
            var $container = this.$('.o_config_fields');
            var html = '';
            
            var properties = this.schema.properties || {};
            Object.keys(properties).forEach(function (key) {
                var prop = properties[key];
                html += self._renderField(key, prop);
            });
            
            $container.html(html);
            this._bindFieldEvents();
        },

        _renderField: function (key, prop) {
            var value = this.config[key] !== undefined ? this.config[key] : prop.default;
            var required = (this.schema.required || []).includes(key) ? ' required' : '';
            var label = prop.title || key;
            var help = prop.description ? '<small class="form-text text-muted">' + prop.description + '</small>' : '';
            
            var html = '<div class="mb-3">';
            html += '<label class="form-label">' + label + required + '</label>';
            
            switch (prop.type) {
                case 'string':
                    if (prop.format === 'textarea') {
                        html += '<textarea class="form-control" name="' + key + '"' + required + '>' + (value || '') + '</textarea>';
                    } else if (prop.enum) {
                        html += '<select class="form-select" name="' + key + '"' + required + '>';
                        html += '<option value="">Select...</option>';
                        prop.enum.forEach(function (opt) {
                            var selected = value === opt ? ' selected' : '';
                            html += '<option value="' + opt + '"' + selected + '>' + opt + '</option>';
                        });
                        html += '</select>';
                    } else {
                        html += '<input type="text" class="form-control" name="' + key + '" value="' + (value || '') + '"' + required + '>';
                    }
                    break;
                case 'integer':
                case 'number':
                    html += '<input type="number" class="form-control" name="' + key + '" value="' + (value || '') + '"' + required + ' step="' + (prop.type === 'integer' ? '1' : 'any') + '">';
                    break;
                case 'boolean':
                    html += '<div class="form-check form-switch">';
                    html += '<input class="form-check-input" type="checkbox" name="' + key + '"' + (value ? ' checked' : '') + '>';
                    html += '<label class="form-check-label">' + label + '</label>';
                    html += '</div>';
                    break;
                case 'array':
                    html += '<div class="o_json_field" data-field="' + key + '">';
                    html += '<textarea class="form-control font-monospace small" rows="4" name="' + key + '">' + JSON.stringify(value || [], null, 2) + '</textarea>';
                    html += '<small class="form-text text-muted">JSON Array</small>';
                    html += '</div>';
                    break;
                case 'object':
                    html += '<div class="o_json_field" data-field="' + key + '">';
                    html += '<textarea class="form-control font-monospace small" rows="6" name="' + key + '">' + JSON.stringify(value || {}, null, 2) + '</textarea>';
                    html += '<small class="form-text text-muted">JSON Object</small>';
                    html += '</div>';
                    break;
            }
            
            html += help;
            html += '</div>';
            
            return html;
        },

        _bindFieldEvents: function () {
            var self = this;
            this.$('[name]').each(function () {
                var $field = $(this);
                var name = $field.attr('name');
                self.fields[name] = $field;
            });
        },

        _onFieldChange: function (ev) {
            var $field = $(ev.currentTarget);
            var name = $field.attr('name');
            var value = this._parseFieldValue($field);
            this.config[name] = value;
            this.trigger_up('config_changed', { config: this.config });
        },

        _parseFieldValue: function ($field) {
            var name = $field.attr('name');
            var prop = (this.schema.properties || {})[name];
            
            if ($field.is('input[type="checkbox"]')) {
                return $field.is(':checked');
            }
            
            if ($field.is('select')) {
                var val = $field.val();
                if (prop && prop.type === 'integer') return parseInt(val) || 0;
                if (prop && prop.type === 'number') return parseFloat(val) || 0;
                return val;
            }
            
            if ($field.is('input[type="number"]')) {
                if (prop && prop.type === 'integer') return parseInt($field.val()) || 0;
                return parseFloat($field.val()) || 0;
            }
            
            if ($field.is('.o_json_field textarea')) {
                try {
                    return JSON.parse($field.val() || '{}');
                } catch (e) {
                    return prop && prop.type === 'array' ? [] : {};
                }
            }
            
            return $field.val();
        },

        _onResetClick: function () {
            this.config = {};
            this._renderFields();
            this.trigger_up('config_changed', { config: this.config });
        },

        getConfig: function () {
            return this.config;
        },
    });

    // Dashboard Grid Overlay
    var GridOverlay = Widget.extend({
        template: 'el_dashboard_builder.GridOverlay',
        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.columns = options.columns || 12;
            this.cellHeight = options.cellHeight || 100;
        },

        start: function () {
            this._renderGridLines();
            return this._super.apply(this, arguments);
        },

        _renderGridLines: function () {
            var $lines = this.$('.grid-lines');
            var html = '';
            
            for (var i = 0; i <= this.columns; i++) {
                html += '<div class="grid-line vertical" style="left: ' + (i * (100 / this.columns)) + '%"></div>';
            }
            
            var rows = 20; // Max visible rows
            for (var j = 0; j <= rows; j++) {
                html += '<div class="grid-line horizontal" style="top: ' + (j * this.cellHeight) + 'px"></div>';
            }
            
            $lines.html(html);
        },
    });

    return {
        WidgetPaletteItem: WidgetPaletteItem,
        WidgetConfigForm: WidgetConfigForm,
        GridOverlay: GridOverlay,
    };
});