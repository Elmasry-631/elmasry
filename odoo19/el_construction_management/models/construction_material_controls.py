from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError

from .workflow_mixin import ConstructionWorkflowMixin


class ConstructionMaterialRequisitionControls(ConstructionWorkflowMixin, models.Model):
    _inherit = 'el_construction.material.requisition'

    procurement_stage = fields.Selection([('request','Requested'),('approved','Approved'),('sourcing','Sourcing'),('ordered','Ordered'),('received','Received'),('issued','Issued'),('consumed','Consumed'),('closed','Closed')], default='request', tracking=True)
    committed_amount = fields.Monetary(compute='_compute_procurement_amounts', currency_field='currency_id')
    received_amount = fields.Monetary(compute='_compute_procurement_amounts', currency_field='currency_id')
    currency_id = fields.Many2one(related='company_id.currency_id', store=True)

    @api.depends('purchase_order_link_ids.amount_total', 'picking_link_ids.state')
    def _compute_procurement_amounts(self):
        for rec in self:
            rec.committed_amount = sum(rec.purchase_order_link_ids.mapped('amount_total'))
            rec.received_amount = sum(rec.line_ids.mapped('amount')) if any(p.state == 'done' for p in rec.picking_link_ids) else 0.0
    # Construction material procurement and inventory controls.

    def action_submit_approval(self):
        result = super().action_submit_approval()
        self.write({'procurement_stage': 'request'})
        return result

    def action_approve(self):
        result = super().action_approve()
        self.write({'procurement_stage': 'approved'})
        return result

    def action_create_purchase_order(self):
        result = super().action_create_purchase_order()
        self.write({'procurement_stage': 'ordered'})
        return result

    def action_create_internal_transfer(self):
        result = super().action_create_internal_transfer()
        self.write({'procurement_stage': 'issued'})
        return result

    def action_done(self):
        result = super().action_done()
        self.write({'procurement_stage': 'closed'})
        return result

    # Merged Odoo 19 extension: ConstructionMaterialRequisitionInventory from construction_material_inventory.py

    site_location_id = fields.Many2one(related='project_id.site_location_id', string='Site Location', readonly=True)
    stock_operation_ids = fields.One2many('el_construction.material.issue', 'material_requisition_id', string='Stock Operations')
    stock_operation_count = fields.Integer(compute='_compute_stock_operation_count')

    @api.depends('stock_operation_ids')
    def _compute_stock_operation_count(self):
        for rec in self:
            rec.stock_operation_count = len(rec.stock_operation_ids)

    def action_create_material_issue(self):
        self.ensure_one()
        if self.state not in ('approved', 'in_progress', 'ready'):
            raise UserError(_('Material stock operations can only be created for an Approved/In Progress/Ready requisition.'))
        if not self.warehouse_id:
            raise UserError(_('Select a Warehouse on the Material Requisition before creating stock operations.'))
        self.project_id._ensure_stock_locations()
        if not self.site_location_id:
            raise UserError(_('The Project must have a warehouse and a Site Stock Location.'))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Issue Materials to Site'),
            'res_model': 'el_construction.material.issue',
            'view_mode': 'form',
            'context': {
                'default_project_id': self.project_id.id,
                'default_sub_project_id': self.sub_project_id.id,
                'default_work_order_id': self.work_order_id.id,
                'default_material_requisition_id': self.id,
                'default_warehouse_id': self.warehouse_id.id,
                'default_source_location_id': self.warehouse_id.lot_stock_id.id,
                'default_destination_location_id': self.site_location_id.id,
                'default_company_id': self.company_id.id,
                'default_issue_type': 'issue',
                'default_line_ids': [Command.create({
                    'material_requisition_line_id': line.id,
                    'product_id': line.product_id.id,
                    'description': line.description or line.product_id.display_name,
                    'quantity': line.quantity,
                    'uom_id': line.uom_id.id or line.product_id.uom_id.id,
                }) for line in self.line_ids],
            },
        }

    def action_view_stock_operations(self):
        self.ensure_one()
        return {
            'name': _('Material Stock Operations'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.material.issue',
            'view_mode': 'list,form',
            'domain': [('material_requisition_id', '=', self.id)],
        }

    def _open_stock_operation(self, issue_type):
        self.ensure_one()
        project = self.project_id
        project._ensure_stock_locations()
        warehouse = self.warehouse_id
        if issue_type == 'issue':
            source = warehouse.lot_stock_id
            destination = project.site_location_id
        elif issue_type == 'consume':
            source = project.site_location_id
            destination = project.consumption_location_id
        elif issue_type == 'return':
            source = project.site_location_id
            destination = warehouse.lot_stock_id
        else:
            source = project.site_location_id
            destination = False
        return {
            'type': 'ir.actions.act_window', 'name': _('Material Stock Operation'),
            'res_model': 'el_construction.material.issue', 'view_mode': 'form',
            'context': {
                'default_project_id': project.id, 'default_sub_project_id': self.sub_project_id.id,
                'default_work_order_id': self.work_order_id.id, 'default_material_requisition_id': self.id,
                'default_warehouse_id': warehouse.id, 'default_source_location_id': source.id,
                'default_destination_location_id': destination.id if destination else False,
                'default_company_id': self.company_id.id, 'default_issue_type': issue_type,
            },
        }

    def action_create_consumption(self):
        return self._open_stock_operation('consume')

    def action_create_return(self):
        return self._open_stock_operation('return')

    def action_create_wastage(self):
        return self._open_stock_operation('wastage')
