from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ConstructionBoqLine(models.Model):
    _name = 'el_construction.boq.line'
    _description = 'BOQ Line'
    _order = 'id'
    _rec_name = 'description'

    boq_id = fields.Many2one('el_construction.boq', string='BOQ', required=True, ondelete='cascade', index=True)
    budget_line_ids = fields.One2many('el_construction.budget.line', 'boq_line_id', string='Budget Lines')
    product_id = fields.Many2one('product.product', string='Product')
    description = fields.Char(string='Description')
    quantity = fields.Float(string='Quantity', default=1.0)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    unit_price = fields.Float(string='Unit Price')
    amount = fields.Float(string='Amount', compute='_compute_amount', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        boq_ids = [vals.get('boq_id') for vals in vals_list if vals.get('boq_id')]
        boq_records = self.env['el_construction.boq'].browse(boq_ids)
        if any(boq.state != 'draft' for boq in boq_records):
            raise UserError(_('BOQ lines can only be created while the BOQ is Draft.'))
        protected_boqs = self.env['el_construction.boq'].browse(boq_ids).filtered(
            lambda boq: any(bl.budget_id.state in ('approved', 'done') for bl in boq.line_ids.mapped('budget_line_ids'))
        )
        if protected_boqs:
            raise UserError(_('BOQ lines cannot be added while the BOQ has an Approved or Done Budget.'))
        records = super().create(vals_list)
        records._check_values()
        return records

    def write(self, vals):
        if any(line.boq_id.state != 'draft' for line in self):
            raise UserError(_('BOQ lines can only be changed while the BOQ is Draft.'))
        if any(line.budget_line_ids.filtered(lambda bl: bl.budget_id.state in ('approved', 'done')) for line in self):
            if set(vals) - {'description'}:
                raise UserError(_('A BOQ Line linked to an Approved or Done Budget cannot be modified.'))
        result = super().write(vals)
        self._check_values()
        return result

    def unlink(self):
        for line in self:
            if line.boq_id.state != 'draft':
                raise UserError(_('BOQ lines can only be deleted while the BOQ is Draft.'))
            if line.budget_line_ids.filtered(lambda bl: bl.budget_id.state in ('approved', 'done')):
                raise UserError(_('A BOQ Line linked to an Approved or Done Budget cannot be deleted.'))
        return super().unlink()

    @api.depends('quantity', 'unit_price')
    def _compute_amount(self):
        for line in self:
            line.amount = line.quantity * line.unit_price

    def _check_values(self):
        for line in self:
            if line.quantity < 0:
                raise ValidationError(_('BOQ Quantity cannot be negative.'))
            if line.unit_price < 0:
                raise ValidationError(_('BOQ Unit Price cannot be negative.'))
            if line.product_id and line.uom_id and line.product_id.uom_id and not line.uom_id._has_common_reference(line.product_id.uom_id):
                raise ValidationError(_('BOQ Unit of Measure must use the same UoM category as the Product.'))

    @api.depends('description', 'product_id', 'boq_id.name', 'quantity', 'uom_id')
    def _compute_display_name(self):
        for line in self:
            if line.description:
                base = line.description
            elif line.product_id:
                base = line.product_id.display_name
            else:
                base = _('BOQ Line #%s') % line.id
            # اجعل الاسم مميز: [BOQ Reference] الوصف - الكمية الوحدة
            boq_ref = line.boq_id.name if line.boq_id and line.boq_id.name != 'New' else ''
            if boq_ref:
                base = f"[{boq_ref}] {base}"
            if line.quantity and line.uom_id:
                base = f"{base} ({line.quantity:g} {line.uom_id.name})"
            line.display_name = base

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.name
            self.uom_id = self.product_id.uom_id
            self.unit_price = self.product_id.standard_price
