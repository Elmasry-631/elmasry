# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class InvoiceTracking(models.Model):
    _name = 'invoice.tracking'
    _description = 'Invoice Tracking'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Reference", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    bill_reference = fields.Char(string="Bill Reference")
    code_id = fields.Many2one('partner.code')
    partner_id = fields.Many2one('res.partner', string="Vendor")
    purchase_id = fields.Many2one('purchase.order', string="Purchase Order")
    vendor_bill_id = fields.Many2one('account.move', string="Vendor Bill", readonly=True, copy=False)
    purchase_reference = fields.Char(string="Purchase Reference")
    received_date = fields.Date(string="Received Date")
    bill_date = fields.Date(string="Bill Date")
    del_to_administration = fields.Date(string="delivery to administration Date")
    rec_from_administration = fields.Date(string=" Received from administration Date")

    purchase_line_ids = fields.One2many('purchase.order.line', compute='_compute_purchase_lines', string="Order Lines")
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id)
    egp_currency_id = fields.Many2one('res.currency', string="EGP Currency", default=lambda self: self.env.ref('base.EGP', raise_if_not_found=False))
    usd_currency_id = fields.Many2one('res.currency', string="USD Currency", default=lambda self: self.env.ref('base.USD', raise_if_not_found=False))
    total_invoice_amount = fields.Monetary(string="Total Invoice", currency_field="currency_id")
    approved_egp_amount = fields.Monetary(string="Approved EGP Amount", currency_field="egp_currency_id")
    approved_usd_amount = fields.Monetary(string="Approved USD Amount", currency_field="usd_currency_id")
    rate_today = fields.Float(string="Rate Today", compute="_compute_rate_today", store=True)
    usd_percentage = fields.Float('USD %', digits=(16, 2), default=100.0)
    egp_percentage = fields.Float('EGP %', digits=(16, 2), default=0.0)
    is_egp_currency = fields.Boolean()
    total_invoice_amount_egp = fields.Monetary(string="Total Invoice EGP", compute="_compute_total_invoice_amount_egp", store=True, currency_field="egp_currency_id")
    total_invoice_amount_usd = fields.Monetary(string="Total Invoice USD", compute="_compute_total_invoice_amount_usd", store=True, currency_field="usd_currency_id")
    well_number = fields.Many2one("oil.well", string="Well Number")


    status_id = fields.Many2one('check.tracking', string="Check Number")
    check_status = fields.Selection(string="Check Status", related='status_id.status', store=True)

    status = fields.Selection([
        ('new', 'New'),
        ('received', 'Received'),
        ('send_to_administration', 'Send To Administration'),
        ('receive_from_administration', 'Received from administration'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string="Status", default='new', tracking=True)


    @api.depends('purchase_id', 'purchase_reference')
    def _compute_purchase_lines(self):
        for rec in self:
            order = rec.purchase_id
            if not order and rec.purchase_reference:
                order = self.env['purchase.order'].search([('name', '=', rec.purchase_reference)], limit=1)
            if order:
                rec.purchase_line_ids = order.order_line if order else False
            else:
                rec.purchase_line_ids = False

    @api.depends('currency_id', 'total_invoice_amount')
    def _compute_rate_today(self):
        usd_currency = self.env.ref('base.USD', raise_if_not_found=False)
        egp_currency = self.env.ref('base.EGP', raise_if_not_found=False)
        company = self.env.company
        today = fields.Date.today()
        current_rate = 50.0
        if usd_currency and egp_currency:
            current_rate = usd_currency._convert(
                1.0, egp_currency, company, today
            )
        for rec in self:
            rec.rate_today = current_rate

    @api.depends('total_invoice_amount', 'egp_percentage', 'rate_today', 'currency_id')
    def _compute_total_invoice_amount_egp(self):
        # جلب العملات للمقارنة
        usd_currency = self.env.ref('base.USD')
        egp_currency = self.env.ref('base.EGP')

        for rec in self:
            amount_in_egp = 0.0
            if rec.total_invoice_amount and rec.egp_percentage:
                amount_by_percentage = rec.total_invoice_amount * (rec.egp_percentage / 100.0)
                if rec.currency_id == usd_currency:
                    amount_in_egp = amount_by_percentage * rec.rate_today
                elif rec.currency_id == egp_currency:
                    amount_in_egp = amount_by_percentage
                else:
                    amount_in_egp = rec.currency_id._convert(
                        amount_by_percentage, egp_currency, rec.env.company, fields.Date.today()
                    )

            rec.total_invoice_amount_egp = amount_in_egp

    @api.depends('total_invoice_amount', 'usd_percentage', 'currency_id')
    def _compute_total_invoice_amount_usd(self):
        usd_currency = self.env.ref('base.USD', raise_if_not_found=False)
        company = self.env.company
        today = fields.Date.today()
        for rec in self:
            amount_by_percentage = rec.total_invoice_amount * (rec.usd_percentage / 100.0)
            if amount_by_percentage and usd_currency and rec.currency_id and rec.currency_id != usd_currency:
                amount_by_percentage = rec.currency_id._convert(amount_by_percentage, usd_currency, company, today)
            rec.total_invoice_amount_usd = amount_by_percentage

    @api.constrains('egp_percentage', 'usd_percentage')
    def _check_percentages(self):
        for rec in self:
            if not 0 <= rec.egp_percentage <= 100 or not 0 <= rec.usd_percentage <= 100:
                raise ValidationError(_("Percentages must be between 0 and 100."))
            if round(rec.egp_percentage + rec.usd_percentage, 2) != 100.0:
                raise ValidationError(_("EGP and USD percentages must total 100%."))

    @api.onchange('egp_percentage')
    def _onchange_egp_percentage(self):
        if not 0 <= self.egp_percentage <= 100:
            return {'warning': {'title': _("Warning"), 'message': _("النسبة يجب أن تكون بين 0 و 100")}}
        self.usd_percentage = round(100.0 - self.egp_percentage, 2)

    @api.onchange('usd_percentage')
    def _onchange_usd_percentage(self):
        if not 0 <= self.usd_percentage <= 100:
            return {'warning': {'title': _("Warning"), 'message': _("النسبة يجب أن تكون بين 0 و 100")}}
        self.egp_percentage = round(100.0 - self.usd_percentage, 2)

    @api.onchange('currency_id')
    def _onchange_currency_id(self):
        usd_currency = self.env.ref('base.USD')
        egp_currency = self.env.ref('base.EGP')
        if self.currency_id == egp_currency:
            self.is_egp_currency = True
            self.egp_percentage = 100.0
            self.usd_percentage = 0.0
        elif self.currency_id == usd_currency:
            self.is_egp_currency = False
            self.egp_percentage = 0.0
            self.usd_percentage = 100.0

    @api.onchange('purchase_id')
    def _onchange_purchase_id(self):
        if self.purchase_id:
            self.purchase_reference = self.purchase_id.name
            self.partner_id = self.purchase_id.partner_id

    def _get_partner_from_code(self, code_id):
        if not code_id:
            return self.env['res.partner']
        return self.env['res.partner'].search([('code_id', '=', code_id)], limit=1)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('invoice.tracking') or _('New')
            if vals.get('purchase_id'):
                purchase_order = self.env['purchase.order'].browse(vals['purchase_id'])
                vals.setdefault('purchase_reference', purchase_order.name)
                vals.setdefault('partner_id', purchase_order.partner_id.id)
            if vals.get('code_id') and not vals.get('partner_id'):
                partner = self._get_partner_from_code(vals['code_id'])
                if partner:
                    vals['partner_id'] = partner.id
        return super(InvoiceTracking, self).create(vals_list)

    def write(self, vals):
        if vals.get('purchase_id') and ('purchase_reference' not in vals or 'partner_id' not in vals):
            purchase_order = self.env['purchase.order'].browse(vals['purchase_id'])
            vals = dict(vals)
            vals.setdefault('purchase_reference', purchase_order.name)
            vals.setdefault('partner_id', purchase_order.partner_id.id)
        if vals.get('code_id') and not vals.get('partner_id'):
            vals = dict(vals)
            partner = self._get_partner_from_code(vals['code_id'])
            if partner:
                vals['partner_id'] = partner.id
        return super().write(vals)



    def action_receive(self):
        for rec in self:
            if not rec.received_date:
                raise UserError(_("Please enter received date"))
            rec.status = 'received'

    def action_del_to_administration(self):
        for rec in self:
            if not rec.del_to_administration or not rec.bill_date:
                raise UserError(_("Please enter delivery administration date and bill date"))
            rec.status = 'send_to_administration'

    def action_rec_from_administration(self):
        for rec in self:
            if not rec.rec_from_administration:
                raise UserError(_("Please enter delivery administration date"))
            rec.status = 'receive_from_administration'

    def action_cancel(self):
        for rec in self:
            if rec.status == 'done':
                raise UserError(_("لا يمكنك إلغاء سجل تم إنشاء فاتورة له بالفعل (Done)."))
            rec.status = 'cancel'

    def action_reset_to_draft(self):
        for rec in self:
            rec.status = 'new'



    def action_create_bill_from_invoice_tracking(self):
        self.ensure_one()
        if self.status != 'receive_from_administration':
            raise UserError(_("You can only create a bill after receiving from administration."))
        if self.vendor_bill_id:
            raise UserError(_("A vendor bill is already linked to this tracking record."))
        if not self.partner_id:
            raise UserError(_("Please select a vendor before creating the bill."))

        purchase_order = self.purchase_id
        if not purchase_order and self.purchase_reference:
            purchase_order = self.env['purchase.order'].search([('name', '=', self.purchase_reference)], limit=1)

        invoice_lines = []
        if purchase_order:
            for line in purchase_order.order_line:
                if line.qty_to_invoice > 0:
                    account = line.product_id.property_account_expense_id or line.product_id.categ_id.property_account_expense_categ_id
                    if not account:
                        raise UserError(_("Please configure an expense account for product %s.") % line.product_id.display_name)
                    invoice_lines.append((0, 0, {
                        'product_id': line.product_id.id,
                        'name': line.name,
                        'quantity': line.qty_to_invoice,
                        'price_unit': line.price_unit,
                        'tax_ids': [(6, 0, line.tax_ids.ids)],
                        'purchase_line_id': line.id,
                        'account_id': account.id,
                    }))

        bill_vals = {
            'move_type': 'in_invoice',
            'partner_id': self.partner_id.id,
            'purchase_id': purchase_order.id if purchase_order else False,
            'ref': self.bill_reference or self.purchase_reference or self.name,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': invoice_lines,
        }
        new_bill = self.env['account.move'].create(bill_vals)
        self.vendor_bill_id = new_bill
        if not self.bill_reference:
            self.bill_reference = new_bill.ref
        self.status = 'done'
        return {
            'name': 'Bill Created',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': new_bill.id,
            'target': 'current',
        }

    def action_view_purchase_order(self):
        self.ensure_one()
        purchase_order = self.purchase_id
        if not purchase_order and self.purchase_reference:
            purchase_order = self.env['purchase.order'].search([('name', '=', self.purchase_reference)], limit=1)
        if purchase_order:
            return {'type': 'ir.actions.act_window', 'res_model': 'purchase.order', 'view_mode': 'form',
                    'res_id': purchase_order.id, 'target': 'current'}
        return {'type': 'ir.actions.client', 'tag': 'display_notification',
                'params': {'title': _('Warning'), 'message': _('No Purchase Order found.'), 'type': 'warning'}}

    def action_view_vendor_bill(self):
        self.ensure_one()
        vendor_bill = self.vendor_bill_id
        if not vendor_bill and self.bill_reference:
            vendor_bill = self.env['account.move'].search(
                [('ref', '=', self.bill_reference), ('move_type', '=', 'in_invoice')], limit=1)
        if vendor_bill:
            return {'name': _('Vendor Bill'), 'type': 'ir.actions.act_window', 'res_model': 'account.move',
                    'view_mode': 'form', 'res_id': vendor_bill.id, 'target': 'current'}
        return {'type': 'ir.actions.client', 'tag': 'display_notification',
                'params': {'title': _('Tracking'), 'message': _('No invoice found.'), 'type': 'warning'}}



    @api.onchange('code_id')
    def change_partner(self):
        if self.code_id:
            self.partner_id = self._get_partner_from_code(self.code_id.id)

    def unlink(self):
        for rec in self:
            if rec.status == 'done':
                raise UserError(_("You cannot delete a record that is in 'Done' status."))

        return super(InvoiceTracking, self).unlink()
