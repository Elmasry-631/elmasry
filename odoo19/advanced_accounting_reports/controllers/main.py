# -*- coding: utf-8 -*-
from odoo import http

class AdvancedAccountingController(http.Controller):
    @http.route('/advanced_accounting/reports/general_ledger', type='json', auth='user')
    def get_general_ledger_data(self, **kw):
        wizard_id = kw.get('wizard_id')
        wizard = request.env['general.ledger.wizard'].browse(int(wizard_id))
        domain = wizard._build_domain()
        lines = request.env['account.move.line'].search_read(domain, [
            'date', 'journal_id', 'move_id', 'name', 'partner_id',
            'feature_ids', 'cost_center_ids', 'patch_number_id',
            'debit', 'credit', 'balance',
            'secondary_debit', 'secondary_credit', 'secondary_balance',
            'manual_rate',
        ])
        return {'lines': lines}
