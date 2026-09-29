# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    def _default_ebook_serial_mail_template(self):
        return self.env.ref('ebook_serial_delivery.mail_template_ebook_serial', raise_if_not_found=False)

    ebook_serial_mail_template_id = fields.Many2one(
        'mail.template',
        string="eBook Serial Email",
        domain="[('model', '=', 'sale.order')]",
        default=_default_ebook_serial_mail_template,
        help="Email sent to the customer with the serial numbers when an eBook delivery is done.",
    )

    def _get_ebook_serial_mail_template(self):
        """Template chosen in Inventory settings, or the module's default one."""
        self.ensure_one()
        return self.ebook_serial_mail_template_id or self._default_ebook_serial_mail_template()
