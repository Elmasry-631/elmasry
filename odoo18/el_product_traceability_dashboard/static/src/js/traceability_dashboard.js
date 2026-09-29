/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";

export class ProductTraceabilityDashboard extends Component {
    setup() {
        this.action = useService("action");
        this.state = useState({
            loading: true,
            error: null,
            period: "month",
            filters: { date_from: "", date_to: "", product_id: false, categ_id: false, partner_id: false, lot_id: false, warehouse_id: false, operation_type: false },
            options: { products: [], categories: [], vendors: [], lots: [], warehouses: [] },
            data: { metrics: {}, totals: {}, products: [], vendors: [], activity: [], manufacturing: [] },
        });
        onWillStart(async () => {
            await this.loadOptions();
            await this.load();
        });
    }

    async loadOptions() {
        const result = await rpc("/web/dataset/call_kw", {
            model: "el.product.traceability.dashboard",
            method: "get_filter_options",
            args: [this.env.company?.id || false],
            kwargs: {},
        });
        this.state.options = result;
    }

    async load() {
        this.state.loading = true;
        this.state.error = null;
        try {
            const range = this.getRange(this.state.period);
            const filters = { ...this.state.filters };
            if (!filters.date_from && range.date_from) filters.date_from = range.date_from;
            if (!filters.date_to && range.date_to) filters.date_to = range.date_to;
            filters.company_id = this.env.company?.id || false;
            this.state.data = await rpc("/web/dataset/call_kw", {
                model: "el.product.traceability.dashboard",
                method: "get_dashboard_data",
                args: [filters],
                kwargs: {},
            });
        } catch (error) {
            this.state.error = error.message || "Unable to load dashboard.";
        } finally {
            this.state.loading = false;
        }
    }

    getRange(period) {
        const now = new Date();
        const pad = (n) => String(n).padStart(2, "0");
        const fmt = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
        if (period === "month") return { date_from: fmt(new Date(now.getFullYear(), now.getMonth(), 1)), date_to: fmt(now) };
        if (period === "quarter") {
            const month = Math.floor(now.getMonth() / 3) * 3;
            return { date_from: fmt(new Date(now.getFullYear(), month, 1)), date_to: fmt(now) };
        }
        if (period === "year") return { date_from: fmt(new Date(now.getFullYear(), 0, 1)), date_to: fmt(now) };
        return { date_from: false, date_to: false };
    }

    async setPeriod(period) {
        this.state.period = period;
        this.state.filters.date_from = "";
        this.state.filters.date_to = "";
        const range = this.getRange(period);
        this.state.filters.date_from = range.date_from || "";
        this.state.filters.date_to = range.date_to || "";
        await this.load();
    }

    async onFilterChange(field, ev) {
        this.state.filters[field] = ev.target.value ? parseInt(ev.target.value) || ev.target.value : false;
        await this.load();
    }

    async onDateChange(field, ev) {
        this.state.filters[field] = ev.target.value || "";
        this.state.period = "custom";
        await this.load();
    }

    async reset() {
        this.state.period = "month";
        this.state.filters = { date_from: "", date_to: "", product_id: false, categ_id: false, partner_id: false, lot_id: false, warehouse_id: false, operation_type: false };
        await this.load();
    }

    openMovements() {
        this.action.doAction("el_product_traceability_dashboard.action_product_traceability_report");
    }

    openManufacturing() {
        this.action.doAction("el_product_traceability_dashboard.action_product_traceability_manufacturing");
    }

    operationLabel(key) {
        return {
            receipt: "Purchases / Receipts", vendor_return: "Vendor Returns", manufacturing_consume: "Consumed in Production",
            manufacturing_produce: "Manufactured", internal: "Internal Transfers", delivery: "Customer Deliveries",
            customer_return: "Customer Returns", scrap: "Scrap / Waste", adjustment: "Adjustments",
        }[key] || key;
    }

    metric(key) { return this.state.data.metrics?.[key] || { qty: 0, value: 0, count: 0 }; }
    format(value, digits = 2) { return Number(value || 0).toLocaleString(undefined, { maximumFractionDigits: digits }); }
    formatDate(value) { return value ? new Date(value.replace(" ", "T")).toLocaleDateString() : "-"; }
    pct(value, max) { return max ? Math.min(100, Math.max(3, (value / max) * 100)) : 3; }

    get flowMax() {
        const m = this.state.data.metrics || {};
        return Math.max(m.receipt?.qty || 0, m.manufacturing_consume?.qty || 0, m.manufacturing_produce?.qty || 0, m.delivery?.qty || 0, m.scrap?.qty || 0, 1);
    }
}

ProductTraceabilityDashboard.template = "el_product_traceability_dashboard.Dashboard";
registry.category("actions").add("el_product_traceability_dashboard", ProductTraceabilityDashboard);
