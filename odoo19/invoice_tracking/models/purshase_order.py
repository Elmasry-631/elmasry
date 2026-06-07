from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    tracking_count = fields.Integer(compute='_compute_tracking_count')

    def action_create_invoice_tracking(self):
        self.ensure_one()
        tracking_obj = self.env['invoice.tracking']

        existing_track = tracking_obj.search([
            '|',
            ('purchase_id', '=', self.id),
            ('purchase_reference', '=', self.name),
        ], limit=1)

        if existing_track:
            new_track = existing_track
        else:
            new_track = tracking_obj.create({
                'purchase_id': self.id,
                'purchase_reference': self.name,
                'partner_id': self.partner_id.id,
                'received_date': fields.Date.today(),
                'status': 'new',
            })

        return {
            'name': 'Invoice Tracking',
            'type': 'ir.actions.act_window',
            'res_model': 'invoice.tracking',
            'view_mode': 'form',
            'res_id': new_track.id,
            'target': 'current',
        }

    def _compute_tracking_count(self):
        for order in self:
            order.tracking_count = self.env['invoice.tracking'].search_count([
                '|',
                ('purchase_id', '=', order.id),
                ('purchase_reference', '=', order.name)
            ])
    def action_view_invoice_tracking(self):
        self.ensure_one()
        tracking_record = self.env['invoice.tracking'].search([
            '|',
            ('purchase_id', '=', self.id),
            ('purchase_reference', '=', self.name)
        ], limit=1)

        result = {
            'name': _('Invoice Tracking'),
            'type': 'ir.actions.act_window',
            'res_model': 'invoice.tracking',
            'target': 'current',
        }

        if tracking_record:
            result.update({
                'view_mode': 'form',
                'res_id': tracking_record.id,
            })
        else:
            result.update({
                'view_mode': 'list,form',
                'domain': ['|', ('purchase_id', '=', self.id), ('purchase_reference', '=', self.name)],
                'context': {
                    'default_purchase_id': self.id,
                    'default_purchase_reference': self.name,
                    'default_partner_id': self.partner_id.id,
                },
            })

        return result
