/** @odoo-module **/
/*
 * Hospital Dashboard — OWL client action.
 *
 * Fetches data from /hospital/dashboard/data and renders KPIs + charts.
 * Chart.js is lazy-loaded via loadJS.
 *
 * Odoo 19 notes:
 *   - `useService("rpc")` was REMOVED — use the standalone `rpc` function
 *     from `@web/core/network/rpc`.
 *   - `useService("orm")` is still available for ORM calls.
 */

import { Component, onWillStart, onMounted, onWillUnmount, useRef, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";
import { rpc } from "@web/core/network/rpc";

class HospitalDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.actionService = useService("action");
        this.state = useState({
            loading: true,
            error: null,
            data: null,
        });
        this.chartRefs = {
            appointments: useRef("chart_appointments"),
            admissions: useRef("chart_admissions"),
            beds: useRef("chart_beds"),
        };
        this._charts = {};

        onWillStart(async () => {
            await loadJS("https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js");
        });

        onMounted(() => {
            this._fetchData();
        });

        // LAW 24: destroy all chart instances on unmount — prevents ~500KB memory leak per navigation
        onWillUnmount(() => {
            Object.values(this._charts).forEach((chart) => {
                try { chart.destroy(); } catch (e) { /* ignore */ }
            });
            this._charts = {};
        });
    }

    async _fetchData() {
        try {
            const result = await rpc("/hospital/dashboard/data", {});
            if (result && result.error) {
                this.state.error = result.error;
                this.state.loading = false;
            } else if (result) {
                this.state.data = result;
                this.state.loading = false;
                // LAW 25: double requestAnimationFrame ensures DOM is fully painted
                // before chart render — single rAF renders against 0×0 canvas
                requestAnimationFrame(() => {
                    requestAnimationFrame(() => this._renderCharts());
                });
            }
        } catch (err) {
            this.state.error = (err && err.message) || "Failed to load dashboard data";
            this.state.loading = false;
        }
    }

    _renderCharts() {
        if (!this.state.data || !this.state.data.charts) return;
        const charts = this.state.data.charts;

        // Destroy existing charts before re-creating
        Object.values(this._charts).forEach((c) => {
            try { c.destroy(); } catch (e) { /* ignore */ }
        });
        this._charts = {};

        // Appointments by department (bar)
        if (this.chartRefs.appointments.el && charts.appointments_by_dept) {
            this._charts.appointments = new Chart(this.chartRefs.appointments.el, {
                type: "bar",
                data: {
                    labels: charts.appointments_by_dept.labels,
                    datasets: [{
                        label: "Appointments",
                        data: charts.appointments_by_dept.values,
                        backgroundColor: "#17a2b8",
                    }],
                },
                options: { responsive: true, maintainAspectRatio: false },
            });
        }

        // Admissions by state (doughnut)
        if (this.chartRefs.admissions.el && charts.admissions_by_state) {
            this._charts.admissions = new Chart(this.chartRefs.admissions.el, {
                type: "doughnut",
                data: {
                    labels: charts.admissions_by_state.labels,
                    datasets: [{
                        data: charts.admissions_by_state.values,
                        backgroundColor: ["#6c757d", "#17a2b8", "#28a745", "#dc3545"],
                    }],
                },
                options: { responsive: true, maintainAspectRatio: false },
            });
        }

        // Beds by ward type (stacked bar)
        if (this.chartRefs.beds.el && charts.beds_by_ward_type) {
            this._charts.beds = new Chart(this.chartRefs.beds.el, {
                type: "bar",
                data: {
                    labels: charts.beds_by_ward_type.labels,
                    datasets: [
                        {
                            label: "Available",
                            data: charts.beds_by_ward_type.available,
                            backgroundColor: "#28a745",
                        },
                        {
                            label: "Occupied",
                            data: charts.beds_by_ward_type.occupied,
                            backgroundColor: "#dc3545",
                        },
                    ],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: { x: { stacked: true }, y: { stacked: true } },
                },
            });
        }
    }

    // Action handlers for KPI cards (click to navigate)
    onClickPatients() {
        this.actionService.doAction("el_hospital.action_hospital_patient");
    }

    onClickPhysicians() {
        this.actionService.doAction("el_hospital.action_hospital_physician");
    }

    onClickAppointments() {
        this.actionService.doAction("el_hospital.action_hospital_appointment_today");
    }

    onClickAdmissions() {
        this.actionService.doAction("el_hospital.action_hospital_admission_active");
    }

    onClickRefresh() {
        this.state.loading = true;
        this.state.error = null;
        this._fetchData();
    }
}

HospitalDashboard.template = "hospital_dashboard.HospitalDashboard";

registry.category("actions").add("hospital_dashboard", HospitalDashboard);

export default HospitalDashboard;
