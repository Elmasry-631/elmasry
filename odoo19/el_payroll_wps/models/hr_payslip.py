from odoo import models, fields

HOUSING_CODE = 'HOUALLOW'


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    x_others = fields.Float(
        string='Others',
        digits='Payroll',
        help="Other allowances: the allowances of the payslip except the housing "
             "allowance (rule HOUALLOW). Set when the payslip is computed; you can "
             "edit it afterwards. Informational only: it does not change the Net "
             "Salary, and the WPS export always reads the payslip lines.",
    )

    def _get_line_amount_by_code(self, line_code):
        """Return the amount ('total') of a single payslip line matched by
        its rule code (e.g. 'NET', 'BASIC', 'HOUALLOW')."""
        self.ensure_one()
        line = self.line_ids.filtered(lambda l: l.code == line_code)
        return line[0].total if line else 0.0

    def _get_line_total_by_category(self, category_code):
        """Sum the payslip line totals of a salary rule category code, its
        sub-categories included (e.g. 'ALW' for Allowances, 'DED' for
        Deductions; deduction totals are negative)."""
        self.ensure_one()
        return sum(
            line.total for line in self.line_ids
            if category_code in (line.category_id.code, line.category_id.parent_id.code)
        )

    def _wps_amounts(self):
        """Amounts of the bank file columns. Basic + housing + other
        allowances - deductions equals the net salary when the NET rule is
        BASIC + ALW + DED (checked by the export)."""
        self.ensure_one()
        house = self._get_line_amount_by_code(HOUSING_CODE)
        housing_lines = self.line_ids.filtered(lambda l: l.code == HOUSING_CODE)
        house_in_alw = sum(
            l.total for l in housing_lines
            if 'ALW' in (l.category_id.code, l.category_id.parent_id.code)
        )
        return {
            'basic': self.basic_wage,
            'house': house,
            'others': self._get_line_total_by_category('ALW') - house_in_alw,
            'deductions': -self._get_line_total_by_category('DED'),
            'net': self.net_wage,
        }

    def _compute_x_others(self):
        """Others = other allowances (allowances except housing). Called once
        after the payslip lines are computed (see compute_sheet below), so a
        manual edit is kept until the sheet is computed again."""
        for slip in self:
            slip.x_others = slip._wps_amounts()['others']

    def compute_sheet(self):
        res = super().compute_sheet()
        self._compute_x_others()
        return res
