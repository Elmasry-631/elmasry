# -*- coding: utf-8 -*-
"""System-wide config settings exposing company cheque fields."""
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    cheque_received_account_id = fields.Many2one(
        string="Cheques Received Account",
        comodel_name="account.account",
        related="company_id.cheque_received_account_id",
        readonly=False,
        domain="[('company_ids', '=', company_id), ('active', '=', True)]",
    )
    cheque_under_collection_account_id = fields.Many2one(
        string="Cheques Under Collection Account",
        comodel_name="account.account",
        related="company_id.cheque_under_collection_account_id",
        readonly=False,
        domain="[('company_ids', '=', company_id), ('active', '=', True)]",
    )
    cheque_issued_account_id = fields.Many2one(
        string="Cheques Issued Account",
        comodel_name="account.account",
        related="company_id.cheque_issued_account_id",
        readonly=False,
        domain="[('company_ids', '=', company_id), ('active', '=', True)]",
    )
    cheque_penalty_income_account_id = fields.Many2one(
        string="Cheque Penalty Income Account",
        comodel_name="account.account",
        related="company_id.cheque_penalty_income_account_id",
        readonly=False,
        domain="[('company_ids', '=', company_id), ('active', '=', True)]",
    )
    cheque_bank_charges_account_id = fields.Many2one(
        string="Cheque Bank Charges Account",
        comodel_name="account.account",
        related="company_id.cheque_bank_charges_account_id",
        readonly=False,
        domain="[('company_ids', '=', company_id), ('active', '=', True)]",
    )
    cheque_stale_months = fields.Integer(
        string="Stale Cheque Months",
        related="company_id.cheque_stale_months",
        readonly=False,
    )
    cheque_pdc_reminder_days = fields.Integer(
        string="PDC Reminder Days",
        related="company_id.cheque_pdc_reminder_days",
        readonly=False,
    )
    cheque_max_redeposits = fields.Integer(
        string="Max Re-deposit Attempts",
        related="company_id.cheque_max_redeposits",
        readonly=False,
    )
    cheque_approval_threshold = fields.Monetary(
        string="High-value Approval Threshold",
        related="company_id.cheque_approval_threshold",
        readonly=False,
        currency_field="company_currency_id",
    )
    company_currency_id = fields.Many2one(
        string="Company Currency",
        comodel_name="res.currency",
        related="company_id.currency_id",
    )
