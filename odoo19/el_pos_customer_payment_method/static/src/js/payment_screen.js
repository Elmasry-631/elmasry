import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";

/**
 * Customer-wise payment methods.
 *
 * The base PaymentScreen snapshots the config payment methods once in
 * setup() (`payment_methods_from_config`). We replace that snapshot with a
 * reactive getter so the payment buttons are recomputed on every render.
 * Rules, first match wins:
 *
 * 1. order partner (or its commercial partner) has allowed methods
 *    -> only those (clipped to this POS)
 * 2. POS has default methods -> only the default methods
 * 3. otherwise               -> all POS payment methods
 *
 * A rule whose list does not match any method enabled on this POS is
 * skipped (falls to the next rule) so the screen never ends up with zero
 * buttons - the template reads payment_methods_from_config[0].
 *
 * The property has both a getter and a setter on purpose: the base setup()
 * assigns payment_methods_from_config, and a getter-only accessor on the
 * prototype would turn that assignment into a TypeError. The setter keeps
 * the assigned snapshot; the getter applies the filtering on top of it.
 */
function elKeepOnly(methods, allowed) {
    const ids = new Set(allowed.map((m) => m.id));
    return methods.filter((pm) => ids.has(pm.id));
}

patch(PaymentScreen.prototype, {
    get payment_methods_from_config() {
        const methods = (
            this.el_payment_methods_snapshot ?? this.pos.config.payment_method_ids
        )
            .slice()
            .sort((a, b) => a.sequence - b.sequence);
        const partner = this.currentOrder && this.currentOrder.getPartner();
        // The order can be set to a child (invoice) address while the
        // restriction sits on the parent, so also try the commercial partner.
        const candidates = [
            partner && partner.el_allowed_pos_payment_method_ids,
            partner &&
                partner.commercial_partner_id &&
                partner.commercial_partner_id.el_allowed_pos_payment_method_ids,
            this.pos.config.el_pos_default_payment_method_ids,
        ];
        for (const list of candidates) {
            if (list && list.length) {
                const filtered = elKeepOnly(methods, list);
                if (filtered.length) {
                    return filtered;
                }
            }
        }
        return methods;
    },
    /** @override */
    set payment_methods_from_config(methods) {
        this.el_payment_methods_snapshot = methods;
    },
});
