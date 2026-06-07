# -*- coding: utf-8 -*-
"""
Pre-init hook to clean up leftover database artifacts from removed models.
Uses PostgreSQL session_replication_role trick to bypass ALL FK constraints.
"""

import logging

_logger = logging.getLogger('odoo.modules')

REMOVED_MODELS = (
    'account.feature.plan',
    'account.cost.center.plan',
    'account.feature.distribution',
    'account.cost.center.distribution',
)

OUR_MODELS = (
    'account.feature',
    'account.cost.center',
)

ALL_MODELS = OUR_MODELS + REMOVED_MODELS

REMOVED_TABLES = (
    'account_feature_plan',
    'account_cost_center_plan',
    'account_feature_distribution',
    'account_cost_center_distribution',
)


def _pre_init_hook(env):
    """Nuclear cleanup using PostgreSQL FK bypass."""
    cr = env.cr

    _log("=" * 55)
    _log("PRE-INIT CLEANUP STARTING...")
    _log("=" * 55)

    # ================================================================
    # MAGIC: Disable ALL FK checks and triggers for this session
    # This is the ONLY reliable way to delete views with inherit_id
    # ================================================================
    _log("Disabling FK checks...")
    cr.execute("SET session_replication_role = 'replica'")

    try:
        # Now we can delete views without ANY FK constraint blocking us

        _log("Deleting ALL views for our models + removed models...")
        cr.execute("DELETE FROM ir_ui_view WHERE model IN %s", (ALL_MODELS,))
        count = cr.rowcount
        _log(f"  -> Deleted {count} views")

        _log("Deleting views referencing stale fields...")
        for pattern in ('%move_line_id%', '%feature_distribution_ids%',
                        '%cost_center_distribution_ids%', '%feature_display%',
                        '%cost_center_display%', '%distribution_ids%'):
            cr.execute("DELETE FROM ir_ui_view WHERE arch_db::text LIKE %s", (pattern,))
            if cr.rowcount:
                _log(f"  -> Deleted {cr.rowcount} views matching '{pattern}'")

        # Clean up other artifacts
        _log("Cleaning up model data...")
        cr.execute("""
            DELETE FROM ir_model_data
            WHERE module = 'advanced_accounting_reports'
              AND (name LIKE '%%plan%%' OR name LIKE '%%distribution%%')
        """)
        _log(f"  -> Deleted {cr.rowcount} model data entries")

        _log("Cleaning up old top-level menus...")
        cr.execute("""
            DELETE FROM ir_ui_menu WHERE id IN (
                SELECT res_id FROM ir_model_data
                WHERE module = 'advanced_accounting_reports'
                  AND model = 'ir.ui.menu'
                  AND name IN (
                      'menu_advanced_accounting_root',
                      'menu_dimensions_root',
                      'menu_reports_root',
                      'menu_configuration_root',
                      'menu_general_ledger_wizard',
                      'menu_trial_balance_wizard',
                      'menu_account_feature',
                      'menu_account_cost_center',
                      'menu_account_patch_number'
                  )
            )
        """)

        _log("Cleaning up menus...")
        cr.execute("""
            DELETE FROM ir_ui_menu WHERE id IN (
                SELECT res_id FROM ir_model_data
                WHERE module = 'advanced_accounting_reports' AND name LIKE '%%plan%%'
            )
        """)

        _log("Cleaning up actions...")
        cr.execute("""
            DELETE FROM ir_act_window WHERE id IN (
                SELECT res_id FROM ir_model_data
                WHERE module = 'advanced_accounting_reports' AND name LIKE '%%plan%%'
            )
        """)

        _log("Cleaning up access rules...")
        cr.execute("""
            DELETE FROM ir_model_access
            WHERE model_id IN (SELECT id FROM ir_model WHERE model IN %s)
        """, (REMOVED_MODELS,))

        _log("Cleaning up record rules...")
        cr.execute("""
            DELETE FROM ir_rule
            WHERE model_id IN (SELECT id FROM ir_model WHERE model IN %s)
        """, (REMOVED_MODELS,))

        _log("Cleaning up field definitions...")
        cr.execute("""
            DELETE FROM ir_model_fields
            WHERE model_id IN (SELECT id FROM ir_model WHERE model IN %s)
        """, (REMOVED_MODELS,))

        cr.execute("""
            DELETE FROM ir_model_fields
            WHERE name IN ('plan_id', 'feature_distribution_ids',
                           'cost_center_distribution_ids', 'distribution_ids',
                           'feature_display', 'cost_center_display')
              AND model_id IN (
                  SELECT id FROM ir_model
                  WHERE model IN ('account.feature', 'account.cost.center', 'account.move.line')
              )
        """)

        _log("Cleaning up auto-rate field definitions from account.move...")
        cr.execute("""
            DELETE FROM ir_model_fields
            WHERE name IN ('auto_rate', 'effective_rate')
              AND model_id IN (
                  SELECT id FROM ir_model WHERE model = 'account.move'
              )
        """)
        _log(f"  -> Deleted {cr.rowcount} auto-rate field definitions")

        _log("Dropping auto_rate/effective_rate columns if they exist...")
        for col in ('auto_rate', 'effective_rate'):
            cr.execute(f"""
                ALTER TABLE account_move DROP COLUMN IF EXISTS {col}
            """)

        _log("Cleaning up auto-rate related views...")
        cr.execute("""
            DELETE FROM ir_ui_view
            WHERE arch_db::text LIKE '%%auto_rate%%'
               OR arch_db::text LIKE '%%effective_rate%%'
        """)
        if cr.rowcount:
            _log(f"  -> Deleted {cr.rowcount} views referencing auto-rate fields")

        _log("Cleaning up model definitions...")
        cr.execute("DELETE FROM ir_model WHERE model IN %s", (REMOVED_MODELS,))

        _log("Cleaning up constraints...")
        cr.execute("""
            DELETE FROM ir_model_constraint
            WHERE model IN (SELECT id FROM ir_model WHERE model IN %s)
        """, (REMOVED_MODELS,))

        _log("Dropping leftover tables...")
        for table in REMOVED_TABLES:
            cr.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
        _log("  -> Done")

    finally:
        # RE-ENABLE FK checks - CRITICAL: must always run
        _log("Re-enabling FK checks...")
        cr.execute("SET session_replication_role = 'origin'")

    # Verify cleanup
    cr.execute("SELECT COUNT(*) FROM ir_ui_view WHERE model IN %s", (ALL_MODELS,))
    remaining = cr.fetchone()[0]
    if remaining > 0:
        _log(f"WARNING: {remaining} views still remain. This should not happen.")
    else:
        _log("Verification: All views cleaned successfully.")

    _log("=" * 55)
    _log("PRE-INIT CLEANUP COMPLETED!")
    _log("=" * 55)


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
