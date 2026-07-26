# -*- coding: utf-8 -*-
"""Company extension: cheque accounting configuration.

All company-level settings used by the cheque module to know which
accounts to debit/credit at each lifecycle transition, plus operational
thresholds (stale months, PDC reminder days, max re-deposits, approval
threshold).
"""
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    # Accounts
    cheque_received_account_id = fields.Many2one(
        string="Cheques Received Account",
        comodel_name="account.account",
        domain="[('company_ids', '=', id), ('active', '=', True)]",
        help="Current-asset account credited when a received cheque is "
             "handed to the bank for collection.",
    )
    cheque_under_collection_account_id = fields.Many2one(
        string="Cheques Under Collection Account",
        comodel_name="account.account",
        domain="[('company_ids', '=', id), ('active', '=', True)]",
        help="Current-asset account debited when a received cheque is "
             "deposited (still being cleared by the bank).",
    )
    cheque_issued_account_id = fields.Many2one(
        string="Cheques Issued Account",
        comodel_name="account.account",
        domain="[('company_ids', '=', id), ('active', '=', True)]",
        help="Current-liability account credited when an issued cheque is "
             "approved (the cheque has been written but not yet cashed).",
    )
    cheque_penalty_income_account_id = fields.Many2one(
        string="Cheque Penalty Income Account",
        comodel_name="account.account",
        domain="[('company_ids', '=', id), ('active', '=', True)]",
        help="Income account credited when a bounced cheque incurs a penalty.",
    )
    cheque_bank_charges_account_id = fields.Many2one(
        string="Cheque Bank Charges Account",
        comodel_name="account.account",
        domain="[('company_ids', '=', id), ('active', '=', True)]",
        help="Expense account debited for bank charges on returned cheques.",
    )

    # Operational thresholds
    cheque_stale_months = fields.Integer(
        string="Stale Cheque Months",
        default=6,
        help="A received cheque is flagged as stale if it has been in "
             "holding or deposited state for more than this many months.",
    )
    cheque_pdc_reminder_days = fields.Integer(
        string="PDC Reminder Days",
        default=7,
        help="Schedule a reminder activity this many days before a "
             "post-dated received cheque matures.",
    )
    cheque_max_redeposits = fields.Integer(
        string="Max Re-deposit Attempts",
        default=2,
        help="Maximum number of times a returned cheque can be re-deposited.",
    )
    cheque_approval_threshold = fields.Monetary(
        string="High-value Approval Threshold",
        currency_field="currency_id",
        default=50000.0,
        help="Issued cheques above this amount in company currency "
             "automatically schedule an approval activity.",
    )
