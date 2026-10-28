/**
 * Dashboard Builder - Action Buttons Widget
 * 
 * Renders quick action buttons for common operations.
 */

odoo.define('el_dashboard_builder.widgets.ActionButtons', function (require) {
    "use strict";

    var AbstractWidget = require('el_dashboard_builder.widgets.AbstractWidget');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var _t = core._t;
    var qweb = core.qweb;

    var ActionButtonsWidget = AbstractWidget.extend({
        template: 'el_dashboard_builder.ActionButtonsWidget',
        events: {
            'click [data-action]': '_onActionClick',
        },

        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.buttons = options.config.buttons || [];
        },

        willStart: function () {
            return this._super.apply(this, arguments);
        },

        _onActionClick: function (ev) {
            var $btn = $(ev.currentTarget);
            var actionIndex = parseInt($btn.data('action-index'));
            var button = this.buttons[actionIndex];
            
            if (!button) return;
            
            switch (button.action_type) {
                case 'create':
                    this._actionCreate(button);
                    break;
                case 'open_view':
                    this._actionOpenView(button);
                    break;
                case 'server_action':
                    this._actionServerAction(button);
                    break;
                case 'url':
                    this._actionUrl(button);
                    break;
                case 'client_action':
                    this._actionClientAction(button);
                    break;
            }
        },

        _actionCreate: function (button) {
            var context = Object.assign({}, this.globalContext, button.context || {});
            this.do_action({
                type: 'ir.actions.act_window',
                res_model: button.model,
                view_mode: 'form',
                view_type: 'form',
                target: button.target || 'current',
                context: context,
            });
        },

        _actionOpenView: function (button) {
            var domain = button.domain || [];
            var context = Object.assign({}, this.globalContext, button.context || {});
            
            if (button.view_id) {
                this.do_action({
                    type: 'ir.actions.act_window',
                    res_model: button.model,
                    view_mode: 'list,form',
                    views: [[false, 'list'], [false, 'form']],
                    view_id: button.view_id,
                    domain: domain,
                    context: context,
                    target: button.target || 'current',
                });
            } else {
                this.do_action({
                    type: 'ir.actions.act_window',
                    res_model: button.model,
                    view_mode: 'list,form',
                    domain: domain,
                    context: context,
                    target: button.target || 'current',
                });
            }
        },

        _actionServerAction: function (button) {
            if (button.action_id) {
                this.do_action(button.action_id, {
                    context: this.globalContext,
                });
            }
        },

        _actionUrl: function (button) {
            if (button.url) {
                var url = button.url;
                // Replace variables
                Object.keys(this.globalContext).forEach(function (key) {
                    url = url.replace(new RegExp('{{' + key + '}}', 'g'), this.globalContext[key]);
                }.bind(this));
                
                if (button.target === 'blank') {
                    window.open(url, '_blank');
                } else if (button.target === 'modal') {
                    // Open in modal iframe
                    this._openInModal(url);
                } else {
                    window.location.href = url;
                }
            }
        },

        _actionClientAction: function (button) {
            if (button.action_id) {
                this.do_action(button.action_id);
            }
        },

        _openInModal: function (url) {
            var $modal = $('<div class="modal fade" tabindex="-1"><div class="modal-dialog modal-xl modal-dialog-scrollable"><div class="modal-content"><iframe src="' + url + '" style="width:100%;height:80vh;border:none;"></iframe></div></div></div>');
            $modal.modal('show');
            $modal.on('hidden.bs.modal', function () {
                $modal.remove();
            });
        },

        start: function () {
            return this._super.apply(this, arguments);
        },
    });

    window.DashboardActionButtons = ActionButtonsWidget;
    return ActionButtonsWidget;
});