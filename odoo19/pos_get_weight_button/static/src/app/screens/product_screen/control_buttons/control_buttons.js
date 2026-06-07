import { _t } from "@web/core/l10n/translation";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";

patch(ControlButtons.prototype, {
async onClickGetWeight() {
    try {
        const response = await fetch("http://localhost:8000/api/weight");
        const data = await response.json();

        console.log(data);

    } catch (error) {
        console.error(error);
    }
},
});
