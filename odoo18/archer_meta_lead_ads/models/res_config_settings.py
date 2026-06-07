# -*- coding: utf-8 -*-

from odoo import models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def action_open_meta_lead_ads(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Meta Credentials'),
            'res_model': 'meta.app.credential',
            'view_mode': 'list,form',
        }
