from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CheckTracking(models.Model):
    _name = 'check.tracking'
    _description = 'Check Tracking Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Check Number', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)
    check_type = fields.Selection([
        ('incoming', 'Incoming Cheque'),
        ('outgoing', 'Outgoing Cheque'),
    ], string='Cheque Type', default='incoming', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    amount = fields.Monetary(string='Amount', currency_field='currency_id', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    secondary_amount = fields.Monetary(
        string='Amount in Another Currency',
        currency_field='secondary_currency_id',
        compute='_compute_secondary_amount',
        store=True,
    )
    secondary_currency_id = fields.Many2one('res.currency', string='Another Currency')

    date_issue = fields.Date(string='Issue Date', default=fields.Date.context_today)
    date_due = fields.Date(string='Due Date', required=True, tracking=True)

    bank_id = fields.Many2one('res.bank', string='Bank Name')
    journal_id = fields.Many2one('account.journal', string='Journal', domain=[('type', 'in', ('bank', 'cash'))])
    attachment_ids = fields.Many2many('ir.attachment', string='Check Scans')
    receivable_account_id = fields.Many2one(
        'account.account',
        string='Account Receivable',
        domain=[('account_type', '=', 'asset_receivable')],
    )
    payable_account_id = fields.Many2one(
        'account.account',
        string='Account Payable',
        domain=[('account_type', '=', 'liability_payable')],
    )
    bank_account_id = fields.Many2one('account.account', string='Bank Account')
    move_ids = fields.One2many('account.move', 'check_tracking_id', string='Journal Entries', readonly=True)
    move_count = fields.Integer(compute='_compute_move_count', string='Entries')

    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_hand', 'Cheque Received'),
        ('deposited', 'Under Collection'),
        ('cleared', 'Cleared'),
        ('bounced', 'Bounced'),
        ('issued', 'Issued'),
        ('cashed', 'Cashed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    @api.depends('move_ids')
    def _compute_move_count(self):
        for rec in self:
            rec.move_count = len(rec.move_ids)

    @api.depends('amount', 'currency_id', 'secondary_currency_id')
    def _compute_secondary_amount(self):
        today = fields.Date.context_today(self)
        company = self.env.company
        for rec in self:
            if rec.amount and rec.currency_id and rec.secondary_currency_id:
                rec.secondary_amount = rec.currency_id._convert(
                    rec.amount,
                    rec.secondary_currency_id,
                    company,
                    today,
                )
            else:
                rec.secondary_amount = 0.0

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.receivable_account_id = self.partner_id.property_account_receivable_id
            self.payable_account_id = self.partner_id.property_account_payable_id

    @api.onchange('journal_id')
    def _onchange_journal_id(self):
        if self.journal_id:
            self.bank_account_id = self.journal_id.default_account_id

    def _prepare_entry_lines(self, debit_account, credit_account):
        self.ensure_one()
        return [
            (0, 0, {
                'name': self.name,
                'partner_id': self.partner_id.id,
                'account_id': debit_account.id,
                'debit': self.amount,
                'credit': 0.0,
            }),
            (0, 0, {
                'name': self.name,
                'partner_id': self.partner_id.id,
                'account_id': credit_account.id,
                'debit': 0.0,
                'credit': self.amount,
            }),
        ]

    def _create_stage_entry(self, stage, debit_account, credit_account, label):
        self.ensure_one()
        if not self.journal_id:
            raise UserError(_("Please select a journal before creating cheque entries."))
        if not debit_account or not credit_account:
            raise UserError(_("Please configure the debit and credit accounts for this cheque stage."))
        if self.move_ids.filtered(lambda move: move.check_stage == stage):
            raise UserError(_("The accounting entry for this stage was already created."))

        move = self.env['account.move'].create({
            'move_type': 'entry',
            'date': fields.Date.context_today(self),
            'journal_id': self.journal_id.id,
            'ref': '%s - %s' % (self.name, label),
            'check_tracking_id': self.id,
            'check_stage': stage,
            'line_ids': self._prepare_entry_lines(debit_account, credit_account),
        })
        move.action_post()
        return move

    def _get_cheque_account(self, field_name, label):
        self.ensure_one()
        account = self.company_id[field_name]
        if not account:
            raise UserError(_("Please configure %s in Accounting Settings.") % label)
        return account

    def action_confirm(self):
        for rec in self:
            if rec.check_type == 'incoming':
                rec._create_stage_entry(
                    'receive',
                    rec._get_cheque_account('cheque_received_account_id', _('Cheques Received Account')),
                    rec.receivable_account_id,
                    _('Receive Cheque'),
                )
                rec.status = 'in_hand'
            else:
                rec.action_issue()

    def action_deposit(self):
        for rec in self:
            rec._create_stage_entry(
                'deposit',
                rec._get_cheque_account('cheque_under_collection_account_id', _('Cheques Under Collection Account')),
                rec._get_cheque_account('cheque_received_account_id', _('Cheques Received Account')),
                _('Deposit Cheque'),
            )
            rec.status = 'deposited'

    def action_clear(self):
        for rec in self:
            rec._create_stage_entry(
                'clear',
                rec.bank_account_id,
                rec._get_cheque_account('cheque_under_collection_account_id', _('Cheques Under Collection Account')),
                _('Cheque Cleared'),
            )
            rec.status = 'cleared'

    def action_bounce(self):
        for rec in self:
            rec._create_stage_entry(
                'bounce',
                rec.receivable_account_id,
                rec._get_cheque_account('cheque_under_collection_account_id', _('Cheques Under Collection Account')),
                _('Cheque Bounced'),
            )
            rec.status = 'bounced'

    def action_issue(self):
        for rec in self:
            rec._create_stage_entry(
                'issue',
                rec.payable_account_id,
                rec._get_cheque_account('cheque_issued_account_id', _('Cheques Issued Account')),
                _('Issue Cheque'),
            )
            rec.status = 'issued'

    def action_cash(self):
        for rec in self:
            rec._create_stage_entry(
                'cash',
                rec._get_cheque_account('cheque_issued_account_id', _('Cheques Issued Account')),
                rec.bank_account_id,
                _('Cheque Cashed'),
            )
            rec.status = 'cashed'

    def action_view_entries(self):
        self.ensure_one()
        return {
            'name': _('Cheque Journal Entries'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('check_tracking_id', '=', self.id)],
            'context': {'default_check_tracking_id': self.id},
        }

