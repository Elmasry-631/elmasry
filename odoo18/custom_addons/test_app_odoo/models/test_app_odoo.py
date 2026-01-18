from email.policy import default

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class TestAppOdoo(models.Model):
    _name = 'test.app.odoo'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char(default="New", readonly=True)
    name = fields.Char()
    description = fields.Text()
    active = fields.Boolean(default=True)
    value = fields.Integer()
    expected_price = fields.Float()
    sales_price = fields.Float()
    deference = fields.Float(readonly=1, compute="_compute_diff")
    selling_date = fields.Date()
    expected_date = fields.Date()
    is_late =fields.Boolean(store=True)


    test_app_two_id = fields.Many2one('test.app.two', string="Test App Two")

    tag_ids = fields.Many2many('tag', string="Tags")

    state = fields.Selection([

        ('draft','Draft'),
        ('pending','Pending'),
        ('sold','Sold'),
        ('closed','Closed'),
    ], default='draft')




    line_ids = fields.One2many('test.line','property_id')

    @api.depends('expected_price','sales_price')
    def _compute_diff(self):
        for rec in self:
            rec.deference = rec.expected_price - rec.sales_price


    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            if rec.expected_price < 0:
                return {
                    'warning':{
                        'title':'Expected Price Warning',
                        'message':'Expected Price must be greater than zero'
                    }
                }



    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state, 'draft')
            rec.state ='draft'

    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state, 'pending')
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold')
            rec.state = 'sold'

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.state = 'closed'



    def _check_expected_date(self):
        test_app = self.search([])
        for rec in test_app:
            if rec.expected_date > rec.selling_date and fields.Date.today():
                rec.is_late = True




    @api.constrains('value')
    def _check_value(self):
        for rec in self:
            if rec.value <= 0:
                raise ValidationError("Value must be greater than zero.")


    def create_history_record(self, old_state, new_state):
        for rec in self:
            rec.env['test.history'].create({
                'user_id': rec.env.uid,
                'property_id' : rec.id,
                'old_state': old_state,
                'new_state': new_state,

            })


    def action_open_change_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('test_app_odoo.action_open_wizard')
        action['context'] = {'default_property_id' : self.id }
        return action

    def action_open_invoice_account(self):
        action = self.env['ir.actions.actions']._for_xml_id('account.view_move_form')
        action['context'] = {'default_id': self.id}
        return action



    @api.model_create_multi
    def create(self,vals):
        res = super(TestAppOdoo, self).create(vals)
        print("this is from create method")
        return res

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None):
        res = super(TestAppOdoo, self)._search(domain, offset=0, limit=None, order=None)
        print("this is from search method")
        return res



    def write(self, vals):
        res = super(TestAppOdoo, self).write(vals)
        print("this is from update method")
        return res


    def unlink(self):

        res = super(TestAppOdoo, self).unlink()
        print("this i delete method")
        return res



    def create(self, vals):
        res = super(TestAppOdoo, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('test_seq')
        return res




class TestLine(models.Model):
    _name = 'test.line'

    property_id = fields.Many2one('test.app.odoo')
    area = fields.Float()
    description = fields.Text()

