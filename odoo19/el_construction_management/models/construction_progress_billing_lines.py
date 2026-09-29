from .workflow_mixin import ConstructionWorkflowMixin
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ConstructionProgressBillingLine(models.Model):
    _name = 'el_construction.progress.billing.line'
    _description = 'Progress Billing Line'

    billing_id = fields.Many2one('el_construction.progress.billing', string='Billing', required=True, ondelete='cascade')
    line_type = fields.Selection([
        ('material', 'Material'),
        ('equipment', 'Equipment'),
        ('labour', 'Labour'),
        ('overhead', 'Overhead'),
        ('other', 'Other'),
    ], string='Type', required=True, default='material')

    product_id = fields.Many2one('product.product', string='Product')
    description = fields.Char(string='Description')
    quantity = fields.Float(string='Quantity', default=1.0)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    unit_price = fields.Float(string='Unit Price')
    tax_ids = fields.Many2many('account.tax', string='Taxes')
    tax_amount = fields.Float(string='Tax Amount', compute='_compute_amounts', store=True)
    total_amount = fields.Float(string='Total Amount', compute='_compute_amounts', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        billings = self.env['el_construction.progress.billing'].browse([v.get('billing_id') for v in vals_list if v.get('billing_id')])
        if any(billing.state != 'draft' for billing in billings):
            raise UserError(_('Progress Billing lines can only be created while the billing is Draft.'))
        return super().create(vals_list)

    @api.constrains('billing_id', 'tax_ids')
    def _check_tax_company(self):
        for line in self:
            if line.billing_id and line.tax_ids.filtered(lambda tax: tax.company_id and tax.company_id != line.billing_id.company_id):
                raise ValidationError(_('All Progress Billing taxes must belong to the same company as the Billing.'))

    @api.constrains('quantity', 'unit_price', 'uom_id', 'product_id')
    def _check_values(self):
        for line in self:
            if line.quantity <= 0:
                raise ValidationError(_('Progress Billing quantity must be greater than zero.'))
            if line.unit_price < 0:
                raise ValidationError(_('Progress Billing unit price cannot be negative.'))
            if line.product_id and line.uom_id and line.product_id.uom_id and not line.uom_id._has_common_reference(line.product_id.uom_id):
                raise ValidationError(_('Progress Billing Unit of Measure must use the same category as the Product.'))

    def write(self, vals):
        for line in self:
            if line.billing_id.state != 'draft':
                raise UserError(_('Progress Billing lines can only be changed while the billing is Draft.'))
        return super().write(vals)

    def unlink(self):
        for line in self:
            if line.billing_id.state != 'draft':
                raise UserError(_('Progress Billing lines can only be deleted while the billing is Draft.'))
        return super().unlink()

    @api.depends('quantity', 'unit_price', 'tax_ids')
    def _compute_amounts(self):
        for line in self:
            subtotal = line.quantity * line.unit_price
            tax_amount = 0.0
            if line.tax_ids:
                taxes = line.tax_ids.compute_all(line.unit_price, quantity=line.quantity)
                tax_amount = taxes['total_included'] - taxes['total_excluded']
            line.tax_amount = tax_amount
            line.total_amount = subtotal + tax_amount

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.name
            self.uom_id = self.product_id.uom_id.id
            self.unit_price = self.product_id.lst_price
