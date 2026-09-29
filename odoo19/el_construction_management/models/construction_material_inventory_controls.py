from .workflow_mixin import ConstructionWorkflowMixin
from odoo import api, fields, models, _, Command
from odoo.exceptions import UserError, ValidationError


class ConstructionMaterialRequisitionLineInventory(models.Model):
    _inherit = 'el_construction.material.requisition.line'

    issue_line_ids = fields.One2many('el_construction.material.issue.line', 'material_requisition_line_id', string='Stock Operations')
    issued_qty = fields.Float(compute='_compute_stock_quantities', string='Issued Qty')
    consumed_qty = fields.Float(compute='_compute_stock_quantities', string='Consumed Qty')
    returned_qty = fields.Float(compute='_compute_stock_quantities', string='Returned Qty')
    wastage_qty = fields.Float(compute='_compute_stock_quantities', string='Wastage Qty')
    received_qty = fields.Float(compute='_compute_received_qty', string='Received Qty')
    remaining_to_issue = fields.Float(compute='_compute_stock_quantities', string='Remaining to Issue')
    allowed_wastage_pct = fields.Float(string='Allowed Wastage (%)', default=0.0)
    allowed_wastage_qty = fields.Float(compute='_compute_allowed_wastage_qty', string='Allowed Wastage Qty')
    site_on_hand_qty = fields.Float(compute='_compute_site_on_hand_qty', string='Site On Hand')

    @api.depends('quantity', 'allowed_wastage_pct')
    def _compute_allowed_wastage_qty(self):
        for line in self:
            line.allowed_wastage_qty = line.quantity * max(line.allowed_wastage_pct, 0.0) / 100.0

    @api.depends('issue_line_ids.issue_id.state', 'issue_line_ids.issue_id.issue_type', 'issue_line_ids.quantity')
    def _compute_stock_quantities(self):
        for line in self:
            done = line.issue_line_ids.filtered(lambda l: l.issue_id.state == 'done')
            line.issued_qty = sum(done.filtered(lambda l: l.issue_id.issue_type == 'issue').mapped('quantity'))
            line.consumed_qty = sum(done.filtered(lambda l: l.issue_id.issue_type == 'consume').mapped('quantity'))
            line.returned_qty = sum(done.filtered(lambda l: l.issue_id.issue_type == 'return').mapped('quantity'))
            line.wastage_qty = sum(done.filtered(lambda l: l.issue_id.issue_type == 'wastage').mapped('quantity'))
            line.remaining_to_issue = max(line.quantity - line.issued_qty + line.returned_qty, 0.0)

    @api.depends('purchase_order_line_ids.qty_received', 'purchase_order_line_ids.product_uom_id')
    def _compute_received_qty(self):
        for line in self:
            total = 0.0
            target_uom = line.uom_id or line.product_id.uom_id
            for po_line in line.purchase_order_line_ids:
                qty = po_line.qty_received
                if po_line.product_uom and target_uom and po_line.product_uom != target_uom:
                    qty = po_line.product_uom._compute_quantity(qty, target_uom)
                total += qty
            line.received_qty = total

    @api.depends('product_id', 'requisition_id.project_id.site_location_id')
    def _compute_site_on_hand_qty(self):
        for line in self:
            location = line.requisition_id.project_id.site_location_id if line.requisition_id and line.requisition_id.project_id else False
            line.site_on_hand_qty = line.product_id.with_context(location=location.id).free_qty if line.product_id and location else 0.0
