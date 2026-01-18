odoo.define('sale_discount_total.CustomTaxTotalsComponent', function (require) {
    "use strict";

    const LegacyTaxTotalsComponent = require('account.tax_group_owl');
    const field_registry = require('web.field_registry_owl');

    class CustomTaxTotalsComponent extends LegacyTaxTotalsComponent {

        _computeTotalsFormat() {
            if (!this.totals.value) // Misc journal entry
                return;

            // Extract discount type and rate from context
            const discountType = this.totals.value.discount_type;
            const discountRate = this.totals.value.discount_rate;

            let amount_untaxed = this.totals.value.amount_untaxed;
            let amount_tax = 0;
            let subtotals = [];

            // Calculate subtotals
            for (let subtotal_title of this.totals.value.subtotals_order) {
                let amount_total = amount_untaxed + amount_tax;
                subtotals.push({
                    'name': subtotal_title,
                    'amount': amount_total,
                    'formatted_amount': this._format(amount_total),
                });
                let group = this.totals.value.groups_by_subtotal[subtotal_title];
                for (let i in group) {
                    amount_tax += group[i].tax_group_amount;
                }
            }

            // Apply discount to amount_total
            let amount_total = amount_untaxed + amount_tax;
            if (discountType === 'percent') {
                amount_total -= (amount_total * discountRate / 100);
            } else if (discountType === 'amount') {
                amount_total -= discountRate;
            }

            // Update the state with the new totals
            this.totals.value.subtotals = subtotals;
            this.totals.value.amount_total = amount_total;
            this.totals.value.formatted_amount_total = this._format(amount_total);

            // Format the tax group amounts
            for (let group_name of Object.keys(this.totals.value.groups_by_subtotal)) {
                let group = this.totals.value.groups_by_subtotal[group_name];
                for (let i in group) {
                    group[i].formatted_tax_group_amount = this._format(group[i].tax_group_amount);
                    group[i].formatted_tax_group_base_amount = this._format(group[i].tax_group_base_amount);
                }
            }
        }
    }

    field_registry.add('account-tax-totals-field', CustomTaxTotalsComponent);
});
