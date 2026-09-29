from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.addons.el_construction_management.models.workflow_mixin import ConstructionWorkflowMixin


class ConstructionTenderRfq(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.tender.rfq'
    _description = 'Subcontractor / Vendor RFQ (Tendering)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    _ALLOWED = {
        'draft': {'sent', 'cancelled'},
        'sent': {'bidding', 'cancelled', 'draft'},
        'bidding': {'comparison', 'cancelled'},
        'comparison': {'awarded', 'bidding', 'cancelled'},
        'awarded': set(),
        'cancelled': {'draft'},
    }

    name = fields.Char(string='Reference', readonly=True, default='New', copy=False)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    project_id = fields.Many2one('el_construction.project', string='Project',
                                  help='Set when this RFQ is for an already-awarded project. Awarding it will generate a Subcontract.')
    sub_project_id = fields.Many2one('el_construction.sub.project', string='Sub Project')
    tender_opportunity_id = fields.Many2one(
        'el_construction.tender.opportunity', string='Tender Opportunity',
        help='Set when this RFQ is used to build up the cost of a client bid before award.')

    work_type_id = fields.Many2one('el_construction.work.type', string='Work Type')
    scope_description = fields.Text(string='Scope of Work')
    submission_deadline = fields.Datetime(string='Submission Deadline')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('bidding', 'Bidding'),
        ('comparison', 'Comparison'),
        ('awarded', 'Awarded'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    line_ids = fields.One2many('el_construction.tender.rfq.line', 'rfq_id', string='Requested Items')
    vendor_ids = fields.One2many('el_construction.tender.rfq.vendor', 'rfq_id', string='Invited Vendors')
    winner_vendor_id = fields.Many2one('el_construction.tender.rfq.vendor', string='Awarded Vendor', readonly=True, copy=False)
    subcontract_id = fields.Many2one('el_construction.subcontract', string='Generated Subcontract', readonly=True, copy=False)

    lowest_amount = fields.Float(string='Lowest Bid', compute='_compute_stats')
    vendor_count = fields.Integer(string='Vendors', compute='_compute_stats')

    @api.constrains('project_id', 'tender_opportunity_id', 'sub_project_id', 'company_id')
    def _check_consistency(self):
        for rec in self:
            if not rec.project_id and not rec.tender_opportunity_id:
                raise ValidationError(_(
                    'An RFQ must be linked to either a Project (post-award subcontracting) '
                    'or a Tender Opportunity (pre-award cost buildup).'))
            if rec.sub_project_id and rec.sub_project_id.project_id != rec.project_id:
                raise ValidationError(_('Sub Project must belong to the selected Project.'))
            if rec.project_id and rec.project_id.company_id != rec.company_id:
                raise ValidationError(_('RFQ company must match the Project company.'))
            if rec.tender_opportunity_id and rec.tender_opportunity_id.company_id != rec.company_id:
                raise ValidationError(_('RFQ company must match the Tender Opportunity company.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('el_construction.tender.rfq') or 'New'
        return super().create(vals_list)

    def write(self, vals):
        if 'state' in vals and not self._workflow_write_allowed():
            for rec in self:
                if vals['state'] != rec.state:
                    raise UserError(_('Use the workflow buttons to change the Status.'))
        return super().write(vals)

    @api.depends('vendor_ids.total_amount', 'vendor_ids.state')
    def _compute_stats(self):
        for rec in self:
            amounts = rec.vendor_ids.filtered(lambda v: v.state in ('submitted', 'awarded')).mapped('total_amount')
            rec.lowest_amount = min(amounts) if amounts else 0.0
            rec.vendor_count = len(rec.vendor_ids)

    # Workflow -----------------------------------------------------------
    def action_send(self):
        for rec in self:
            if not rec.vendor_ids:
                raise UserError(_('Invite at least one vendor before sending the RFQ.'))
            if not rec.line_ids:
                raise UserError(_('Add at least one requested item before sending the RFQ.'))
        self._transition('sent', self._ALLOWED)

    def action_start_bidding(self):
        self._transition('bidding', self._ALLOWED)

    def action_go_comparison(self):
        for rec in self:
            if not rec.vendor_ids.filtered(lambda v: v.state == 'submitted'):
                raise UserError(_('At least one vendor must have a submitted bid to move to Comparison.'))
        self._transition('comparison', self._ALLOWED)

    def action_reset_draft(self):
        self._transition('draft', self._ALLOWED)

    def action_cancel(self):
        self._transition('cancelled', self._ALLOWED)

    def action_open_compare_wizard(self):
        self.ensure_one()
        wizard = self.env['el_construction.tender.rfq.compare.wizard'].create({'rfq_id': self.id})
        return {
            'name': _('Bid Comparison'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.tender.rfq.compare.wizard',
            'view_mode': 'form',
            'res_id': wizard.id,
            'target': 'new',
        }

    def action_award_vendor(self, vendor):
        """Award the RFQ to `vendor` (an el_construction.tender.rfq.vendor record)."""
        self.ensure_one()
        vendor.ensure_one()
        if vendor.rfq_id != self:
            raise UserError(_('The selected vendor does not belong to this RFQ.'))
        if vendor.state != 'submitted':
            raise UserError(_('Only a vendor with a submitted bid can be awarded.'))

        self._transition('awarded', self._ALLOWED)
        self.winner_vendor_id = vendor.id
        vendor.state = 'awarded'
        (self.vendor_ids - vendor).filtered(lambda v: v.state == 'submitted').write({'state': 'rejected'})

        for line in self.line_ids:
            bid_line = vendor.bid_line_ids.filtered(lambda b: b.rfq_line_id == line)
            line.awarded_unit_price = bid_line[:1].unit_price

        if self.project_id:
            return self.action_create_subcontract()
        return True

    def action_create_subcontract(self):
        self.ensure_one()
        if not self.winner_vendor_id:
            raise UserError(_('Award the RFQ to a vendor first.'))
        if not self.project_id:
            raise UserError(_('A Subcontract can only be generated from an RFQ linked to a Project.'))
        if self.subcontract_id:
            return self._open_subcontract_action()

        subcontract = self.env['el_construction.subcontract'].create({
            'project_id': self.project_id.id,
            'sub_project_id': self.sub_project_id.id,
            'partner_id': self.winner_vendor_id.partner_id.id,
            'company_id': self.company_id.id,
            'work_description': self.scope_description,
            'line_ids': [(0, 0, {
                'description': line.description,
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'uom_id': line.uom_id.id,
                'unit_price': line.awarded_unit_price,
            }) for line in self.line_ids],
        })
        self.subcontract_id = subcontract.id
        return self._open_subcontract_action()

    def _open_subcontract_action(self):
        self.ensure_one()
        return {
            'name': _('Subcontract'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.subcontract',
            'view_mode': 'form',
            'res_id': self.subcontract_id.id,
        }


class ConstructionTenderRfqLine(models.Model):
    _name = 'el_construction.tender.rfq.line'
    _description = 'RFQ Requested Item'
    _order = 'id'
    _rec_name = 'description'

    rfq_id = fields.Many2one('el_construction.tender.rfq', string='RFQ', required=True, ondelete='cascade', index=True)
    boq_line_id = fields.Many2one('el_construction.boq.line', string='BOQ Line (optional source)')
    product_id = fields.Many2one('product.product', string='Product')
    description = fields.Char(string='Description', required=True)
    quantity = fields.Float(string='Quantity', default=1.0)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    awarded_unit_price = fields.Float(string='Awarded Unit Price', readonly=True, copy=False)

    @api.constrains('quantity')
    def _check_quantity(self):
        for line in self:
            if line.quantity < 0:
                raise ValidationError(_('Quantity cannot be negative.'))

    @api.onchange('boq_line_id')
    def _onchange_boq_line_id(self):
        if self.boq_line_id:
            self.description = self.boq_line_id.description
            self.product_id = self.boq_line_id.product_id
            self.quantity = self.boq_line_id.quantity
            self.uom_id = self.boq_line_id.uom_id

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.name
            self.uom_id = self.product_id.uom_id


class ConstructionTenderRfqVendor(models.Model):
    _name = 'el_construction.tender.rfq.vendor'
    _description = 'RFQ Invited Vendor'
    _order = 'total_amount'
    _rec_name = 'partner_id'

    rfq_id = fields.Many2one('el_construction.tender.rfq', string='RFQ', required=True, ondelete='cascade', index=True)
    partner_id = fields.Many2one('res.partner', string='Vendor / Subcontractor', required=True,
                                  domain="[('supplier_rank', '>', 0)]")
    state = fields.Selection([
        ('invited', 'Invited'),
        ('submitted', 'Bid Submitted'),
        ('declined', 'Declined'),
        ('rejected', 'Rejected'),
        ('awarded', 'Awarded'),
    ], string='Status', default='invited', tracking=True)
    submission_date = fields.Date(string='Submission Date')
    bid_line_ids = fields.One2many('el_construction.tender.rfq.bid.line', 'rfq_vendor_id', string='Bid Lines')
    total_amount = fields.Float(string='Total Bid Amount', compute='_compute_total_amount', store=True)
    notes = fields.Text(string='Notes')

    @api.depends('bid_line_ids.amount')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.bid_line_ids.mapped('amount'))

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            existing_lines = rec.bid_line_ids.mapped('rfq_line_id')
            missing = rec.rfq_id.line_ids - existing_lines
            for line in missing:
                self.env['el_construction.tender.rfq.bid.line'].create({
                    'rfq_vendor_id': rec.id,
                    'rfq_line_id': line.id,
                })
        return records

    def action_mark_submitted(self):
        for rec in self:
            if not rec.bid_line_ids.filtered(lambda b: b.unit_price):
                raise UserError(_('Enter at least one bid price before marking the vendor as submitted.'))
            rec.write({'state': 'submitted', 'submission_date': fields.Date.context_today(rec)})

    def action_mark_declined(self):
        self.write({'state': 'declined'})

    def action_award(self):
        self.ensure_one()
        return self.rfq_id.action_award_vendor(self)


class ConstructionTenderRfqBidLine(models.Model):
    _name = 'el_construction.tender.rfq.bid.line'
    _description = 'Vendor Bid Line'
    _order = 'id'
    _rec_name = 'rfq_line_id'

    rfq_vendor_id = fields.Many2one('el_construction.tender.rfq.vendor', string='Vendor', required=True, ondelete='cascade', index=True)
    rfq_line_id = fields.Many2one('el_construction.tender.rfq.line', string='Requested Item', required=True, ondelete='cascade', index=True)
    unit_price = fields.Float(string='Unit Price')
    amount = fields.Float(string='Amount', compute='_compute_amount', store=True)
    is_lowest = fields.Boolean(string='Lowest Bid', compute='_compute_is_lowest')
    remarks = fields.Char(string='Remarks')

    _sql_constraints = [
        ('vendor_line_uniq', 'unique(rfq_vendor_id, rfq_line_id)', 'A vendor can only have one bid price per requested item.'),
    ]

    @api.depends('unit_price', 'rfq_line_id.quantity')
    def _compute_amount(self):
        for line in self:
            line.amount = line.unit_price * line.rfq_line_id.quantity

    def _compute_is_lowest(self):
        for line in self:
            siblings = self.search([
                ('rfq_line_id', '=', line.rfq_line_id.id),
                ('rfq_vendor_id.state', 'in', ('submitted', 'awarded')),
                ('unit_price', '>', 0),
            ])
            line.is_lowest = bool(siblings) and line.unit_price == min(siblings.mapped('unit_price'))

    @api.constrains('unit_price')
    def _check_price(self):
        for line in self:
            if line.unit_price < 0:
                raise ValidationError(_('Unit price cannot be negative.'))

    @api.constrains('rfq_vendor_id', 'rfq_line_id')
    def _check_same_rfq(self):
        for line in self:
            if line.rfq_vendor_id.rfq_id != line.rfq_line_id.rfq_id:
                raise ValidationError(_('The bid line must belong to the same RFQ as the vendor.'))
