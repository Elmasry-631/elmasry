from odoo import models, fields, api

class ZKAttendanceSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _name = 'zk.attendance.settings'
    _description = 'ZK Attendance Settings'

    no_checkout_mode = fields.Selection(
        [('default', 'Default Date'), ('shift', 'Work Schedule')],
        string="No Checkout Mode",
        default='default'
    )

    deflt_time = fields.Float(
        string="Default Time",
        default=0.0
    )

    api_ip = fields.Char(
        string="API IP"
    )

    api_port = fields.Char(
        string="API Port",
        help="If port is left empty, the request will be sent without a port number"
    )

    def set_values(self):
        super(ZKAttendanceSettings, self).set_values()
        IrDefault = self.env['ir.default'].sudo()
        IrDefault.set('zk.attendance.settings', 'no_checkout_mode', self.no_checkout_mode)
        IrDefault.set('zk.attendance.settings', 'deflt_time', self.deflt_time)
        IrDefault.set('zk.attendance.settings', 'api_ip', self.api_ip)
        IrDefault.set('zk.attendance.settings', 'api_port', self.api_port)

    @api.model
    def get_values(self):
        res = super(ZKAttendanceSettings, self).get_values()
        IrDefault = self.env['ir.default'].sudo()
        res.update({
            'no_checkout_mode': IrDefault.get('zk.attendance.settings', 'no_checkout_mode') or 'default',
            'deflt_time': IrDefault.get('zk.attendance.settings', 'deflt_time') or 0.0,
            'api_ip': IrDefault.get('zk.attendance.settings', 'api_ip'),
            'api_port': IrDefault.get('zk.attendance.settings', 'api_port'),
        })
        return res
