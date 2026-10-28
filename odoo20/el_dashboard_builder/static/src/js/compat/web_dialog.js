/**
 * web.Dialog - Compatibility module for Odoo 20
 */

odoo.define('web.Dialog', ['web.core'], function (require) {
    "use strict";
    
    var core = require('web.core');
    
    // Get Component, with fallback
    var Component = core.Component;
    if (!Component) {
        console.warn('web.Dialog: owl.Component not available yet, using fallback');
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
    
    var Dialog = {
        confirm: function (parent, message, options) {
            if (window.confirm(message)) {
                if (options && options.confirm_callback) {
                    options.confirm_callback();
                }
            }
        },
        
        alert: function (parent, message, options) {
            window.alert(message);
        },
    };
    
    Dialog.extend = function (props) {
        var DialogClass = Component.extend(props);
        return DialogClass;
    };
    
    return Dialog;
});