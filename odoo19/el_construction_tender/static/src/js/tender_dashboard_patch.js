/** @odoo-module **/

import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";

// The base dashboard component is registered but not exported, so it is
// retrieved from the actions registry. This module's assets load after
// el_construction_management's (declared dependency), so the entry exists
// by the time this file runs.
const ConstructionDashboard = registry.category("actions").get("construction_dashboard");

patch(ConstructionDashboard.prototype, {
    setup() {
        super.setup();
        Object.assign(this.state, {
            tenderTotal: 0,
            tenderOpen: 0,
            tenderWon: 0,
            tenderLost: 0,
            tenderPipelineValue: 0,
            tenderWonValue: 0,
            rfqOpen: 0,
        });
    },

    async fetchDashboardData() {
        await super.fetchDashboardData();
        try {
            const r = await this.orm.call("el_construction.tender.opportunity", "dashboard_snapshot", []);
            Object.assign(this.state, {
                tenderTotal: r.tender_total,
                tenderOpen: r.tender_open,
                tenderWon: r.tender_won,
                tenderLost: r.tender_lost,
                tenderPipelineValue: r.tender_pipeline_value,
                tenderWonValue: r.tender_won_value,
                rfqOpen: r.rfq_open,
            });
        } catch (e) {
            console.error("Tender dashboard fetch error:", e);
        }
    },

    onTendersClick() {
        this.openView("el_construction.tender.opportunity", "Tenders", []);
    },

    onTendersOpenClick() {
        this.openView("el_construction.tender.opportunity", "Open Tenders",
            [["state", "in", ["draft", "qualification", "estimating", "review", "submitted"]]]);
    },

    onRfqOpenClick() {
        this.openView("el_construction.tender.rfq", "Open RFQs",
            [["state", "in", ["draft", "sent", "bidding", "comparison"]]]);
    },
});
