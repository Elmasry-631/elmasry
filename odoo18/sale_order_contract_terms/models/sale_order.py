# sale_order_contract_terms/models/sale_order.py
from odoo import models, fields,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    technical_specification_id = fields.Text(
        compute="_compute_technical_specification_id",
        store=True
    )

    @api.depends('order_line.product_id.technical_specification')
    def _compute_technical_specification_id(self):
        for order in self:
            specs = order.order_line.mapped(
                'product_id.product_tmpl_id.technical_specification'
            )
            # remove empty values and join
            order.technical_specification_id = '\n\n'.join(
                spec for spec in specs if spec
            )

    def get_date_arabic(self):
        self.ensure_one()
        # استخدم تاريخ الأمر إذا موجود، وإلا استخدم الآن
        if self.date_order:
            dt = fields.Datetime.to_datetime(self.date_order)
        else:
            dt = fields.Datetime.now()
        # حول للتوقيت المحلي للمستخدم إن أمكن
        try:
            dt = fields.Datetime.context_timestamp(self.env.user, dt)
        except Exception:
            pass

        weekdays = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
        months = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
                  "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
        try:
            weekday_str = weekdays[dt.weekday()]
            month_str = months[dt.month - 1]
            return f"{weekday_str} {dt.day} {month_str} {dt.year}"
        except Exception:
            return fields.Datetime.to_string(dt).split(" ")[0]


class SaleOrderContractTerms(models.Model):
    _inherit = 'sale.order.line'

    technical_specification_id = fields.Text(
        related='product_id.product_tmpl_id.technical_specification',
        readonly=True
    )
