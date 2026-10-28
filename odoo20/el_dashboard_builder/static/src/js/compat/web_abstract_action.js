/**
 * web.AbstractAction - Compatibility module for Odoo 20
 */

odoo.define('web.AbstractAction', ['web.core'], function (require) {
    "use strict";
    
    var core = require('web.core');
    
    // Get Component, with fallback
    var Component = core.Component;
    if (!Component) {
        console.warn('web.AbstractAction: owl.Component not available yet, using fallback');
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
    
    var AbstractAction = Component.extend({
        init: function (parent, params) {
            this._super.apply(this, arguments);
            this.params = params || {};
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
    });
    
    return AbstractAction;
});