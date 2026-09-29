from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    material_requisition_id = fields.Many2one(
        'el_construction.material.requisition', string='Material Requisition', index=True, ondelete='set null'
    )

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    material_requisition_line_id = fields.Many2one(
        'el_construction.material.requisition.line', string='Material Requisition Line', index=True, ondelete='set null'
    )
