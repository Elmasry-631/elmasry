import datetime
from email.policy import default

from odoo import fields, models, api


class ChangeState(models.TransientModel):
    _name = 'change.state'
    _description = 'Description'

    property_id = fields.Many2one('test.app.odoo')
    reason = fields.Text()
    date_today = fields.Datetime(default=datetime.datetime.now())
    state = fields.Selection([
        ('draft','Draft'),
        ('pending','Pending'),
        ('sold','Sold'),
    ], default='draft')



    def action_confirm(self):
        print("from action record")
        if self.property_id.state == 'closed':
            self.property_id.state == self.state
            self.property_id.create_history_record('closed', self.state, self.reason)
