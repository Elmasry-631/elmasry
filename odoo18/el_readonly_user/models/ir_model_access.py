# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.exceptions import AccessError


_READONLY_WRITABLE_MODELS = {
    'res.users.log', 'mail.channel', 'mail.alias',
    'bus.presence', 'res.lang', 'mail.channel.member',
    'bus.bus', 'mail.message', 'mail.followers',
}


class IrModelAccess(models.Model):
    """Enforce readonly permissions while preserving read access."""

    _inherit = 'ir.model.access'

    @api.model
    def check(self, model_name, mode='read', raise_exception=True):
        is_readonly = self.env.user.has_group(
            'el_readonly_user.group_users_readonly')
        if not is_readonly:
            return super().check(model_name, mode=mode, raise_exception=raise_exception)

        if mode == 'read':
            return True

        # Stock forms may perform ACL-level write checks even when the user is
        # only opening a record. Allow the ACL check for stock form models;
        # actual writes are still denied by ir.rule._compute_domain().
        if model_name in _READONLY_WRITABLE_MODELS or model_name in {
                'stock.picking', 'stock.move', 'stock.move.line',
                'stock.quant', 'stock.scrap', 'stock.valuation.layer'}:
            return super().check(model_name, mode=mode, raise_exception=raise_exception)

        if raise_exception:
            raise AccessError(
                _("Readonly access: %(mode)s on %(model)s is not allowed.",
                  mode=mode, model=model_name))
        return False
