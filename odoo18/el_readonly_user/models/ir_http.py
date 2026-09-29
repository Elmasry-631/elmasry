# -*- coding: utf-8 -*-
from odoo import models

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        res = super().session_info()
        res['is_readonly_user'] = self.env.user.has_group(
            'el_readonly_user.group_users_readonly')
        # also expose group id for JS fallback
        return res
