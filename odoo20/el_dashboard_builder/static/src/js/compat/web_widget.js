/**
 * web.Widget - Compatibility module for Odoo 20
 */

odoo.define('web.Widget', ['web.core'], function (require) {
    "use strict";
    
    var core = require('web.core');
    
    // Get Component, with fallback
    var Component = core.Component;
    if (!Component) {
        console.warn('web.Widget: owl.Component not available yet, using fallback');
        // Create a minimal Component-like class
        Component = function () {};
        Component.extend = function (props) {
            var Child = function () {
                this._super = function () {};
                if (props.init) props.init.apply(this, arguments);
            };
            Child.prototype = Object.create(this.prototype);
            for (var key in props) {
                if (key !== 'init') Child.prototype[key] = props[key];
            }
            Child.extend = this.extend;
            return Child;
        };
    }
    
    var Widget = Component.extend({
        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.options = options || {};
        },
        
        willStart: function () {
            return this._super.apply(this, arguments);
        },
        
        start: function () {
            return this._super.apply(this, arguments);
        },
        
        destroy: function () {
            this._super.apply(this, arguments);
        },
        
        $: function (selector) {
            return this.$el.find(selector);
        },
    });
    
    return Widget;
});