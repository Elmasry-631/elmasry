from odoo import fields, models, _
from odoo.exceptions import UserError


class GenerateCodesWizard(models.TransientModel):
    _name = 'generate.codes.wizard'
    _description = 'Generate E-Book Codes'

    product_tmpl_id = fields.Many2one('product.template', string='E-Book', required=True)
    generation_mode = fields.Selection([
        ('auto', 'Auto Generate (Random)'),
        ('manual', 'Manual Entry'),
    ], string='Generation Mode', default='auto', required=True)
    code_count = fields.Integer(string='Number of Codes', default=10)
    manual_codes = fields.Text(string='Manual Codes', help='One code per line')
    max_access = fields.Integer(string='Max Access per Code', default=1)

    def action_generate(self):
        self.ensure_one()
        if self.generation_mode == 'auto':
            if self.code_count <= 0 or self.code_count > 1000:
                raise UserError(_('Code count must be between 1 and 1000.'))
            manual = None
        else:
            if not self.manual_codes:
                raise UserError(_('Please enter at least one code.'))
            manual = self.manual_codes.strip().split('\n')
            self.code_count = len(manual)

        codes = self.env['ebook.code'].generate_codes(
            self.product_tmpl_id.id,
            self.code_count,
            generation_mode=self.generation_mode,
            manual_codes=manual,
        )
        # Set max_access
        if self.max_access != 1:
            codes.write({'max_access': self.max_access})

        return {
            'type': 'ir.actions.act_window',
            'name': _('Generated Codes'),
            'res_model': 'ebook.code',
            'view_mode': 'list,form',
            'domain': [('id', 'in', codes.ids)],
            'target': 'current',
        }
