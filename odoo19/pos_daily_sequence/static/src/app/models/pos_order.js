import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    setup(vals) {
        super.setup(...arguments);
        this.daily_order_number = vals.daily_order_number || this.daily_order_number || "";
    },

    get dailyOrderNumberOnly() {
        return this.daily_order_number?.match(/\d+$/)?.[0] || this.daily_order_number || "";
    },
});
