# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ebook_serial_mail_template_id = fields.Many2one(
        related='company_id.ebook_serial_mail_template_id',
        readonly=False,
    )

    def action_open_ebook_serial_mail_template(self):
        self.ensure_one()
        template = self.company_id._get_ebook_serial_mail_template()
        return {
            'name': self.env._("eBook Serial Email"),
            'type': 'ir.actions.act_window',
            'res_model': 'mail.template',
            'view_mode': 'form',
            'res_id': template.id if template else False,
        }
