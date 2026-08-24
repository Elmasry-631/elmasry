"""El Stock Alert model — logs rejected negative stock attempts."""

from odoo import api, fields, models, _


class ElStockAlert(models.Model):
    """Log of rejected negative stock attempts."""

    _name = 'el.stock.alert'
    _description = 'Negative Stock Alert'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(
        string='Reference',
        required=True,
        readonly=True,
        default=lambda self: _('New'),
        tracking=True,
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=True,
        readonly=True,
        index=True,
    )
    location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Location',
        required=True,
        readonly=True,
        index=True,
    )
    requested_qty = fields.Float(
        string='Requested Quantity',
        required=True,
        readonly=True,
    )
    available_qty = fields.Float(
        string='Available Quantity',
        required=True,
        readonly=True,
    )
    move_id = fields.Many2one(
        comodel_name='stock.move',
        string='Stock Move',
        readonly=True,
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Rejected By',
        readonly=True,
        default=lambda self: self.env.user,
    )
    state = fields.Selection(
        selection=[('rejected', 'Rejected')],
        string='Status',
        default='rejected',
        readonly=True,
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.company,
        readonly=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Assign sequence on create."""
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'el.stock.alert'
                ) or _('New')
        return super().create(vals_list)
