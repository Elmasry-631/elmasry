import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class CustomerClassification(models.Model):
    """
    Customer Classification — defines pricing, credit, and payment policies
    that are inherited by assigned customers.

    Technical details:
        - Table: customer_classification
        - Inherits: mail.thread, mail.activity.mixin
        - Order: sequence, name

    Relationships:
        - Has many: res.partner (field: partner_ids)
        - Has many: classification.criteria (field: criteria_ids)
        - Belongs to: product.pricelist (field: pricelist_id)
        - Belongs to: account.payment.term (field: payment_term_id)
        - Belongs to: res.company (field: company_id)
    """

    _name = 'customer.classification'
    _description = 'Customer Classification'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'
    _rec_name = 'display_name'

    # ── Identity Fields ──────────────────────────────────────────

    name = fields.Char(
        string='Code',
        required=True,
        tracking=True,
        help='Classification code (e.g., A, B, C). Must be unique per company.',
    )

    description = fields.Text(
        string='Description',
        tracking=True,
        help='Optional description of this customer tier.',
    )

    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sort order for lists and auto-classification priority.',
    )

    active = fields.Boolean(
        string='Active',
        default=True,
        help='Soft delete. Inactive classifications are hidden from lists.',
    )

    # ── Pricing Fields ───────────────────────────────────────────

    pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        string='Price List',
        tracking=True,
        domain="[('company_id', 'in', (False, company_id))]",
        help='Default price list inherited by customers in this classification.',
    )

    # ── Credit Fields ────────────────────────────────────────────

    credit_limit = fields.Float(
        string='Credit Limit',
        digits=(16, 2),
        default=0.0,
        tracking=True,
        help='Default credit limit for customers in this classification.',
    )

    payment_term_id = fields.Many2one(
        comodel_name='account.payment.term',
        string='Payment Term',
        tracking=True,
        help='Default payment term inherited by customers in this classification.',
    )

    credit_policy = fields.Selection(
        selection=[
            ('block', 'Block Sale'),
            ('warning', 'Warning Only'),
        ],
        string='Credit Policy',
        required=True,
        default='block',
        tracking=True,
        help='What happens when a customer exceeds their credit limit:\n'
             '- Block Sale: Prevent order confirmation with an error.\n'
             '- Warning Only: Post a warning message but allow confirmation.',
    )

    # ── Multi-Company ────────────────────────────────────────────

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        help='Each classification belongs to a single company.',
    )

    # ── Relation Fields ──────────────────────────────────────────

    partner_ids = fields.One2many(
        comodel_name='res.partner',
        inverse_name='classification_id',
        string='Customers',
        help='All customers assigned to this classification.',
    )

    partner_count = fields.Integer(
        string='Customer Count',
        compute='_compute_partner_count',
        store=True,
        help='Number of customers in this classification.',
    )

    criteria_ids = fields.One2many(
        comodel_name='classification.criteria',
        inverse_name='classification_id',
        string='Auto-Classification Criteria',
        help='Conditions for automatic customer classification.',
    )

    has_active_criteria = fields.Boolean(
        string='Has Active Criteria',
        compute='_compute_has_active_criteria',
        help='Whether this classification has any active auto-classification criteria.',
    )

    # ── Computed Fields ──────────────────────────────────────────

    @api.depends('name', 'description')
    def _compute_display_name(self):
        """Generate display name: 'Code - Description' or just 'Code'."""
        for rec in self:
            if rec.description:
                rec.display_name = f"{rec.name} - {rec.description}"
            else:
                rec.display_name = rec.name

    @api.depends('partner_ids')
    def _compute_partner_count(self):
        """Count customers in this classification."""
        for rec in self:
            rec.partner_count = len(rec.partner_ids)

    @api.depends('criteria_ids.active')
    def _compute_has_active_criteria(self):
        """Check if any active criteria exist."""
        for rec in self:
            rec.has_active_criteria = any(
                c.active for c in rec.criteria_ids
            )

    # ── Constraints (Odoo 19: models.Constraint) ─────────────────

    _name_uniq_per_company = models.Constraint(
        'UNIQUE(name, company_id)',
        'Classification code must be unique per company!',
    )

    # ── Actions ──────────────────────────────────────────────────

    def action_apply_pricelist(self):
        """
        Safety net: manually push pricelist to all non-override customers.
        Normally @api.depends handles this, but this button ensures
        consistency in edge cases (e.g., after bulk import).
        """
        self.ensure_one()
        partners = self.partner_ids.filtered(
            lambda p: not p.override_pricelist
        )
        if partners:
            partners._compute_product_pricelist()
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Pricelist Updated'),
                    'message': _(
                        'Price list has been updated for %(count)s customer(s).',
                        count=len(partners),
                    ),
                    'type': 'success',
                    'sticky': False,
                },
            }
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('No Updates'),
                'message': _('No customers found to update.'),
                'type': 'info',
                'sticky': False,
            },
        }

    # ── Auto-Classification (Cron) ───────────────────────────────

    def _auto_classify_partners(self):
        """
        Evaluate auto-classification criteria for all customers.
        Called by the scheduled action (cron job).

        Algorithm:
            1. Get all active classifications with active criteria, ordered by sequence.
            2. For each company, get its customers.
            3. For each customer, evaluate criteria per classification (AND logic).
            4. First matching classification wins.
            5. If no match, customer keeps current classification.
        """
        classifications = self.search([
            ('active', '=', True),
            ('has_active_criteria', '=', True),
        ], order='sequence, name')

        if not classifications:
            return

        companies = classifications.mapped('company_id')
        updated_count = 0

        for company in companies:
            company_classifs = classifications.filtered(
                lambda c: c.company_id == company
            )
            if not company_classifs:
                continue

            customers = self.env['res.partner'].with_company(company).search([
                ('is_company', '=', True),
                ('company_id', '=', company.id),
            ])

            for partner in customers:
                new_classif = self._evaluate_for_partner(
                    partner, company_classifs
                )
                if new_classif and new_classif != partner.classification_id:
                    old_name = partner.classification_id.display_name or _('None')
                    partner.classification_id = new_classif
                    partner.message_post(
                        body=_(
                            'Auto-classification: changed from %(old)s to %(new)s.',
                            old=old_name,
                            new=new_classif.display_name,
                        ),
                        subject=_('Auto-Classification'),
                    )
                    updated_count += 1

        if updated_count:
            _logger.info(
                'Customer Classification: auto-classified %d customer(s).',
                updated_count,
            )

    def _evaluate_for_partner(self, partner, classifications):
        """
        Evaluate classification criteria for a single partner.
        Returns the first matching classification or None.
        """
        metrics = self._get_partner_metrics(partner)

        for classification in classifications:
            active_criteria = classification.criteria_ids.filtered('active')
            if not active_criteria:
                continue

            all_match = True
            for criterion in active_criteria:
                field_value = metrics.get(criterion.model_field, 0.0)
                if not criterion._evaluate(field_value):
                    all_match = False
                    break

            if all_match:
                return classification

        return None

    def _get_partner_metrics(self, partner):
        """
        Compute all evaluation metrics for a partner.
        Returns a dict: metric_name -> float_value.
        """
        today = fields.Date.today()
        current_year_start = fields.Date.replace(today, month=1, day=1)
        last_year_start = fields.Date.replace(
            today, year=today.year - 1, month=1, day=1,
        )
        last_year_end = fields.Date.replace(
            today, year=today.year - 1, month=12, day=31,
        )

        # Current year sales
        current_sales = self.env['sale.order'].read_group(
            [
                ('partner_id', '=', partner.id),
                ('state', 'in', ('sale', 'done')),
                ('date_order', '>=', current_year_start),
            ],
            ['amount_total:sum'],
            [],
        )
        total_sales = current_sales[0].get('amount_total', 0.0) or 0.0

        # Last year sales
        last_sales = self.env['sale.order'].read_group(
            [
                ('partner_id', '=', partner.id),
                ('state', 'in', ('sale', 'done')),
                ('date_order', '>=', last_year_start),
                ('date_order', '<=', last_year_end),
            ],
            ['amount_total:sum'],
            [],
        )
        total_sales_last_year = last_sales[0].get('amount_total', 0.0) or 0.0

        # Number of orders this year
        order_count = self.env['sale.order'].search_count([
            ('partner_id', '=', partner.id),
            ('date_order', '>=', current_year_start),
        ])

        # Overdue balance (unpaid invoices past due date)
        overdue_moves = self.env['account.move'].read_group(
            [
                ('partner_id', '=', partner.id),
                ('move_type', '=', 'out_invoice'),
                ('payment_state', '!=', 'paid'),
                ('invoice_date_due', '<', today),
            ],
            ['amount_residual:sum'],
            [],
        )
        overdue_balance = overdue_moves[0].get('amount_residual', 0.0) or 0.0

        # Customer age in days
        customer_age_days = 0.0
        if partner.create_date:
            customer_age_days = (
                fields.Datetime.now() - partner.create_date
            ).days

        return {
            'total_sales': total_sales,
            'total_sales_last_year': total_sales_last_year,
            'outstanding_balance': partner.credit,
            'overdue_balance': overdue_balance,
            'number_of_orders': float(order_count),
            'customer_age_days': float(customer_age_days),
        }