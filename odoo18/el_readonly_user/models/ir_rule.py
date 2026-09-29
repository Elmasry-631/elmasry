# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.osv import expression


_READONLY_RULE_WRITABLE = {
    'res.users.log', 'mail.channel', 'mail.alias',
    'bus.presence', 'res.lang', 'mail.channel.member',
    'bus.bus', 'mail.message', 'mail.followers',
}


class IrRule(models.Model):
    """Block write/create/unlink at record-rule level for readonly users."""

    _inherit = 'ir.rule'

    @api.model
    def _compute_domain(self, model_name, mode):
        res = super()._compute_domain(model_name, mode)
        if self.env.user.has_group(
                'el_readonly_user.group_users_readonly') \
                and model_name not in _READONLY_RULE_WRITABLE \
                and mode in ('write', 'create', 'unlink'):
            return expression.AND([res, expression.FALSE_DOMAIN])
        return res
