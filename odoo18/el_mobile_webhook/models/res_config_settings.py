from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    mobile_webhook_endpoint = fields.Char(config_parameter='el_mobile_webhook.endpoint')
    mobile_webhook_secret = fields.Char(config_parameter='el_mobile_webhook.secret', password=True)
    mobile_webhook_timeout = fields.Integer(config_parameter='el_mobile_webhook.timeout', default=10)
    mobile_webhook_retry_limit = fields.Integer(config_parameter='el_mobile_webhook.retry_limit', default=5)

    @api.constrains('mobile_webhook_endpoint', 'mobile_webhook_timeout', 'mobile_webhook_retry_limit')
    def _check_mobile_webhook_settings(self):
        for settings in self:
            if settings.mobile_webhook_endpoint:
                self.env['mobile.webhook.event']._validate_endpoint(settings.mobile_webhook_endpoint)
            if not 1 <= settings.mobile_webhook_timeout <= 120:
                raise ValidationError('Webhook timeout must be between 1 and 120 seconds.')
            if not 1 <= settings.mobile_webhook_retry_limit <= 20:
                raise ValidationError('Webhook retry limit must be between 1 and 20.')
