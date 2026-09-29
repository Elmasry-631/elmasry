# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class InterCompanyConfig(models.Model):
    _name = 'inter.company.config'
    _description = 'Inter Company Configuration'
    _rec_name = 'display_name'
    _order = 'source_company_id, dest_company_id'

    source_company_id = fields.Many2one(
        'res.company',
        string='Source Company',
        required=True,
        ondelete='cascade',
    )
    dest_company_id = fields.Many2one(
        'res.company',
        string='Destination Company',
        required=True,
        ondelete='cascade',
    )
    display_name = fields.Char(compute='_compute_display_name', store=True)
    apply_on = fields.Selection(
        [
            ('sale', 'Sale Order Only'),
            ('purchase', 'Purchase Order Only'),
            ('both', 'Both Sale & Purchase Order'),
        ],
        string='Apply On',
        default='both',
        required=True,
    )
    link_document = fields.Boolean(
        string='Link InterCompany Document',
        default=True,
        help='Show links between the inter-company transaction and generated documents.',
    )
    auto_validate_picking = fields.Boolean(
        string='Auto Validate Picking/Receipt',
        help='Automatically validate generated delivery and receipt transfers.',
    )
    auto_create_invoice = fields.Boolean(
        string='Auto Create Invoice/Bill',
        help='Automatically create the customer invoice and vendor bill.',
    )
    auto_validate_invoice = fields.Boolean(
        string='Auto Validate Invoice/Bill',
        help='Automatically post generated accounting documents.',
    )
    active = fields.Boolean(default=True)

    _unique_company_pair = models.Constraint(
        'unique(source_company_id, dest_company_id)',
        'Only one inter-company rule is allowed for the same company pair.',
    )
    _different_company_pair = models.Constraint(
        'check(source_company_id != dest_company_id)',
        'Source company and destination company must be different.',
    )

    @api.depends('source_company_id', 'dest_company_id')
    def _compute_display_name(self):
        """Build a readable rule name from the configured company pair."""
        for config in self:
            if config.source_company_id and config.dest_company_id:
                config.display_name = _('%(source)s -> %(dest)s') % {
                    'source': config.source_company_id.display_name,
                    'dest': config.dest_company_id.display_name,
                }
            else:
                config.display_name = _('New Inter Company Rule')

    @api.constrains('source_company_id', 'dest_company_id')
    def _check_company_warehouses(self):
        """Ensure both companies have an inter-company warehouse configured."""
        for config in self:
            missing = (
                config.source_company_id | config.dest_company_id
            ).filtered(lambda company: not company.inter_company_warehouse_id)
            if missing:
                raise ValidationError(
                    _('Configure an inter-company warehouse for: %s')
                    % ', '.join(missing.mapped('display_name'))
                )

    @api.model
    def _find_for_sale(self, source_company, customer):
        """Return the active sale rule for a source company/customer pair."""
        company = self._company_from_partner(customer)
        if not company or company == source_company:
            return self.browse()
        return self.search([
            ('source_company_id', '=', source_company.id),
            ('dest_company_id', '=', company.id),
            ('apply_on', 'in', ('sale', 'both')),
            ('active', '=', True),
        ], limit=1)

    @api.model
    def _find_for_purchase(self, dest_company, vendor):
        """Return the active purchase rule for a destination company/vendor pair."""
        company = self._company_from_partner(vendor)
        if not company or company == dest_company:
            return self.browse()
        return self.search([
            ('source_company_id', '=', company.id),
            ('dest_company_id', '=', dest_company.id),
            ('apply_on', 'in', ('purchase', 'both')),
            ('active', '=', True),
        ], limit=1)

    @api.model
    def _company_from_partner(self, partner):
        """Resolve a company from a commercial partner used on SO/PO documents."""
        if not partner:
            return self.env['res.company']
        commercial_partner = partner.commercial_partner_id
        return self.env['res.company'].search([
            ('partner_id', '=', commercial_partner.id),
        ], limit=1)
