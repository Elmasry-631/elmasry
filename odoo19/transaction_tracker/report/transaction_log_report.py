# -*- coding: utf-8 -*-
from odoo import models, api, _


class TransactionLogReport(models.AbstractModel):
    _name = 'report.transaction_tracker.report_transaction_log'
    _description = 'Transaction Log PDF Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['transaction.log'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'transaction.log',
            'docs': docs,
            'data': data or {},
        }
