/**
 * web.session - Compatibility module for Odoo 20
 */

odoo.define('web.session', [], function (require) {
    "use strict";
    
    return odoo.session_info || {};
});