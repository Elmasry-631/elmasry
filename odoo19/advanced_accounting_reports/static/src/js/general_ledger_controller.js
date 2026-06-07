/** @odoo-module **/
import { registry } from "@web/core/registry";
import { ListController } from "@web/views/list/list_controller";

export class GeneralLedgerController extends ListController {
    setup() {
        super.setup();
    }
}

registry.category("views").add("general_ledger_tree", {
    ...registry.category("views").get("list"),
    Controller: GeneralLedgerController,
});
