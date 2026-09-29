# -*- coding: utf-8 -*-
from odoo import fields, models, _
from odoo.exceptions import UserError


class PilotReportWizard(models.TransientModel):
    _name = 'pilot.report.wizard'
    _description = 'تقرير أوامر البيع حسب الطيار'

    x_driver_name = fields.Many2many(
        'x.pilot',
        string='اسم الطيار',
    )

    date_from = fields.Date(
        string='من تاريخ',
    )

    date_to = fields.Date(
        string='إلى تاريخ',
    )

    sale_order_id = fields.Many2one(
        'sale.order',
        string='أمر بيع ',
        domain=[('x_driver_name', '!=', False)],
        help='اتركه فارغاً إذا كنت تريد جميع أوامر البيع للطيار',
    )

    def _get_order_domain(self):
        domain = []
        if self.x_driver_name:
            domain = [('x_driver_name', 'in', self.x_driver_name.ids)]
        if self.date_from:
            domain.append(('date_order', '>=', self.date_from))
        if self.date_to:
            domain.append(('date_order', '<=', self.date_to))
        if self.sale_order_id:
            domain.append(('id', '=', self.sale_order_id.id))
        return domain

    def action_print_report(self):
        self.ensure_one()

        base_domain = self._get_order_domain()
        orders = self.env['sale.order'].search(base_domain, order='date_order desc')

        if not orders:
            raise UserError(
                _('لا توجد أوامر بيع تطابق معايير البحث المحددة.')
            )

        # Use read_group to group by pilot
        group_data = self.env['sale.order'].read_group(
            base_domain,
            ['x_driver_name', 'amount_total', 'id'],
            ['x_driver_name'],
            lazy=False,
        )

        pilot_groups = []
        for g in group_data:
            pilot = g.get('x_driver_name')
            if not pilot or pilot == [(6, '', [])]:
                continue
            pilot_id = pilot[0]
            pilot_name = pilot[1] if len(pilot) > 1 else pilot[0]
            pilot_orders = self.env['sale.order'].search(
                base_domain + [('x_driver_name', '=', pilot_id)]
            )
            pilot_groups.append({
                'name': pilot_name,
                'order_ids': pilot_orders.ids,
                'total': sum(pilot_orders.mapped('amount_total')),
                'count': len(pilot_orders),
            })

        # Handle orders without pilot
        no_pilot_orders = self.env['sale.order'].search(
            base_domain + [('x_driver_name', '=', False)]
        )
        if no_pilot_orders:
            pilot_groups.append({
                'name': 'بدون طيار',
                'order_ids': no_pilot_orders.ids,
                'total': sum(no_pilot_orders.mapped('amount_total')),
                'count': len(no_pilot_orders),
            })

        for pg in pilot_groups:
            pg['average'] = pg['total'] / pg['count'] if pg['count'] else 0.0

        wizard_driver_names = ', '.join(self.x_driver_name.mapped('name')) if self.x_driver_name else 'جميع الطيارين'

        return self.env.ref(
            'el_kitchen_receipt.action_pilot_report'
        ).with_context(
            from_wizard=True,
            wizard_driver_name=wizard_driver_names,
            wizard_date_from=self.date_from,
            wizard_date_to=self.date_to,
            wizard_sale_order=self.sale_order_id.name if self.sale_order_id else False,
            wizard_pilot_groups=pilot_groups,
            wizard_order_ids=orders.ids,
        ).report_action(orders)
