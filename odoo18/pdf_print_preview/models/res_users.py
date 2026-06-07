# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    preview_print = fields.Boolean(
        string="Preview print",
        default=True
    )

    automatic_printing = fields.Boolean(
        string="Automatic printing"
    )

    def preview_reload(self):
        return {
            "type": "ir.actions.client",
            "tag": "reload"
        }

    def preview_print_save(self):
        """
        دالة مخصصة لحفظ الإعدادات من النافذة المنبثقة.
        تضمن أننا نقوم بتحديث السجل الحالي فقط وتجنب أي عمليات إنشاء جانبية.
        """
        self.ensure_one()
        # الحفظ يتم تلقائياً عند الضغط على زر من نوع object في الفورم
        # ولكن سنقوم بعمل reload_context لتحديث الجلسة في المتصفح
        return {
            "type": "ir.actions.client",
            "tag": "reload_context"
        }

    @api.model
    def _get_self_readable_fields(self):
        return super()._get_self_readable_fields() | {"preview_print", "automatic_printing"}

    @api.model
    def _get_self_writeable_fields(self):
        return super()._get_self_writeable_fields() | {"preview_print", "automatic_printing"}
