import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";

/**
 * Customer-wise payment methods.
 *
 * The base PaymentScreen snapshots the config payment methods once in
 * setup() (`payment_methods_from_config`). We replace that snapshot with a
 * reactive getter so the payment buttons are recomputed on every render:
 *
 * 1. order partner (or its commercial partner) has allowed methods
 *    -> only those (clipped to this POS)
 * 2. no partner list, POS has defaults  -> only the default methods
 * 3. otherwise                          -> all POS payment methods
 *
 * Because the getter reads the reactive POS store, removing the partner
 * or changing it updates the buttons immediately, without reopening the
 * payment screen.
 *
 * The property is defined with both a getter and a setter on purpose. The
 * base PaymentScreen.setup() assigns payment_methods_from_config, and other
 * modules (pos_urban_piper) append to it. A getter-only accessor installed on
 * the prototype would turn those assignments into a TypeError ("Cannot set
 * property ... which has only a getter"), so the setter below captures the
 * assigned snapshot and the getter keeps applying the filtering on top of it.
 */
patch(PaymentScreen.prototype, {
    get payment_methods_from_config() {
        const methods = (this.el_payment_methods_snapshot ??
            this.pos.config.payment_method_ids)
            .slice()
            .sort((a, b) => a.sequence - b.sequence);
        const partner =
            this.currentOrder && this.currentOrder.get_partner();
        // An order can be set to a child (invoice) address while the
        // restriction sits on the parent, so fall back to the commercial
        // partner before giving up.
        const allowed = [
            partner && partner.el_allowed_pos_payment_method_ids,
            partner &&
                partner.commercial_partner_id &&
                partner.commercial_partner_id
                    .el_allowed_pos_payment_method_ids,
        ].find((list) => list && list.length);
        if (allowed) {
            const allowedIds = new Set(allowed.map((m) => m.id));
            return methods.filter((pm) => allowedIds.has(pm.id));
        }
        const defaults = this.pos.config.el_pos_default_payment_method_ids;
        if (defaults && defaults.length) {
            const defaultIds = new Set(defaults.map((m) => m.id));
            return methods.filter((pm) => defaultIds.has(pm.id));
        }
        return methods;
    },
    /**
     * Keep assignments working: the base PaymentScreen.setup() builds the
     * snapshot, and other modules may append their own methods to it. The
     * getter above stays authoritative for what the template renders.
     *
     * @override
     */
    set payment_methods_from_config(methods) {
        this.el_payment_methods_snapshot = methods;
    },
});
