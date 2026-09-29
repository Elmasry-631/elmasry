from .workflow_mixin import ConstructionWorkflowMixin
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ConstructionBudgetLine(models.Model):
    _name = 'el_construction.budget.line'
    _description = 'Construction Budget Line'
    _order = 'id'
    _rec_name = 'description'

    budget_id = fields.Many2one('el_construction.budget', string='Budget', required=True, ondelete='cascade', index=True)
    project_id = fields.Many2one(
        'el_construction.project', string='Project', related='budget_id.project_id', store=True, index=True,
    )
    sub_project_id = fields.Many2one(
        'el_construction.sub.project', string='Sub Project', related='budget_id.sub_project_id', store=True, index=True,
    )
    company_id = fields.Many2one(
        'res.company', string='Company', related='budget_id.company_id', store=True, index=True,
    )

    # Exact source of the planned amount. This replaces product-only matching.
    boq_line_id = fields.Many2one(
        'el_construction.boq.line', string='BOQ Line', ondelete='set null', index=True,
    )
    work_type_id = fields.Many2one('el_construction.work.type', string='Work Type')
    work_sub_type_id = fields.Many2one('el_construction.work.sub.type', string='Work Sub Type')
    product_id = fields.Many2one('product.product', string='Product')
    description = fields.Char(string='Description')
    quantity = fields.Float(string='Budget Quantity')
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    unit_price = fields.Float(string='Budget Unit Price')
    planned_amount = fields.Float(string='Planned Amount')

    actual_amount = fields.Float(
        string='Actual Amount', compute='_compute_actual_amount', readonly=True,
    )
    variance = fields.Float(string='Variance', compute='_compute_variance')
    progress = fields.Float(string='Progress (%)', compute='_compute_progress')

    _budget_boq_line_uniq = models.Constraint(
        'UNIQUE(budget_id, boq_line_id)',
        'A BOQ line can only be linked once to the same budget.',
    )

    @api.model_create_multi
    def create(self, vals_list):
        budgets = self.env['el_construction.budget'].browse([vals.get('budget_id') for vals in vals_list if vals.get('budget_id')])
        budgets._check_editable()
        for budget in budgets:
            if budget.budget_method == 'project':
                raise UserError(_('Budget Lines cannot be added to a Project Total budget.'))
        records = super().create(vals_list)
        records._check_consistency()
        records._check_structure()
        return records

    def write(self, vals):
        for record in self:
            record.budget_id._check_editable()
            if record.budget_id.budget_method == 'project':
                raise UserError(_('Budget Lines cannot be modified on a Project Total budget.'))
        result = super().write(vals)
        self._check_consistency()
        self._check_structure()
        return result

    def unlink(self):
        budgets = self.mapped('budget_id')
        budgets._check_editable()
        result = super().unlink()
        budgets._check_structure()
        return result

    @api.constrains('budget_id', 'boq_line_id', 'project_id', 'sub_project_id', 'company_id')
    def _check_budget_source(self):
        for line in self:
            if line.boq_line_id and line.boq_line_id.boq_id.company_id != line.company_id:
                raise ValidationError(_('Budget Line company must match the BOQ company.'))

    def _check_consistency(self):
        for line in self:
            budget = line.budget_id
            if not budget:
                continue
            if line.boq_line_id:
                boq = line.boq_line_id.boq_id
                if boq.project_id != budget.project_id:
                    raise ValidationError(_('BOQ Line must belong to the Budget Project.'))
                if boq.sub_project_id != budget.sub_project_id:
                    raise ValidationError(_('BOQ Line must belong to the Budget Sub Project.'))
                if boq.company_id != budget.company_id:
                    raise ValidationError(_('BOQ Line company must match the Budget company.'))
                boq_line_product = line.boq_line_id.product_id
                if line.product_id and boq_line_product:
                    if line.product_id != boq_line_product:
                        raise ValidationError(_('Budget Product must match the linked BOQ Line Product.'))
            if line.work_sub_type_id and line.work_sub_type_id.work_type_id != line.work_type_id:
                raise ValidationError(_('Work Sub Type must belong to the selected Work Type.'))
            if line.product_id and line.uom_id and line.product_id.uom_id and not line.uom_id._has_common_reference(line.product_id.uom_id):
                raise ValidationError(_('Budget Unit of Measure must use the same UoM category as the Product.'))
            if line.quantity < 0:
                raise ValidationError(_('Budget Quantity cannot be negative.'))
            if line.unit_price < 0:
                raise ValidationError(_('Budget Unit Price cannot be negative.'))
            if line.planned_amount < 0:
                raise ValidationError(_('Planned Amount cannot be negative.'))

    @api.depends('budget_id.project_id', 'budget_id.sub_project_id', 'budget_id.company_id', 'product_id', 'boq_line_id', 'work_type_id')
    def _compute_actual_amount(self):
        """Compute actual cost from explicit Budget Line allocations only.

        Sources are fetched in batches to avoid one SQL query per Budget Line.
        """
        if not self:
            return
        Expense = self.env['el_construction.extra.expense']
        WorkOrderLine = self.env['el_construction.work.order.line']
        RABillingLine = self.env['el_construction.ra.billing.line']
        ids = self.ids

        expenses = Expense.search([('budget_line_id', 'in', ids), ('state', '=', 'approved')])
        work_lines = WorkOrderLine.search([('budget_line_id', 'in', ids), ('work_order_id.state', '=', 'done')])
        ra_lines = RABillingLine.search([('budget_line_id', 'in', ids), ('ra_billing_id.state', '=', 'approved')])

        expense_totals = {}
        for rec in expenses:
            expense_totals[rec.budget_line_id.id] = expense_totals.get(rec.budget_line_id.id, 0.0) + rec.amount
        work_totals = {}
        for rec in work_lines:
            work_totals[rec.budget_line_id.id] = work_totals.get(rec.budget_line_id.id, 0.0) + rec.amount
        ra_totals = {}
        for rec in ra_lines:
            billing = rec.ra_billing_id
            if billing.total_amount:
                amount = billing.current_amount * (rec.amount / billing.total_amount)
                ra_totals[rec.budget_line_id.id] = ra_totals.get(rec.budget_line_id.id, 0.0) + amount

        for line in self:
            line.actual_amount = (
                expense_totals.get(line.id, 0.0)
                + work_totals.get(line.id, 0.0)
                + ra_totals.get(line.id, 0.0)
            )

    @api.depends('planned_amount', 'actual_amount')
    def _compute_variance(self):
        for line in self:
            line.variance = line.planned_amount - line.actual_amount

    @api.depends('planned_amount', 'actual_amount')
    def _compute_progress(self):
        for line in self:
            line.progress = (line.actual_amount / line.planned_amount * 100.0) if line.planned_amount else 0.0

    @api.depends('description', 'product_id', 'budget_id.name', 'planned_amount', 'boq_line_id')
    def _compute_display_name(self):
        for line in self:
            if line.description:
                base = line.description
            elif line.product_id:
                base = line.product_id.display_name
            elif line.boq_line_id and line.boq_line_id.display_name:
                base = line.boq_line_id.display_name
            else:
                base = _('Budget Line #%s') % line.id
            budget_ref = line.budget_id.name if line.budget_id and line.budget_id.name != 'New' else ''
            if budget_ref:
                base = f"[{budget_ref}] {base}"
            if line.planned_amount:
                base = f"{base} ({line.planned_amount:,.2f})"
            line.display_name = base

    def action_recompute_actual(self):
        self.invalidate_recordset(['actual_amount', 'variance', 'progress'])
        self._compute_actual_amount()
        self._compute_variance()
        self._compute_progress()
        return True
