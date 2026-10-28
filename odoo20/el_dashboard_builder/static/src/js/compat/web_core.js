/**
 * web.core - Compatibility module for Odoo 20
 */

odoo.define('web.core', [], function (require) {
    "use strict";
    
    // Try to get owl.Component from various sources
    var getOwlComponent = function () {
        // Try global owl first
        if (typeof owl !== 'undefined' && owl.Component) {
            return owl.Component;
        }
        // Try window.owl
        if (typeof window !== 'undefined' && window.owl && window.owl.Component) {
            return window.owl.Component;
        }
        // Try globalThis
        if (typeof globalThis !== 'undefined' && globalThis.owl && globalThis.owl.Component) {
            return globalThis.owl.Component;
        }
        // Try to get from module system if available
        if (typeof require !== 'undefined') {
            try {
                var owlModule = require('@odoo/owl');
                if (owlModule && owlModule.Component) {
                    return owlModule.Component;
                }
            } catch (e) {
                // ignore
            }
        }
        return null;
    };
    
    var core = {
        _t: function (text) {
            return text;
        },
        
        qweb: {
            render: function (template, values) {
                console.warn('qweb.render called in compat shim, template:', template);
                return '';
            },
            add_template: function (templates) {
            }
        },
        
        bus: {
            on: function () {},
            off: function () {},
            trigger: function () {},
        },
        
        Class: function () {
            return function () {};
        },
        
        _Component: null,
        get Component() {
            if (!this._Component) {
                this._Component = getOwlComponent();
            }
            return this._Component;
        },
    };
    
    return core;
});