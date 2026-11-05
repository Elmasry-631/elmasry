# -*- coding: utf-8 -*-
"""Post-install data maintenance for secondary-currency amounts."""

import logging

_logger = logging.getLogger('odoo.modules')

def _post_init_hook(env):
    """Recalculate secondary_balance for ALL existing posted journal lines.
    Uses raw SQL to bypass ORM and fix stored values directly.
    secondary_balance = secondary_debit - secondary_credit for every line.
    """
    cr = env.cr
    _log("=" * 55)
    _log("POST-INIT: Recalculating secondary currency amounts...")
    _log("=" * 55)

    try:
        # === STEP 1: Full recalculation for posted moves with manual rate ===
        # Recompute ALL three secondary fields from raw debit/credit x rate
        cr.execute("""
            UPDATE account_move_line aml
            SET secondary_debit   = ROUND(aml.debit * am.manual_rate, rc.decimal_places),
                secondary_credit  = ROUND(aml.credit * am.manual_rate, rc.decimal_places),
                secondary_balance = ROUND(aml.debit * am.manual_rate, rc.decimal_places)
                                    - ROUND(aml.credit * am.manual_rate, rc.decimal_places)
            FROM account_move am
            JOIN res_currency rc ON rc.id = am.secondary_currency_id
            WHERE aml.move_id = am.id
              AND am.state = 'posted'
              AND am.use_manual_rate = true
              AND am.manual_rate > 0
              AND am.secondary_currency_id IS NOT NULL
        """)
        step1 = cr.rowcount
        _log(f"  -> Step 1: Recalculated {step1} posted lines (full recalc)")

        # === STEP 2: Fix secondary_balance ONLY for any remaining lines ===
        # where debit/credit are non-zero but balance is still wrong
        cr.execute("""
            UPDATE account_move_line aml
            SET secondary_balance = COALESCE(secondary_debit, 0) - COALESCE(secondary_credit, 0)
            FROM account_move am
            WHERE aml.move_id = am.id
              AND am.state = 'posted'
              AND am.use_manual_rate = true
              AND am.manual_rate > 0
              AND am.secondary_currency_id IS NOT NULL
              AND COALESCE(aml.secondary_balance, 0)
                  != COALESCE(aml.secondary_debit, 0) - COALESCE(aml.secondary_credit, 0)
        """)
        step2 = cr.rowcount
        _log(f"  -> Step 2: Fixed {step2} lines with wrong balance")

        # === STEP 3: Zero out secondary amounts for moves without manual rate ===
        cr.execute("""
            UPDATE account_move_line aml
            SET secondary_debit = 0,
                secondary_credit = 0,
                secondary_balance = 0
            FROM account_move am
            WHERE aml.move_id = am.id
              AND (am.use_manual_rate = false OR am.manual_rate IS NULL OR am.manual_rate <= 0)
              AND (COALESCE(aml.secondary_debit, 0) != 0
                   OR COALESCE(aml.secondary_credit, 0) != 0
                   OR COALESCE(aml.secondary_balance, 0) != 0)
        """)
        step3 = cr.rowcount
        _log(f"  -> Step 3: Zeroed {step3} lines without manual rate")

        _log(f"POST-INIT: Total fixed = {step1 + step2 + step3} lines")
    except Exception as e:
        _log(f"POST-INIT ERROR: {e}")

    _log("=" * 55)


def _log(msg):
    _logger.info("[advanced_accounting_reports] %s", msg)
