from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError
from psycopg2 import IntegrityError



class ConstructionCostEntry(models.Model):
    _name = 'el_construction.cost.entry'
    _description = 'Construction Cost Entry'
    _order = 'date desc, id desc'

    name = fields.Char(required=True)
    project_id = fields.Many2one('el_construction.project', required=True, index=True, ondelete='restrict')
    sub_project_id = fields.Many2one('el_construction.sub.project', index=True, ondelete='restrict')
    company_id = fields.Many2one(related='project_id.company_id', store=True, index=True)
    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    date = fields.Date(default=fields.Date.context_today, required=True, index=True)
    cost_type = fields.Selection([('committed','Committed'),('actual','Actual'),('forecast','Forecast')], required=True, index=True)
    cost_category = fields.Selection([('material','Material'),('labour','Labour'),('equipment','Equipment'),('subcontract','Subcontract'),('overhead','Overhead'),('other','Other')], required=True)
    amount = fields.Monetary(required=True, currency_field='currency_id')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    source_model = fields.Char(readonly=True, copy=False)
    source_res_id = fields.Integer(readonly=True, copy=False)
    source_ref = fields.Char(readonly=True, copy=False)
    notes = fields.Text()

    _source_unique = models.Constraint(

        'unique(source_model, source_res_id, cost_type, project_id)',

        'The same source cannot create the same project cost entry twice.',

    )
    @api.model
    def create_from_source(self, vals):
        """Create an idempotent system cost entry from one business source.

        The database constraint is the final concurrency guard; the pre-check
        avoids unnecessary inserts in the normal path. A savepoint converts a
        concurrent duplicate into a harmless no-op without aborting the parent
        transaction.
        """
        source_model = vals.get('source_model')
        source_res_id = vals.get('source_res_id')
        project_id = vals.get('project_id')
        cost_type = vals.get('cost_type')
        if not all((source_model, source_res_id, project_id, cost_type)):
            raise ValidationError(_('System cost entries require a source model, source record, project, and cost type.'))
        existing = self.search([
            ('source_model', '=', source_model),
            ('source_res_id', '=', source_res_id),
            ('project_id', '=', project_id),
            ('cost_type', '=', cost_type),
        ], limit=1)
        if existing:
            return existing
        try:
            with self.env.cr.savepoint():
                return self.create(vals)
        except IntegrityError:
            return self.search([
                ('source_model', '=', source_model),
                ('source_res_id', '=', source_res_id),
                ('project_id', '=', project_id),
                ('cost_type', '=', cost_type),
            ], limit=1)

    @api.constrains('project_id', 'sub_project_id', 'analytic_account_id', 'amount')
    def _check_cost_context(self):
        for rec in self:
            if rec.amount < 0:
                raise ValidationError(_('Project cost amount cannot be negative.'))
            if rec.sub_project_id and rec.sub_project_id.project_id != rec.project_id:
                raise ValidationError(_('Cost Sub Project must belong to the Cost Project.'))
            if rec.analytic_account_id and rec.analytic_account_id.company_id and rec.analytic_account_id.company_id != rec.company_id:
                raise ValidationError(_('Cost Analytic Account must belong to the same Company.'))
