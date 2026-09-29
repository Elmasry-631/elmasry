from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Deduction(models.Model):
    _name = 'deduction.deduction'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Deduction'
    _rec_name='employee_id'

    employee_id = fields.Many2one('hr.employee', required=True, tracking=1, domain=lambda l: l.employee_id_domain(), ondelete='restrict')
    vehicle_id = fields.Many2one(
        'fleet.vehicle',
        string='Vehicle',
        compute='_compute_vehicle_id',
        tracking=True,
        store=True
    )
    date = fields.Date(required=True, tracking=2)
    # amount_type = fields.Selection([
    #     ('fixed', 'Fixed Amount'),
    # ], string="Deduction Type", required=True, tracking=3)
    amount = fields.Monetary(string='Amount', tracking=3)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve1', 'First Approve'),
        ('approve2', 'Second Approve'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('done', 'Done'),
    ], default='draft', tracking=4)

    deduction_type = fields.Selection([
        ('deduction', 'Deduction'),
        ('salary_adv', 'Salary Advance'),
        ('housing', 'Housing'),
        ('gas', 'Gasoline'),
        ('traffic_violations', 'Traffic Violations'),
    ], tracking=5, required=True, string='Deduction Type')

    liter_value = fields.Monetary(string='Liter Value', tracking=6)
    litres_no = fields.Float(string='Number of Litres', tracking=7)
    litres_total_cost = fields.Monetary(string='Litres Total Cost', tracking=8, compute='_compute_litres_total_cost', store=True)

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        # default=lambda self: self.env.company.id,
        related='employee_id.company_id',
        store=True,
        index=True,
        required=False
    )
    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id
    )

    @api.depends('employee_id')
    def _compute_vehicle_id(self):
        for rec in self:
            rec.vehicle_id = False
            vehicle_id = self.env['fleet.vehicle'].search([
                ('driver_employee_id', '=', rec.employee_id.id),
            ], limit=1)
            if vehicle_id:
                rec.vehicle_id = vehicle_id.id

    @api.depends('liter_value', 'litres_no')
    def _compute_litres_total_cost(self):
        for rec in self:
            rec.litres_total_cost = rec.litres_no * rec.liter_value

    def employee_id_domain(self):
        current_user_id = self.env.user.id
        admins = self.get_admins()
        if current_user_id not in admins:
            return ['|', ('parent_id.user_id', '=', current_user_id), ('user_id', '=', current_user_id)]
        else:
            return []

    def button_approve1(self):
        self.state = 'approve1'

    def button_approve2(self):
        self.state = 'approve2'

    def button_approve(self):
        self.state = 'approved'

    def button_reject(self):
        if self.env.user.has_group('deduction_management.group_deduction_management_approver') and self.state not in ('approve1', 'draft'):
            raise ValidationError(_('You cannot reject this record as it has been moved to the management.'))
        self.state = 'rejected'

    def action_reset_to_draft(self):
        if self.env.user.has_group('deduction_management.group_deduction_management_approver') and self.state != 'approve1':
            raise ValidationError(_('You cannot reset this record to draft as it has been moved to the management.'))
        self.state = 'draft'

    def get_admins(self):
        users = (
            self.env.ref('deduction_management.group_deduction_management_manager').user_ids |
            self.env.ref('deduction_management.group_deduction_management_hr').user_ids
        )
        return users.ids

    def write(self, vals_list):
        res = super(Deduction, self).write(vals_list)
        for rec in self:
            current_user_id = rec.env.user.id
            admins = rec.get_admins()
            if rec.state in ('approve2', 'approved', 'rejected') and current_user_id not in admins:
                raise ValidationError(
                    _("You cannot edit current record as its status is 'approved', reset it to draft or contact your administrator instead."))

        return res

    def unlink(self):
        for rec in self:
            if rec.state in ('approve1', 'approve2', 'approved'):
                raise ValidationError(_("You can only delete records in (Draft, Rejected) status."))
        return super(Deduction, self).unlink()
