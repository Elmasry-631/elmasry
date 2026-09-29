from odoo import fields, models, api, _

class InvestmentContact(models.Model):
    _inherit = "res.partner"
    _description = "Codes of contact in groups"

    employee_code = fields.Char(string="Employee Code")
    customer_code = fields.Char(string="Customer Code")
    vendor_code = fields.Char(string="Vendor Code")
    investor_code = fields.Char(string="Investors Code")

    employee_code_check = fields.Boolean(string="Employee")
    customer_code_check = fields.Boolean(string="Customer")
    vendor_code_check = fields.Boolean(string="Vendor")
    investor_code_check = fields.Boolean(string="Investor")


    club_id = fields.Many2one('investment.club' )



    # =============================================
    # 1) default_get - Automatically from customer/vendor lists
    # =============================================
    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        ctx = self.env.context

        # When added from the customer list
        if ctx.get('default_customer_rank') or ctx.get('search_default_customer'):
            defaults['customer_code_check'] = True

        # When added from the vendor list
        if ctx.get('default_supplier_rank') or ctx.get('search_default_supplier'):
            defaults['vendor_code_check'] = True

        # Comment translated/normalized to English.
        if ctx.get('default_employee_code_check'):
            defaults['employee_code_check'] = True

        return defaults

    # =============================================
    # 2) onchange - UI Only before saving
    # =============================================
    @api.onchange('employee_code_check', 'customer_code_check', 'vendor_code_check')
    def _onchange_check_codes(self):
        # --- Employee ---
        if self.employee_code_check and not self.employee_code:
            self.employee_code = self.env['ir.sequence'].next_by_code('employee.code') or _('New')
        elif not self.employee_code_check and self.employee_code:
            self.employee_code = False  # ← Remove the code Details Details Details checkbox

        # --- Customer ---
        if self.customer_code_check and not self.customer_code:
            self.customer_code = self.env['ir.sequence'].next_by_code('customer.code') or _('New')
        elif not self.customer_code_check and self.customer_code:
            self.customer_code = False

        # --- Vendor ---
        if self.vendor_code_check and not self.vendor_code:
            self.vendor_code = self.env['ir.sequence'].next_by_code('vendor.code') or _('New')
        elif not self.vendor_code_check and self.vendor_code:
            self.vendor_code = False

    # =============================================
    # 3) create - When the record is created
    # =============================================
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Employee
            if vals.get('employee_code_check') and not vals.get('employee_code'):
                vals['employee_code'] = self.env['ir.sequence'].next_by_code('employee.code') or _('New')
            # Customer
            if vals.get('customer_code_check') and not vals.get('customer_code'):
                vals['customer_code'] = self.env['ir.sequence'].next_by_code('customer.code') or _('New')
            # Vendor
            if vals.get('vendor_code_check') and not vals.get('vendor_code'):
                vals['vendor_code'] = self.env['ir.sequence'].next_by_code('vendor.code') or _('New')
        return super().create(vals_list)

    # =============================================
    # 4) write - When an existing record is edited
    # =============================================
    def write(self, vals):
        for record in self:
            local_vals = vals.copy()
            # --- Employee ---
            if 'employee_code_check' in local_vals:
                if local_vals['employee_code_check'] and not record.employee_code:
                    local_vals['employee_code'] = self.env['ir.sequence'].next_by_code('employee.code') or _('New')
                elif not local_vals['employee_code_check'] and record.employee_code:
                    local_vals['employee_code'] = False  # ← Remove the code

            # --- Customer ---
            if 'customer_code_check' in local_vals:
                if local_vals['customer_code_check'] and not record.customer_code:
                    local_vals['customer_code'] = self.env['ir.sequence'].next_by_code('customer.code') or _('New')
                elif not local_vals['customer_code_check'] and record.customer_code:
                    local_vals['customer_code'] = False

            # --- Vendor ---
            if 'vendor_code_check' in local_vals:
                if local_vals['vendor_code_check'] and not record.vendor_code:
                    local_vals['vendor_code'] = self.env['ir.sequence'].next_by_code('vendor.code') or _('New')
                elif not local_vals['vendor_code_check'] and record.vendor_code:
                    local_vals['vendor_code'] = False

            super(InvestmentContact, record).write(local_vals)
        return True

    _sql_constraints = [
        ('employee_code_unique', 'UNIQUE(employee_code)', 'Employee Code must be unique!'),
        ('customer_code_unique', 'UNIQUE(customer_code)', 'Customer Code must be unique!'),
        ('vendor_code_unique', 'UNIQUE(vendor_code)', 'Vendor Code must be unique!'),
    ]


