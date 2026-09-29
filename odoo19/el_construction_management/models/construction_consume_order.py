from .workflow_mixin import ConstructionWorkflowMixin
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ConstructionConsumeOrder(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.consume.order'
    _description = 'Material Consume Order'
    _inherit = ['mail.thread']
    _order = 'id desc'

    name = fields.Char(string='Reference', readonly=True, default='New', copy=False)
    subcontract_id = fields.Many2one('el_construction.subcontract', string='Subcontract', required=True, ondelete='cascade')
    project_id = fields.Many2one('el_construction.project', string='Project',
                                  related='subcontract_id.project_id', store=True, index=True)
    sub_project_id = fields.Many2one('el_construction.sub.project', string='Sub Project',
                                     related='subcontract_id.sub_project_id', store=True, index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 related='subcontract_id.company_id', store=True, index=True)
    date = fields.Date(string='Date', default=fields.Date.context_today)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    line_ids = fields.One2many('el_construction.consume.order.line', 'consume_order_id', string='Lines')
    notes = fields.Text(string='Notes')

    @api.constrains('subcontract_id')
    def _check_consistency(self):
        for rec in self:
            if rec.subcontract_id and rec.subcontract_id.company_id != rec.company_id:
                raise ValidationError(_('Consume Order company must match the Subcontract company.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('el_construction.consume.order') or 'New'
        return super().create(vals_list)

    def write(self, vals):
        if 'state' in vals and not self._workflow_write_allowed():
            for record in self:
                if vals['state'] != record.state:
                    raise UserError(_('Use the workflow buttons to change the Status.'))
        return super().write(vals)

    def action_confirm(self):
        return self._transition('confirmed', {'draft': {'confirmed'}})

    def action_done(self):
        return self._transition('done', {'confirmed': {'done'}}, manager=True)

    def action_cancel(self):
        return self._transition('cancelled', {'draft': {'cancelled'}, 'confirmed': {'cancelled'}}, manager=True)

class ConstructionConsumeOrderLine(models.Model):
    _name = 'el_construction.consume.order.line'
    _description = 'Consume Order Line'

    consume_order_id = fields.Many2one('el_construction.consume.order', string='Consume Order', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    description = fields.Char(string='Description')
    quantity = fields.Float(string='Quantity', default=1.0)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.name
            self.uom_id = self.product_id.uom_id.id
