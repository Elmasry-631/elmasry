import logging

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return

    # Legacy Work Order Lines: match through the Work Order context.
    cr.execute("""
        UPDATE el_construction_work_order_line AS src
           SET budget_line_id = candidate.id
          FROM (
                SELECT src2.id AS source_id, MIN(bl.id) AS id
                  FROM el_construction_work_order_line src2
                  JOIN el_construction_work_order wo ON wo.id = src2.work_order_id
                  JOIN el_construction_budget_line bl
                    ON bl.project_id = wo.project_id
                   AND bl.sub_project_id IS NOT DISTINCT FROM wo.sub_project_id
                   AND bl.company_id = wo.company_id
                   AND bl.product_id IS NOT DISTINCT FROM src2.product_id
                 WHERE src2.budget_line_id IS NULL
                 GROUP BY src2.id
                HAVING COUNT(bl.id) = 1
               ) candidate
         WHERE src.id = candidate.source_id
           AND src.budget_line_id IS NULL
    """)

    # Legacy Extra Expenses: use the explicit project/sub-project/company/product context.
    cr.execute("""
        UPDATE el_construction_extra_expense AS src
           SET budget_line_id = candidate.id
          FROM (
                SELECT src2.id AS source_id, MIN(bl.id) AS id
                  FROM el_construction_extra_expense src2
                  JOIN el_construction_budget_line bl
                    ON bl.project_id = src2.project_id
                   AND bl.sub_project_id IS NOT DISTINCT FROM src2.sub_project_id
                   AND bl.company_id = src2.company_id
                   AND bl.product_id IS NOT DISTINCT FROM src2.product_id
                 WHERE src2.budget_line_id IS NULL
                 GROUP BY src2.id
                HAVING COUNT(bl.id) = 1
               ) candidate
         WHERE src.id = candidate.source_id
           AND src.budget_line_id IS NULL
    """)

    # Legacy RA Billing Lines do not have a reliable product key. Auto-map only when
    # project/sub-project/company AND exact description resolve to exactly one budget line.
    cr.execute("""
        UPDATE el_construction_ra_billing_line AS src
           SET budget_line_id = candidate.id
          FROM (
                SELECT src2.id AS source_id, MIN(bl.id) AS id
                  FROM el_construction_ra_billing_line src2
                  JOIN el_construction_ra_billing ra ON ra.id = src2.ra_billing_id
                  JOIN el_construction_budget_line bl
                    ON bl.project_id = ra.project_id
                   AND bl.sub_project_id IS NOT DISTINCT FROM ra.sub_project_id
                   AND bl.company_id = ra.company_id
                   AND bl.description IS NOT DISTINCT FROM src2.description
                 WHERE src2.budget_line_id IS NULL
                 GROUP BY src2.id
                HAVING COUNT(bl.id) = 1
               ) candidate
         WHERE src.id = candidate.source_id
           AND src.budget_line_id IS NULL
    """)



    _log_unmapped_counts(cr)

# Migration is intentionally conservative: ambiguous legacy rows remain NULL.
# Staging operators should review these counts before production promotion.
def _log_unmapped_counts(cr):
    tables = (
        'el_construction_work_order_line',
        'el_construction_extra_expense',
        'el_construction_ra_billing_line',
    )
    for table in tables:
        cr.execute(f"SELECT count(*) FROM {table} WHERE budget_line_id IS NULL")
        count = cr.fetchone()[0]
        _logger.info(
            'Construction Management migration: %s has %s unmapped budget allocations',
            table, count,
        )
