"""Budget method migration for 19.0.1.5.0.

Existing budgets default to Budget Lines because that preserves the previous
meaning of total_planned and the existing explicit cost-allocation model.
No financial amounts are changed by this migration.
"""


def migrate(cr, version):
    if not version:
        return
    cr.execute(
        """
        UPDATE el_construction_budget
           SET budget_method = 'lines'
         WHERE budget_method IS NULL
        """
    )
