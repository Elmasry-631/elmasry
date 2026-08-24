from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    classification_id = fields.Many2one(
        comodel_name='customer.classification',
        string='Customer Classification',
        tracking=True,
        help='Assign this customer to a classification tier.',
    )

    override_pricelist = fields.Boolean(
        string='Override Price List',
        default=False,
        tracking=True,
        help='Enable to manually set a price list different from the classification.',
    )

    override_credit_limit = fields.Boolean(
        string='Override Credit Limit',
        default=False,
        tracking=True,
        help='Enable to manually set a credit limit different from the classification.',
    )

    override_payment_term = fields.Boolean(
        string='Override Payment Term',
        default=False,
        tracking=True,
        help='Enable to manually set a payment term different from the classification.',
    )

    manual_pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        string='Manual Price List',
        tracking=True,
        domain=lambda self: [('company_id', 'in', (False, self.env.company.id))],
        help='Manually assigned price list (takes effect when Override is enabled).',
    )

    classification_pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        string='Classification Price List',
        related='classification_id.pricelist_id',
        help='Price list inherited from the classification (read-only reference).',
    )

    classification_credit_limit = fields.Float(
        string='Classification Credit Limit',
        digits=(16, 2),
        related='classification_id.credit_limit',
        store=True,
        help='Credit limit inherited from the classification (stored for search/filter).',
    )

    classification_payment_term_id = fields.Many2one(
        comodel_name='account.payment.term',
        string='Classification Payment Term',
        related='classification_id.payment_term_id',
        help='Payment term inherited from the classification.',
    )

    credit_policy = fields.Selection(
        selection=[
            ('block', 'Block Sale'),
            ('warning', 'Warning Only'),
        ],
        string='Credit Policy',
        related='classification_id.credit_policy',
        store=True,
        help='Credit policy from the classification (stored for sale order logic).',
    )

    effective_credit_limit = fields.Float(
        string='Effective Credit Limit',
        digits=(16, 2),
        compute='_compute_effective_credit_limit',
        help='The actual credit limit applied: override > classification > 0.',
    )

    effective_payment_term_id = fields.Many2one(
        comodel_name='account.payment.term',
        string='Effective Payment Term',
        compute='_compute_effective_payment_term_id',
        help='The actual payment term applied: override > classification > partner default.',
    )

    payment_type = fields.Selection([
        ('cash', 'Cash'),
        ('credit', 'Credit'),
    ], string='Payment Type', default='cash', required=True, tracking=True)

    payment_gateway_id = fields.Many2one('sale.payment.gateway', string='Payment Gateway')

    @api.depends(
        'override_pricelist', 'manual_pricelist_id',
        'classification_id', 'classification_id.pricelist_id',
        'specific_property_product_pricelist',
    )
    @api.depends_context('company', 'country_code')
    def _compute_product_pricelist(self):
        classified = self.filtered('classification_id')
        for partner in classified:
            if partner.override_pricelist and partner.manual_pricelist_id:
                partner.property_product_pricelist = partner.manual_pricelist_id
            elif partner.classification_id.pricelist_id:
                partner.property_product_pricelist = (
                    partner.classification_id.pricelist_id
                )
            else:
                super(ResPartner, partner)._compute_product_pricelist()

        remaining = self - classified
        if remaining:
            super(ResPartner, remaining)._compute_product_pricelist()

    @api.depends(
        'payment_type',
        'override_credit_limit', 'credit_limit',
        'classification_id.credit_limit',
    )
    def _compute_effective_credit_limit(self):
        for partner in self:
            if partner.payment_type == 'cash':
                partner.effective_credit_limit = 0.0
            elif partner.override_credit_limit and partner.credit_limit:
                partner.effective_credit_limit = partner.credit_limit
            elif partner.classification_id and partner.classification_id.credit_limit:
                partner.effective_credit_limit = partner.classification_id.credit_limit
            elif partner.credit_limit:
                partner.effective_credit_limit = partner.credit_limit
            else:
                partner.effective_credit_limit = 0.0

    remaining_credit = fields.Float(
        string='Remaining Credit',
        digits=(16, 2),
        compute='_compute_remaining_credit',
        help='Available credit remaining (credit limit - outstanding).',
    )

    @api.depends('effective_credit_limit', 'credit')
    def _compute_remaining_credit(self):
        for partner in self:
            remaining = partner.effective_credit_limit - partner.credit
            partner.remaining_credit = max(remaining, 0.0)

    @api.depends(
        'override_payment_term', 'property_payment_term_id',
        'classification_id.payment_term_id',
    )
    def _compute_effective_payment_term_id(self):
        for partner in self:
            if partner.override_payment_term and partner.property_payment_term_id:
                partner.effective_payment_term_id = (
                    partner.property_payment_term_id
                )
            elif partner.classification_id.payment_term_id:
                partner.effective_payment_term_id = (
                    partner.classification_id.payment_term_id
                )
            else:
                partner.effective_payment_term_id = (
                    partner.property_payment_term_id
                )

    @api.onchange('classification_id')
    def _onchange_classification_id(self):
        if not self.classification_id:
            self.override_pricelist = False
            self.manual_pricelist_id = False
            self.override_credit_limit = False
            self.override_payment_term = False

    @api.onchange('override_pricelist')
    def _onchange_override_pricelist(self):
        if not self.override_pricelist:
            self.manual_pricelist_id = False

    @api.onchange('override_credit_limit')
    def _onchange_override_credit_limit(self):
        if not self.override_credit_limit:
            self.credit_limit = 0.0

    @api.onchange('override_payment_term')
    def _onchange_override_payment_term(self):
        if not self.override_payment_term:
            self.property_payment_term_id = False
