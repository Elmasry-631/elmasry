from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.addons.el_construction_management.models.workflow_mixin import ConstructionWorkflowMixin


class ConstructionTenderOpportunity(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.tender.opportunity'
    _description = 'Construction Tender (Bid Submitted to Client)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    _ALLOWED = {
        'draft': {'qualification', 'cancelled'},
        'qualification': {'estimating', 'cancelled', 'draft'},
        'estimating': {'review', 'cancelled'},
        'review': {'submitted', 'estimating', 'cancelled'},
        'submitted': {'won', 'lost', 'cancelled'},
        'won': set(),
        'lost': {'estimating'},
        'cancelled': {'draft'},
    }

    name = fields.Char(string='Reference', readonly=True, default='New', copy=False)
    title = fields.Char(string='Tender Title', required=True, tracking=True)
    client_id = fields.Many2one('res.partner', string='Client / Tendering Authority', required=True, tracking=True)
    tender_type = fields.Selection([
        ('public', 'Public Tender'),
        ('private', 'Private Tender'),
        ('direct', 'Direct Negotiation'),
    ], string='Tender Type', default='private', tracking=True)
    reference_no = fields.Char(string="Client's Tender No.")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    user_id = fields.Many2one('res.users', string='Estimator / Responsible', default=lambda self: self.env.user, tracking=True)

    submission_deadline = fields.Datetime(string='Submission Deadline', tracking=True)
    site_visit_date = fields.Datetime(string='Site Visit Date')

    bid_bond_required = fields.Boolean(string='Bid Bond Required')
    bid_bond_amount = fields.Float(string='Bid Bond Amount')
    bid_bond_expiry = fields.Date(string='Bid Bond Expiry')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('qualification', 'Qualification'),
        ('estimating', 'Estimating'),
        ('review', 'Pricing Review'),
        ('submitted', 'Submitted'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    line_ids = fields.One2many('el_construction.tender.line', 'tender_id', string='Priced Items')
    rfq_ids = fields.One2many('el_construction.tender.rfq', 'tender_opportunity_id', string='Subcontractor / Vendor RFQs')
    rfq_count = fields.Integer(compute='_compute_counts')

    total_cost = fields.Float(string='Total Direct Cost', compute='_compute_totals', store=True)
    total_price = fields.Float(string='Total Bid Price', compute='_compute_totals', store=True)
    margin_amount = fields.Float(string='Margin', compute='_compute_totals', store=True)
    margin_percent = fields.Float(string='Margin %', compute='_compute_totals', store=True)

    lost_reason = fields.Text(string='Lost Reason')
    won_date = fields.Date(string='Won Date', readonly=True, copy=False)

    project_id = fields.Many2one('el_construction.project', string='Awarded Project', readonly=True, copy=False)
    sub_project_id = fields.Many2one('el_construction.sub.project', string='Awarded Sub Project', readonly=True, copy=False)

    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('el_construction.tender.opportunity') or 'New'
        return super().create(vals_list)

    def write(self, vals):
        if 'state' in vals and not self._workflow_write_allowed():
            for rec in self:
                if vals['state'] != rec.state:
                    raise UserError(_('Use the workflow buttons to change the Status.'))
        return super().write(vals)

    @api.depends('line_ids.cost_amount', 'line_ids.amount')
    def _compute_totals(self):
        for rec in self:
            rec.total_cost = sum(rec.line_ids.mapped('cost_amount'))
            rec.total_price = sum(rec.line_ids.mapped('amount'))
            rec.margin_amount = rec.total_price - rec.total_cost
            rec.margin_percent = (rec.margin_amount / rec.total_price * 100.0) if rec.total_price else 0.0

    @api.depends('rfq_ids')
    def _compute_counts(self):
        for rec in self:
            rec.rfq_count = len(rec.rfq_ids)

    # Workflow -----------------------------------------------------------
    def action_set_qualification(self):
        self._transition('qualification', self._ALLOWED)

    def action_start_estimating(self):
        self._transition('estimating', self._ALLOWED)

    def action_send_review(self):
        for rec in self:
            if not rec.line_ids:
                raise UserError(_('Add at least one priced item before sending for review.'))
        self._transition('review', self._ALLOWED)

    def action_submit(self):
        self._transition('submitted', self._ALLOWED)

    def action_reset_draft(self):
        self._transition('draft', self._ALLOWED)

    def action_mark_lost(self):
        self._transition('lost', self._ALLOWED)

    def action_cancel(self):
        self._transition('cancelled', self._ALLOWED)

    def action_mark_won(self):
        self.ensure_one()
        self._transition('won', self._ALLOWED)
        self.won_date = fields.Date.context_today(self)
        return self.action_create_project()

    # Conversion -----------------------------------------------------------
    def action_create_project(self):
        """Convert a Won tender into a live Project + Sub Project + BOQ."""
        self.ensure_one()
        if self.project_id:
            return self._open_project_action()
        if self.state != 'won':
            raise UserError(_('Only a Won tender can be converted into a Project.'))

        project = self.env['el_construction.project'].create({
            'name': self.title,
            'company_id': self.company_id.id,
        })
        sub_project = self.env['el_construction.sub.project'].create({
            'name': self.title,
            'project_id': project.id,
            'company_id': self.company_id.id,
            'partner_id': self.client_id.id,
        })
        boq = self.env['el_construction.boq'].create({
            'project_id': project.id,
            'sub_project_id': sub_project.id,
            'company_id': self.company_id.id,
            'description': self.title,
        })
        BoqLine = self.env['el_construction.boq.line']
        for line in self.line_ids:
            boq_line = BoqLine.create({
                'boq_id': boq.id,
                'product_id': line.product_id.id,
                'description': line.description,
                'quantity': line.quantity,
                'uom_id': line.uom_id.id,
                'unit_price': line.unit_price,
            })
            line.boq_line_id = boq_line.id

        self.write({'project_id': project.id, 'sub_project_id': sub_project.id})
        return self._open_project_action()

    def _open_project_action(self):
        self.ensure_one()
        return {
            'name': _('Project'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.project',
            'view_mode': 'form',
            'res_id': self.project_id.id,
        }

    @api.model
    def dashboard_snapshot(self):
        """Lightweight KPI payload consumed by the patched Construction Dashboard."""
        domain = [('company_id', 'in', self.env.companies.ids)]
        tenders = self.sudo().search(domain)
        open_states = ('draft', 'qualification', 'estimating', 'review', 'submitted')
        open_tenders = tenders.filtered(lambda t: t.state in open_states)
        won_tenders = tenders.filtered(lambda t: t.state == 'won')
        lost_tenders = tenders.filtered(lambda t: t.state == 'lost')
        rfq_domain = [
            ('company_id', 'in', self.env.companies.ids),
            ('state', 'in', ('draft', 'sent', 'bidding', 'comparison')),
        ]
        rfq_open_count = self.env['el_construction.tender.rfq'].sudo().search_count(rfq_domain)
        return {
            'tender_total': len(tenders),
            'tender_open': len(open_tenders),
            'tender_won': len(won_tenders),
            'tender_lost': len(lost_tenders),
            'tender_pipeline_value': sum(open_tenders.mapped('total_price')),
            'tender_won_value': sum(won_tenders.mapped('total_price')),
            'rfq_open': rfq_open_count,
        }

    def action_view_rfqs(self):
        self.ensure_one()
        return {
            'name': _('Subcontractor / Vendor RFQs'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.tender.rfq',
            'view_mode': 'list,form',
            'domain': [('tender_opportunity_id', '=', self.id)],
            'context': {'default_tender_opportunity_id': self.id, 'default_company_id': self.company_id.id},
        }


class ConstructionTenderLine(models.Model):
    _name = 'el_construction.tender.line'
    _description = 'Tender Priced Item'
    _order = 'id'
    _rec_name = 'description'

    tender_id = fields.Many2one('el_construction.tender.opportunity', string='Tender', required=True, ondelete='cascade', index=True)
    work_type_id = fields.Many2one('el_construction.work.type', string='Work Type')
    work_sub_type_id = fields.Many2one('el_construction.work.sub.type', string='Work Sub Type',
                                        domain="[('work_type_id', '=', work_type_id)]")
    product_id = fields.Many2one('product.product', string='Product')
    description = fields.Char(string='Description', required=True)
    quantity = fields.Float(string='Quantity', default=1.0)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')

    cost_source_rfq_line_id = fields.Many2one(
        'el_construction.tender.rfq.line', string='Costed From RFQ Line',
        help='If set, the direct unit cost is pulled from the awarded subcontractor/vendor bid on this RFQ line.')
    cost_unit_manual = fields.Float(string='Direct Cost (Manual)')
    cost_unit = fields.Float(string='Direct Unit Cost', compute='_compute_cost_unit', store=True, readonly=False)
    overhead_percent = fields.Float(string='Overhead %', default=10.0)
    profit_percent = fields.Float(string='Profit %', default=10.0)
    unit_price = fields.Float(string='Unit Price', compute='_compute_price', store=True, readonly=False)

    cost_amount = fields.Float(string='Cost Amount', compute='_compute_amounts', store=True)
    amount = fields.Float(string='Bid Amount', compute='_compute_amounts', store=True)

    boq_line_id = fields.Many2one('el_construction.boq.line', string='Converted BOQ Line', readonly=True, copy=False)

    @api.depends('cost_source_rfq_line_id.awarded_unit_price', 'cost_unit_manual')
    def _compute_cost_unit(self):
        for line in self:
            if line.cost_source_rfq_line_id and line.cost_source_rfq_line_id.awarded_unit_price:
                line.cost_unit = line.cost_source_rfq_line_id.awarded_unit_price
            else:
                line.cost_unit = line.cost_unit_manual

    @api.depends('cost_unit', 'overhead_percent', 'profit_percent')
    def _compute_price(self):
        for line in self:
            line.unit_price = line.cost_unit * (1 + line.overhead_percent / 100.0) * (1 + line.profit_percent / 100.0)

    @api.depends('quantity', 'cost_unit', 'unit_price')
    def _compute_amounts(self):
        for line in self:
            line.cost_amount = line.quantity * line.cost_unit
            line.amount = line.quantity * line.unit_price

    @api.constrains('quantity')
    def _check_quantity(self):
        for line in self:
            if line.quantity < 0:
                raise ValidationError(_('Quantity cannot be negative.'))

    @api.onchange('work_type_id')
    def _onchange_work_type_id(self):
        if self.work_sub_type_id and self.work_sub_type_id.work_type_id != self.work_type_id:
            self.work_sub_type_id = False

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.name
            self.uom_id = self.product_id.uom_id
