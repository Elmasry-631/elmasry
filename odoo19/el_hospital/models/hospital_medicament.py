"""Hospital Medicament model — wraps product.product for medications."""

from odoo import api, fields, models, _


class HospitalMedicament(models.Model):
    """Medicament — links to product.product for stock integration."""

    _name = 'hospital.medicament'
    _description = 'Hospital Medicament'
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', compute='_compute_name', store=True, index=True)
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=True,
        ondelete='restrict',
    )
    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        string='Product Template',
        related='product_id.product_tmpl_id',
        store=True,
    )
    generic_name = fields.Char(string='Generic Name')
    form = fields.Selection([
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('syrup', 'Syrup'),
        ('injection', 'Injection'),
        ('inhaler', 'Inhaler'),
        ('other', 'Other'),
    ], string='Form', default='tablet')
    strength = fields.Char(string='Strength', help='e.g. "500mg"')
    is_prescription_required = fields.Boolean(string='Prescription Required', default=True)
    stock_qty = fields.Float(
        string='Stock Quantity',
        compute='_compute_stock_qty',
        help='Available stock from stock.quant',
    )
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    _product_unique = models.Constraint(
        'unique(product_id)',
        'A medicament record already exists for this product!',
        )

    @api.depends('product_id.name')
    def _compute_name(self):
        for rec in self:
            rec.name = rec.product_id.name or _('Unnamed Medicament')

    @api.depends('name', 'strength', 'form')
    def _compute_display_name(self):
        for rec in self:
            parts = [rec.name]
            if rec.strength:
                parts.append(rec.strength)
            if rec.form:
                parts.append(dict(self._fields['form'].selection).get(rec.form, rec.form))
            rec.display_name = ' - '.join(parts)

    @api.depends('product_id')
    def _compute_stock_qty(self):
        Quant = self.env['stock.quant']
        for rec in self:
            quants = Quant.search([
                ('product_id', '=', rec.product_id.id),
                ('location_id.usage', '=', 'internal'),
            ])
            rec.stock_qty = sum(quants.mapped('quantity')) - sum(quants.mapped('reserved_quantity'))
