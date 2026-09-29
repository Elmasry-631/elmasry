# investment_club/models/account_move.py
from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    investor_code_id = fields.Many2one("investment.membership")

    investor_code = fields.Char(
        related="investor_code_id.investor_code",
        store=True,
        readonly=True
    )

    _rec_name = "investor_code"

    # def action_open_membership(self):
    #     pass

    # ===== Hooks =====

    def _investment_activate_membership_if_paid(self):
        """Activate the membership automatically once its invoice is fully
        settled (amount_residual <= 0 on a posted customer invoice)."""
        invoices = self.filtered(
            lambda m: m.move_type == 'out_invoice'
            and m.investor_code_id
            and m.state == 'posted'
        )
        for invoice in invoices:
            try:
                if invoice.amount_residual <= 0:
                    invoice.investor_code_id._auto_activate_after_payment()
            except Exception:
                # Never block accounting flows because of the activation
                continue


class AccountFullReconcile(models.Model):
    _inherit = 'account.full.reconcile'

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        try:
            records.reconcile_line_ids.move_id._investment_activate_membership_if_paid()
        except Exception:
            pass
        return records


class AccountPartialReconcile(models.Model):
    _inherit = 'account.partial.reconcile'

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        try:
            moves = (records.debit_move_id | records.credit_move_id).move_id
            moves._investment_activate_membership_if_paid()
        except Exception:
            pass
        return records
