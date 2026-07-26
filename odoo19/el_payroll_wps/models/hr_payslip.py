from odoo import models, fields


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    x_others = fields.Float(
        string='Others',
        digits='Payroll',
        help="Auto-calculated as Allowances minus Deductions when the payslip "
             "is computed. You can edit it manually afterwards. It is purely "
             "informational and has no effect on the Net Salary.",
    )

    def _get_line_amount_by_code(self, line_code):
        """Return the amount ('total') of a single payslip line matched by
        its rule code (e.g. 'NET', 'BASIC', 'HOUALLOW')."""
        self.ensure_one()
        line = self.line_ids.filtered(lambda l: l.code == line_code)
        return line[0].total if line else 0.0

    def _get_line_total_by_category(self, category_code):
        """Sum payslip line totals for a given salary rule category code
        (e.g. 'ALW' for Allowances, 'DED' for Deductions)."""
        self.ensure_one()
        return sum(
            line.total for line in self.line_ids
            if line.category_id.code == category_code
        )

    def _compute_x_others(self):
        """Set Others = Allowances total - Deductions total.
        Called once after the payslip lines are computed (see compute_sheet
        override below). Not an @api.depends compute, so a manual edit made
        afterwards is NOT overwritten until the sheet is recomputed again."""
        for slip in self:
            allowances = slip._get_line_total_by_category('ALW')
            deductions = slip._get_line_total_by_category('DED')
            slip.x_others = allowances - deductions

    def compute_sheet(self):
        res = super().compute_sheet()
        self._compute_x_others()
        return res
