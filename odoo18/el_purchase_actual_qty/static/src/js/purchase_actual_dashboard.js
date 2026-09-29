/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

class PurchaseActualDashboard extends Component {
    setup() {
        this.state = useState({
            loading: true,
            error: null,
            period: "all",
            date_from: "",
            date_to: "",
            product_id: false,
            data: { kpis: {}, vendors: [], products: [] },
        });
        onWillStart(() => this.load());
        this.onSetPeriodAll = () => this.setPeriod("all");
        this.onSetPeriodMonth = () => this.setPeriod("month");
        this.onSetPeriodQuarter = () => this.setPeriod("quarter");
        this.onSetPeriodYear = () => this.setPeriod("year");
        this.onDateFromChange = (ev) => this.onDateChange(ev, "date_from");
        this.onDateToChange = (ev) => this.onDateChange(ev, "date_to");
        this.onProductChange = (ev) => {
            this.state.product_id = ev.target.value ? parseInt(ev.target.value) : false;
            this.load();
        };
    }

    async load() {
        this.state.loading = true;
        this.state.error = null;
        try {
            const range = this.getRange(this.state.period);
            const date_from = this.state.date_from || range.date_from || false;
            const date_to = this.state.date_to || range.date_to || false;
            const product_id = this.state.product_id || false;
            this.state.data = await rpc("/web/dataset/call_kw/el.purchase.actual.report/get_dashboard_data", {
                model: "el.purchase.actual.report",
                method: "get_dashboard_data",
                args: [date_from, date_to, product_id],
                kwargs: {},
            });
        } catch (error) {
            this.state.error = error.message || "Unable to load dashboard.";
        } finally {
            this.state.loading = false;
        }
    }

    onDateChange(ev, field) {
        const val = ev.target.value;
        this.state[field] = val ? val + " 00:00:00" : "";
        this.state.period = "custom";
        this.load();
    }

    getRange(period) {
        const now = new Date();
        const pad = (n) => String(n).padStart(2, "0");
        const date = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} 00:00:00`;
        if (period === "month") return { date_from: date(new Date(now.getFullYear(), now.getMonth(), 1)), date_to: false };
        if (period === "quarter") {
            const month = Math.floor(now.getMonth() / 3) * 3;
            return { date_from: date(new Date(now.getFullYear(), month, 1)), date_to: false };
        }
        if (period === "year") return { date_from: date(new Date(now.getFullYear(), 0, 1)), date_to: false };
        return { date_from: false, date_to: false };
    }

    async setPeriod(period) {
        this.state.period = period;
        this.state.date_from = "";
        this.state.date_to = "";
        this.state.product_id = false;
        await this.load();
    }

    format(value, digits = 2) {
        return Number(value || 0).toLocaleString(undefined, { maximumFractionDigits: digits });
    }

    exportCsv() {
        window.location.href = "/purchase_actual_qty/export/csv";
    }

    openAnalysis() {
        this.env.services.action.doAction("el_purchase_actual_qty.action_purchase_actual_report");
    }
}

PurchaseActualDashboard.template = "el_purchase_actual_qty.PurchaseActualDashboard";
registry.category("actions").add("purchase_actual_qty_dashboard", PurchaseActualDashboard);
