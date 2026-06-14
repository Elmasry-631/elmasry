from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ClassificationCriteria(models.Model):
    """
    Auto-classification criteria — defines conditions that determine
    whether a customer belongs to a specific classification.

    Multiple criteria on the same classification use AND logic:
    all must be true for the classification to match.

    Technical details:
        - Table: classification_criteria
        - Order: sequence, id
        - ondelete: CASCADE from classification

    Relationships:
        - Belongs to: customer.classification (field: classification_id)
    """

    _name = 'classification.criteria'
    _description = 'Classification Criteria'
    _order = 'sequence, id'
    _rec_name = 'display_name'

    # ── Field Mappings for Evaluation ────────────────────────────

    _EVAL_FIELDS = [
        ('total_sales', 'Total Sales (Current Year)'),
        ('total_sales_last_year', 'Total Sales (Last Year)'),
        ('outstanding_balance', 'Outstanding Balance'),
        ('overdue_balance', 'Overdue Balance'),
        ('number_of_orders', 'Number of Orders (Current Year)'),
        ('customer_age_days', 'Customer Age (Days)'),
    ]

    # ── Core Fields ──────────────────────────────────────────────

    classification_id = fields.Many2one(
        comodel_name='customer.classification',
        string='Classification',
        required=True,
        ondelete='cascade',
        help='The classification this criterion belongs to.',
    )

    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Order of evaluation within the classification.',
    )

    model_field = fields.Selection(
        selection=_EVAL_FIELDS,
        string='Field',
        required=True,
        help='The partner metric to evaluate.',
    )

    operator = fields.Selection(
        selection=[
            ('>', 'Greater Than'),
            ('<', 'Less Than'),
            ('>=', 'Greater Than or Equal'),
            ('<=', 'Less Than or Equal'),
            ('=', 'Equal'),
            ('between', 'Between'),
        ],
        string='Operator',
        required=True,
        help='Comparison operator.',
    )

    value = fields.Float(
        string='Value',
        digits=(16, 2),
        required=True,
        help='Primary comparison value.',
    )

    value_to = fields.Float(
        string='To Value',
        digits=(16, 2),
        help='Upper bound value. Required only when operator is "Between".',
    )

    active = fields.Boolean(
        string='Active',
        default=True,
        help='Disable without deleting.',
    )

    # ── Computed ─────────────────────────────────────────────────

    @api.depends('model_field', 'operator', 'value', 'value_to')
    def _compute_display_name(self):
        """Generate human-readable display name for the criterion."""
        operator_labels = dict(self._fields['operator'].selection)
        field_labels = dict(self._fields['model_field'].selection)
        for rec in self:
            op_label = operator_labels.get(rec.operator, rec.operator)
            field_label = field_labels.get(rec.model_field, rec.model_field)
            if rec.operator == 'between':
                rec.display_name = (
                    f"{field_label} {op_label} "
                    f"{rec.value} and {rec.value_to}"
                )
            else:
                rec.display_name = (
                    f"{field_label} {op_label} {rec.value}"
                )

    # ── Python Constraint ────────────────────────────────────────

    @api.constrains('operator', 'value', 'value_to')
    def _check_between_values(self):
        """For 'Between' operator, value_to must be greater than value."""
        for rec in self:
            if rec.operator == 'between' and rec.value_to <= rec.value:
                raise ValidationError(
                    _('For "Between" operator, "To Value" must be greater than "Value".')
                )

    # ── Evaluation Helper ────────────────────────────────────────

    def _evaluate(self, field_value):
        """
        Evaluate this criterion against a numeric value.
        Returns True if the criterion passes.
        """
        self.ensure_one()
        if self.operator == '>':
            return field_value > self.value
        elif self.operator == '<':
            return field_value < self.value
        elif self.operator == '>=':
            return field_value >= self.value
        elif self.operator == '<=':
            return field_value <= self.value
        elif self.operator == '=':
            return field_value == self.value
        elif self.operator == 'between':
            return self.value <= field_value <= self.value_to
        return False