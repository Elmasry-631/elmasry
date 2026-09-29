from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError

from .workflow_mixin import ConstructionWorkflowMixin


class ConstructionProjectControls(ConstructionWorkflowMixin, models.Model):
    _inherit = 'el_construction.project'

    # Integrated Odoo Inventory / Project Site stock dimensions.
    site_location_id = fields.Many2one('stock.location', string='Project Site Stock Location', copy=False, index=True)
    consumption_location_id = fields.Many2one('stock.location', string='Project Consumption Location', copy=False, index=True)
    material_issue_ids = fields.One2many('el_construction.material.issue', 'project_id', string='Material Stock Operations')
    material_issue_count = fields.Integer(compute='_compute_material_issue_count')

    @api.depends('material_issue_ids')
    def _compute_material_issue_count(self):
        for project in self:
            project.material_issue_count = len(project.material_issue_ids)

    def _ensure_stock_locations(self):
        Location = self.env['stock.location']
        for project in self:
            if not project.warehouse_id:
                continue
            if project.warehouse_id.company_id and project.warehouse_id.company_id != project.company_id:
                raise ValidationError(_('Project warehouse company must match the Project company.'))
            parent = project.warehouse_id.lot_stock_id
            if project.site_location_id:
                if project.site_location_id.company_id and project.site_location_id.company_id != project.company_id:
                    raise ValidationError(_('Project Site Stock Location belongs to another company. Migrate the existing stock location instead of creating a replacement.'))
            else:
                project.site_location_id = Location.create({
                    'name': '%s - Site' % project.name,
                    'location_id': parent.id,
                    'usage': 'internal',
                    'company_id': project.company_id.id,
                })
            if project.consumption_location_id:
                if project.consumption_location_id.company_id and project.consumption_location_id.company_id != project.company_id:
                    raise ValidationError(_('Project Consumption Location belongs to another company. Migrate the existing stock location instead of creating a replacement.'))
            else:
                project.consumption_location_id = Location.create({
                    'name': '%s - Consumption' % project.name,
                    'location_id': project.site_location_id.id,
                    'usage': 'production',
                    'company_id': project.company_id.id,
                })
        return True

    def action_initialize_stock_locations(self):
        self._ensure_stock_locations()
        return True

    def action_view_material_issues(self):
        self.ensure_one()
        return {
            'name': _('Material Stock Operations'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.material.issue',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }

    def write(self, vals):
        if 'warehouse_id' in vals:
            new_warehouse = self.env['stock.warehouse'].browse(vals['warehouse_id']) if vals['warehouse_id'] else self.env['stock.warehouse']
            for project in self:
                if project.site_location_id and project.warehouse_id and project.warehouse_id != new_warehouse:
                    raise UserError(_('The Project Warehouse cannot be changed after stock locations have been created. Migrate/close the Project stock first.'))
        if 'company_id' in vals:
            new_company = self.env['res.company'].browse(vals['company_id']) if vals['company_id'] else self.env['res.company']
            for project in self:
                if project.company_id != new_company:
                    operational_exists = any([
                        project.sub_project_ids,
                        project.permit_ids,
                        project.boq_ids,
                        project.budget_ids,
                        project.phase_ids,
                        project.work_order_ids,
                        project.material_requisition_ids,
                        project.task_ids,
                        project.variation_order_ids,
                        project.extra_expense_ids,
                        project.material_issue_ids,
                        self.env['el_construction.progress.billing'].search_count([('project_id', '=', project.id)]),
                        self.env['el_construction.subcontract'].search_count([('project_id', '=', project.id)]),
                    ])
                    if operational_exists:
                        raise UserError(_('The Project Company cannot be changed after construction records exist. Use a controlled company-transfer/migration process instead.'))
        res = super().write(vals)
        if 'warehouse_id' in vals or 'company_id' in vals or 'name' in vals:
            self._ensure_stock_locations()
        return res

    enforce_closure_gates = fields.Boolean(string='Enforce Closure Gates', default=True, tracking=True)
    closure_gate_summary = fields.Text(string='Closure Gate Summary', compute='_compute_closure_gate_summary')
    variation_order_ids = fields.One2many('el_construction.variation.order', 'project_id', string='Variation Orders')
    cost_entry_ids = fields.One2many('el_construction.cost.entry', 'project_id', string='Cost Entries')
    approved_variation_amount = fields.Monetary(string='Approved Variations', compute='_compute_control_totals', currency_field='currency_id')
    committed_cost = fields.Monetary(string='Committed Cost', compute='_compute_control_totals', currency_field='currency_id')
    actual_cost = fields.Monetary(string='Actual Cost', compute='_compute_control_totals', currency_field='currency_id')
    forecast_cost = fields.Monetary(string='Forecast Cost', compute='_compute_control_totals', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', store=True, readonly=True)

    @api.depends('variation_order_ids.amount', 'variation_order_ids.state', 'cost_entry_ids.amount', 'cost_entry_ids.cost_type')
    def _compute_control_totals(self):
        for rec in self:
            rec.approved_variation_amount = sum(rec.variation_order_ids.filtered(lambda x: x.state == 'approved').mapped('amount'))
            rec.committed_cost = sum(rec.cost_entry_ids.filtered(lambda x: x.cost_type == 'committed').mapped('amount'))
            rec.actual_cost = sum(rec.cost_entry_ids.filtered(lambda x: x.cost_type == 'actual').mapped('amount'))
            rec.forecast_cost = sum(rec.cost_entry_ids.filtered(lambda x: x.cost_type == 'forecast').mapped('amount'))

    @api.depends('sub_project_ids.state', 'task_ids.state', 'work_order_ids.state', 'material_requisition_ids.state', 'budget_ids.state', 'variation_order_ids.state')
    def _compute_closure_gate_summary(self):
        for rec in self:
            rec.closure_gate_summary = '; '.join(rec._closure_gate_messages()) or _('All closure gates passed.')

    def _closure_gate_messages(self):
        self.ensure_one()
        messages = []
        if self.sub_project_ids and any(sp.state != 'handover' for sp in self.sub_project_ids):
            messages.append(_('All Sub Projects must reach Handover.'))
        if self.task_ids and any(t.state not in ('done', 'cancelled') for t in self.task_ids):
            messages.append(_('All Tasks must be Done or Cancelled.'))
        if self.work_order_ids and any(w.state not in ('done', 'cancelled') for w in self.work_order_ids):
            messages.append(_('All Work Orders must be Done or Cancelled.'))
        if self.material_requisition_ids and any(m.state not in ('done', 'cancelled', 'withdrawal') for m in self.material_requisition_ids):
            messages.append(_('All Material Requisitions must be closed, cancelled, or withdrawn.'))
        if self.budget_ids and any(b.state not in ('done', 'cancelled') for b in self.budget_ids):
            messages.append(_('All Budgets must be Done or Cancelled.'))

        checks = self.env['el_construction.quality.check'].search_count([
            ('project_id', '=', self.id),
            ('state', 'not in', ('closed', 'cancelled')),
        ])
        if checks:
            messages.append(_('All Quality Checks must be Closed or Cancelled.'))
        ncrs = self.env['el_construction.ncr'].search_count([
            ('project_id', '=', self.id),
            ('state', 'not in', ('closed', 'cancelled')),
        ])
        if ncrs:
            messages.append(_('All NCRs must be Closed or Cancelled.'))
        capas = self.env['el_construction.capa'].search_count([
            ('project_id', '=', self.id),
            ('state', '=', 'open'),
        ])
        if capas:
            messages.append(_('All CAPA actions must be completed or cancelled.'))

        open_variations = self.variation_order_ids.filtered(
            lambda v: v.state not in ('approved', 'rejected', 'cancelled')
        )
        if open_variations:
            messages.append(_('All Variation Orders must be Approved, Rejected, or Cancelled.'))

        all_subcontracts = self.env['el_construction.subcontract'].search([('project_id', '=', self.id)])
        open_subcontracts = all_subcontracts.filtered(lambda subcontract: subcontract.state not in ('completed', 'cancelled'))
        if open_subcontracts:
            messages.append(_('All Subcontracts must be Completed or Cancelled.'))
        unpaid_vendor_bills = all_subcontracts.mapped('vendor_bill_ids').filtered(
            lambda move: move.state == 'posted' and move.payment_state not in ('paid', 'reversed')
        )
        if unpaid_vendor_bills:
            messages.append(_('All posted Subcontract Vendor Bills must be Paid or Reversed.'))

        all_progress = self.env['el_construction.progress.billing'].search([('project_id', '=', self.id)])
        open_progress = all_progress.filtered(lambda billing: billing.state != 'completed')
        if open_progress:
            messages.append(_('All Progress Billings must be Completed.'))
        unpaid_customer_invoices = all_progress.mapped('invoice_link_ids').filtered(
            lambda move: move.state == 'posted' and move.payment_state not in ('paid', 'reversed')
        )
        if unpaid_customer_invoices:
            messages.append(_('All posted Progress Billing Customer Invoices must be Paid or Reversed.'))

        expenses = self.env['el_construction.extra.expense'].search([
            ('project_id', '=', self.id),
            ('state', 'not in', ('approved', 'cancelled')),
        ])
        if expenses:
            messages.append(_('All Extra Expenses must be Approved or Cancelled.'))

        mreqs = self.material_requisition_ids
        open_purchase_orders = mreqs.mapped('purchase_order_link_ids').filtered(
            lambda po: po.state not in ('done', 'cancel')
        )
        if open_purchase_orders:
            messages.append(_('All Material Requisition Purchase Orders must be Done or Cancelled.'))
        open_pickings = mreqs.mapped('picking_link_ids').filtered(
            lambda picking: picking.state not in ('done', 'cancel')
        )
        if open_pickings:
            messages.append(_('All Material Requisition Stock Pickings must be Done or Cancelled.'))

        permits = self.env['el_construction.permit'].search_count([
            ('project_id', '=', self.id),
            ('state', '=', 'pending'),
        ])
        if permits:
            messages.append(_('All pending Project Permits must be Approved, Rejected, or Expired.'))
        return messages

    def action_complete(self):
        for rec in self:
            rec._lock_records()
            rec.invalidate_recordset()
            if rec.enforce_closure_gates:
                messages = rec._closure_gate_messages()
                if messages:
                    raise UserError(_('Project cannot be completed:\n• %s') % '\n• '.join(messages))
        return super().action_complete()
    # Project cost-control services.

    analytic_account_id = fields.Many2one('account.analytic.account', string='Project Analytic Account', ondelete='restrict')

    def action_rebuild_cost_snapshot(self):
        if not self.env.user.has_group('el_construction_management.group_construction_manager'):
            raise UserError(_('Only Construction Managers can rebuild project cost snapshots.'))
        """Rebuild idempotent project cost entries from the construction source documents.
        This is deliberately explicit: it never deletes user-entered cost entries.
        """
        Cost = self.env['el_construction.cost.entry']
        for project in self:
            # Purchase commitments through Material Requisitions / Purchase Orders.
            mreqs = self.env['el_construction.material.requisition'].search([('project_id', '=', project.id)])
            purchase_orders = mreqs.mapped('purchase_order_link_ids')
            source_keys = set(
                Cost.search([
                    ('project_id', '=', project.id),
                    ('cost_type', '=', 'committed'),
                    ('source_model', '=', 'purchase.order'),
                    ('source_res_id', 'in', purchase_orders.ids),
                ]).mapped(lambda entry: entry.source_res_id)
            ) if purchase_orders else set()
            for po in purchase_orders.filtered(lambda record: record.id not in source_keys):
                Cost.create_from_source({
                    'name': _('PO Commitment: %s') % po.name,
                    'project_id': project.id,
                    'sub_project_id': po.material_requisition_id.sub_project_id.id,
                    'date': po.date_order.date() if po.date_order else fields.Date.context_today(project),
                    'cost_type': 'committed', 'cost_category': 'material',
                    'amount': po.amount_untaxed,
                    'analytic_account_id': project.analytic_account_id.id,
                    'source_model': 'purchase.order', 'source_res_id': po.id, 'source_ref': po.name,
                })
            # Posted vendor bills linked to construction MREQs/subcontracts.
            moves = self.env['account.move'].search([
                ('company_id', '=', project.company_id.id), ('state', '=', 'posted'),
                ('move_type', '=', 'in_invoice'),
            ])
            moves = moves.filtered(lambda m: project.id in m.invoice_line_ids.mapped('purchase_line_id.order_id.material_requisition_id.project_id').ids or (m.construction_subcontract_id and m.construction_subcontract_id.project_id.id == project.id))
            source_keys = set(
                Cost.search([
                    ('project_id', '=', project.id),
                    ('cost_type', '=', 'actual'),
                    ('source_model', '=', 'account.move'),
                    ('source_res_id', 'in', moves.ids),
                ]).mapped(lambda entry: entry.source_res_id)
            ) if moves else set()
            for move in moves.filtered(lambda record: record.id not in source_keys):
                Cost.create_from_source({
                    'name': _('Vendor Bill: %s') % move.name,
                    'project_id': project.id,
                    'date': move.invoice_date or fields.Date.context_today(project),
                    'cost_type': 'actual', 'cost_category': 'subcontract' if move.construction_subcontract_id else 'material',
                    'amount': move.amount_untaxed,
                    'analytic_account_id': project.analytic_account_id.id,
                    'source_model': 'account.move', 'source_res_id': move.id, 'source_ref': move.name,
                })
            # Construction timesheets are actual labour cost placeholders; the amount uses
            # the employee hourly cost when available, otherwise zero rather than inventing a rate.
            timesheets = self.env['el_construction.timesheet'].search([('project_id', '=', project.id)])
            source_keys = set(
                Cost.search([
                    ('project_id', '=', project.id),
                    ('cost_type', '=', 'actual'),
                    ('source_model', '=', 'el_construction.timesheet'),
                    ('source_res_id', 'in', timesheets.ids),
                ]).mapped(lambda entry: entry.source_res_id)
            ) if timesheets else set()
            for ts in timesheets.filtered(lambda record: record.id not in source_keys):
                hourly = ts.employee_id.hourly_cost if 'hourly_cost' in ts.employee_id._fields else 0.0
                Cost.create_from_source({
                    'name': _('Labour: %s') % (ts.employee_id.name or ts.display_name),
                    'project_id': project.id, 'date': ts.date,
                    'cost_type': 'actual', 'cost_category': 'labour', 'amount': ts.hours * hourly,
                    'analytic_account_id': project.analytic_account_id.id,
                    'source_model': 'el_construction.timesheet', 'source_res_id': ts.id, 'source_ref': ts.display_name,
                })
        return True

    # Project dashboard aggregation service.

    @api.model
    def dashboard_snapshot(self, project_id=False, sub_project_id=False):
        """Return dashboard aggregates for one consistent Project/Sub Project scope."""
        if sub_project_id:
            sub_project = self.env['el_construction.sub.project'].browse(sub_project_id).exists()
            if not sub_project:
                raise UserError(_('The selected Sub Project no longer exists.'))
            derived_project_id = sub_project.project_id.id
            if project_id and project_id != derived_project_id:
                raise ValidationError(_('The selected Project and Sub Project do not belong to the same scope.'))
            project_id = derived_project_id
        pd = [('id', '=', project_id)] if project_id else []
        spd = [('project_id', '=', project_id)] if project_id else []
        if sub_project_id:
            spd.append(('id', '=', sub_project_id))
        d = []
        if project_id:
            d.append(('project_id', '=', project_id))
        if sub_project_id:
            d.append(('sub_project_id', '=', sub_project_id))
        def counts(model, domain, field='state'):
            rows = self.env[model].read_group(domain, [field], [field], lazy=False)
            return {r.get(field): r.get('__count', 0) for r in rows}
        ps = counts('el_construction.project', pd)
        sps = counts('el_construction.sub.project', spd)
        mrs = counts('el_construction.material.requisition', d)
        po_domain = [('material_requisition_id', '!=', False)] + ([('material_requisition_id.project_id', '=', project_id)] if project_id else []) + ([('material_requisition_id.sub_project_id', '=', sub_project_id)] if sub_project_id else [])
        po_count = self.env['purchase.order'].search_count(po_domain)
        pick_base = [('picking_type_code', '=', 'internal'), ('material_requisition_id', '!=', False)] + ([('material_requisition_id.project_id', '=', project_id)] if project_id else []) + ([('material_requisition_id.sub_project_id', '=', sub_project_id)] if sub_project_id else [])
        picks = counts('stock.picking', pick_base)
        projects = self.search_read(pd, ['name','date_start','date_end','state'], limit=10, order='id desc')
        subprojects = self.env['el_construction.sub.project'].search_read(spd, ['name','reference','date_start','date_end','state','project_id'], limit=10, order='id desc')
        workorders = self.env['el_construction.work.order'].search_read(d, ['name','material_total','equipment_total','labour_total','overhead_total'], limit=10, order='id asc')
        return {'project_count': sum(ps.values()), 'project_status': ps, 'sub_project_count': sum(sps.values()), 'sub_project_status': sps,
                'mreq_count': sum(mrs.values()), 'mreq_status': mrs, 'phase_count': self.env['el_construction.phase'].search_count(d),
                'work_order_count': self.env['el_construction.work.order'].search_count(d), 'budget_count': self.env['el_construction.budget'].search_count(d),
                'po_count': po_count, 'it_count': sum(picks.values()), 'it_status': picks,
                'projects': projects, 'sub_projects': subprojects, 'work_orders': workorders}

    # Project baseline revision action.

    def action_create_baseline_revision(self, reason):
        self.ensure_one()
        if not reason or not reason.strip(): raise UserError(_('A baseline revision reason is required.'))
        last = self.env['el_construction.task.baseline.revision'].search([('project_id', '=', self.id)], order='revision_no desc', limit=1)
        no = (last.revision_no if last else 0) + 1
        rev = self.env['el_construction.task.baseline.revision'].create({'name': '%s-BL%s' % (self.name, no), 'project_id': self.id, 'revision_no': no, 'reason': reason})
        rev.line_ids = [(0, 0, {'task_id': t.id, 'baseline_start': t.date_start, 'baseline_end': t.date_end, 'baseline_hours': t.planned_hours}) for t in self.task_ids]
        return rev
