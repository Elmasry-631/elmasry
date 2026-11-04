# Odoo Addons by Elmasry

Custom and third-party Odoo addons, organized by Odoo version. Each addon folder contains its own `__manifest__.py`. Add the relevant version directory to `addons_path`, verify dependencies and edition requirements, then install from Apps. This README describes the source snapshot delivered in `elmasry_development_batch1.zip` and includes static technical inventory for all discovered manifests.

| | |
|---|---|
| Addons | **112** |
| Odoo 17 | 4 |
| Odoo 18 | 46 |
| Odoo 19 | 57 |
| Odoo 20 | 5 |

## Contents

- [Technical Inventory — All 112 Modules](#technical-inventory--all-112-modules) — manifest metadata, Python models/classes, declared fields and methods, routes, XML views, menus, security, tests and source-file groups for every addon.

- [Odoo 17](#odoo-17) — 4 addons
- [Odoo 18](#odoo-18) — 46 addons
- [Odoo 19](#odoo-19) — 57 addons
- [Odoo 20](#odoo-20) — 5 addons

## Index by domain

### Point of Sale

| Addon | Version | Summary |
|---|---|---|
| [`el_pos_customer_payment_method`](odoo18/el_pos_customer_payment_method/) | Odoo 18 | Restrict POS payment methods per customer, with POS-level defaults for customers without a specific list |
| [`pos_cashier_handover`](odoo18/pos_cashier_handover/) | Odoo 18 | طباعة تسليم الخزينة عند إغلاق جلسة نقطة البيع |
| [`pos_get_weight_button`](odoo18/pos_get_weight_button/) | Odoo 18 | Get Weight POS button that reads a local scale and sets the line quantity |
| [`pos_receipt_price_before_discount`](odoo18/pos_receipt_price_before_discount/) | Odoo 18 | Show product list price (before discount) under each receipt line when discounted |
| [`pos_refund_restriction`](odoo18/pos_refund_restriction/) | Odoo 18 | Restrict refund operations in POS to administrators only |
| [`el_pos_customer_payment_method`](odoo19/el_pos_customer_payment_method/) | Odoo 19 | Restrict POS payment methods per customer, with POS-level defaults for customers without a specific list |
| [`pos_daily_sequence`](odoo19/pos_daily_sequence/) | Odoo 19 | Automatically reset POS order numbering every day |
| [`pos_get_weight_button`](odoo19/pos_get_weight_button/) | Odoo 19 | Get Weight POS button reading a local scale (Odoo 19 port, logs only) |
| [`el_pos_customer_payment_method`](odoo20/el_pos_customer_payment_method/) | Odoo 20 | Restrict POS payment methods per customer, with POS-level defaults for customers without a specific list |

### Sales

| Addon | Version | Summary |
|---|---|---|
| [`ie_print_document_linked_order`](odoo17/ie_print_document_linked_order/) | Odoo 17 | Show all product attachments directly from Quotation |
| [`bi_so_product_quantity_limit`](odoo18/bi_so_product_quantity_limit/) | Odoo 18 | Minimum and maximum orderable quantity per product |
| [`el_kitchen_receipt`](odoo18/el_kitchen_receipt/) | Odoo 18 | Print kitchen receipt from sales quotation with customer delivery info auto-fill + pilot name sync with delivery |
| [`el_sale_order_confirmation_user`](odoo18/el_sale_order_confirmation_user/) | Odoo 18 | Track which user actually confirmed each sales order |
| [`ie_restrict_qty`](odoo18/ie_restrict_qty/) | Odoo 18 | qty_restrict maximum orderable quantity on product.template |
| [`sale_barcode_scanner`](odoo18/sale_barcode_scanner/) | Odoo 18 | Scan products by Barcode/QRCode in sales orders using mobile camera or webcam |
| [`sale_contract_auto`](odoo18/sale_contract_auto/) | Odoo 18 | Automatically generate contracts from sale orders |
| [`sale_kitchen_receipt`](odoo18/sale_kitchen_receipt/) | Odoo 18 | Print kitchen receipt from sales quotation |
| [`sale_order_automation`](odoo18/sale_order_automation/) | Odoo 18 | One-click invoice creation and delivery validation from the sale order |
| [`sale_order_contract`](odoo18/sale_order_contract/) | Odoo 18 | Bilingual AR/EN supply-and-installation contract PDF rendered from a sale order (QWeb only) |
| [`sale_order_contract_terms`](odoo18/sale_order_contract_terms/) | Odoo 18 | Sales order plus 4 contract pages with 9 bilingual AR/EN clauses |
| [`sale_stock_restrict`](odoo18/sale_stock_restrict/) | Odoo 18 | Module helps to restrict out of stock products |
| [`sales_credit_limit`](odoo18/sales_credit_limit/) | Odoo 18 | An advanced way to handle customer credit limit through warning and blocking stage |
| [`bi_so_product_quantity_limit`](odoo19/bi_so_product_quantity_limit/) | Odoo 19 | Odoo 19 port of the sale order min/max quantity limit |
| [`customer_classification`](odoo19/customer_classification/) | Odoo 19 | Classify customers into tiers (A-E) with inherited price lists, credit limits, and payment terms |
| [`el_commission_type`](odoo19/el_commission_type/) | Odoo 19 | Manage sales commission types by team member role |
| [`el_nmo_classification`](odoo19/el_nmo_classification/) | Odoo 19 | Customer tiers A–E with price list, credit limit, payment term and credit policy per tier |
| [`el_nmo_credit_approval`](odoo19/el_nmo_credit_approval/) | Odoo 19 | Approval workflow for sale orders exceeding customer credit limits |
| [`el_nmo_sale_payment_gateway`](odoo19/el_nmo_sale_payment_gateway/) | Odoo 19 | Payment gateway master data propagated to partners, sales orders, invoices and stock transfers; synchronizes default receivable/payable accounts and carrier |

### Purchase

| Addon | Version | Summary |
|---|---|---|
| [`el_purchase_actual_qty`](odoo18/el_purchase_actual_qty/) | Odoo 18 | Actual purchase quantity with preserved value, dashboard and reporting |
| [`wm_purchase_global_discount`](odoo18/wm_purchase_global_discount/) | Odoo 18 | Global discount on purchase orders, mirroring the Odoo sales discount behaviour |
| [`wm_purchase_global_discount`](odoo19/wm_purchase_global_discount/) | Odoo 19 | Odoo 19 port of the purchase order global discount |

### Inventory & Warehouse

| Addon | Version | Summary |
|---|---|---|
| [`delivery_return_reason`](odoo18/delivery_return_reason/) | Odoo 18 | تتبع أسباب رجوع الطلبات مع إحصائيات وتحليلات |
| [`el_barcode_price_display`](odoo18/el_barcode_price_display/) | Odoo 18 | Standalone barcode scanner price display page — no login needed |
| [`el_product_traceability_dashboard`](odoo18/el_product_traceability_dashboard/) | Odoo 18 | Product traceability dashboard with returns, scrap and manufacturing genealogy |
| [`inventory_report_generator`](odoo18/inventory_report_generator/) | Odoo 18 | Dynamic inventory reports generated from a wizard |
| [`invoice_stock_move`](odoo18/invoice_stock_move/) | Odoo 18 | Create stock deliveries and receipts from a customer invoice or vendor bill |
| [`product_movement_report`](odoo18/product_movement_report/) | Odoo 18 | Full movement history of a product/lot from first receipt until fully sold |
| [`stock_move_invoice`](odoo18/stock_move_invoice/) | Odoo 18 | Create invoice for stock picking |
| [`stock_split_transfer`](odoo18/stock_split_transfer/) | Odoo 18 | Two-step internal transfers with per-user location visibility |
| [`transfer_wizard`](odoo18/transfer_wizard/) | Odoo 18 | Delivery transfer wizard recording the driver and vehicle on stock pickings |
| [`el_barcode_price_display`](odoo19/el_barcode_price_display/) | Odoo 19 | Standalone barcode scanner price display page — no login needed |
| [`el_inter_company_transfer`](odoo19/el_inter_company_transfer/) | Odoo 19 | Automate inter-company stock, sale, purchase, and accounting documents |
| [`el_prevent_negative_stock`](odoo19/el_prevent_negative_stock/) | Odoo 19 | Rejects any stock move that would make a product's quantity negative (delivery, internal, MRP) |
| [`inventory_report_generator`](odoo19/inventory_report_generator/) | Odoo 19 | Odoo 19 port of the dynamic inventory report generator |
| [`invoice_stock_move`](odoo19/invoice_stock_move/) | Odoo 19 | Create stock deliveries and receipts from a customer invoice or vendor bill |
| [`smsa_express_delivery_carrier`](odoo19/smsa_express_delivery_carrier/) | Odoo 19 | SMSA Express integration with the SECOM customer application |
| [`stock_intercompany_transfer`](odoo19/stock_intercompany_transfer/) | Odoo 19 | Create counterpart Receipt/Delivery Orders between companies |
| [`el_inter_company_transfer`](odoo20/el_inter_company_transfer/) | Odoo 20 | Inter-company stock transfer request with source/destination warehouses and outgoing/incoming pickings |

### Accounting & Finance

| Addon | Version | Summary |
|---|---|---|
| [`account_invoice_fixed_discount`](odoo18/account_invoice_fixed_discount/) | Odoo 18 | Allows to apply fixed amount discounts in invoices |
| [`el_restrict_journal`](odoo18/el_restrict_journal/) | Odoo 18 | Per-user journal whitelist — only allowed journals are visible |
| [`account_invoice_fixed_discount`](odoo19/account_invoice_fixed_discount/) | Odoo 19 | Allows to apply fixed amount discounts in invoices |
| [`cheque_tracking`](odoo19/cheque_tracking/) | Odoo 19 | Track received and issued cheques with accounting lifecycle entries |
| [`cheque_tracking_endorsement`](odoo19/cheque_tracking_endorsement/) | Odoo 19 | Full cheque endorsement workflow with audit records |
| [`el_cheque_tracking`](odoo19/el_cheque_tracking/) | Odoo 19 | Track received and issued cheques with accounting lifecycle entries |
| [`invoice_tracking`](odoo19/invoice_tracking/) | Odoo 19 | Tracks inbound vendor invoices through receive → administration → bill |

### Human Resources

| Addon | Version | Summary |
|---|---|---|
| [`WPS`](odoo19/WPS/) | Odoo 19 | Export payroll payslips as a WPS SIF CSV for Qatar wage protection |
| [`bi_employee_travel_managment`](odoo19/bi_employee_travel_managment/) | Odoo 19 | Employee travel requests and travel expense management |
| [`deduction_management`](odoo19/deduction_management/) | Odoo 19 | Employee deductions with automatic payroll integration |
| [`el_hr_attendance_sheet`](odoo19/el_hr_attendance_sheet/) | Odoo 19 | Calculate overtime, lateness, absence from attendance and feed payslip |
| [`el_payroll_wps`](odoo19/el_payroll_wps/) | Odoo 19 | Adds an 'Others' field to payslips and a WPS CSV export action |
| [`loan_management`](odoo19/loan_management/) | Odoo 19 | Employee loans with payroll deduction and repayment tracking |
| [`rm_hr_attendance_sheet`](odoo19/rm_hr_attendance_sheet/) | Odoo 19 | Policy-driven attendance sheets |
| [`zk_attendance_integration_v19`](odoo19/zk_attendance_integration_v19/) | Odoo 19 | Integration with ZK Attendance Machines |
| [`el_hr_attendance_sheet`](odoo20/el_hr_attendance_sheet/) | Odoo 20 | Calculate overtime, lateness, absence from attendance and feed payslip |

### CRM

| Addon | Version | Summary |
|---|---|---|
| [`ie_costem_lead_form`](odoo17/ie_costem_lead_form/) | Odoo 17 | Two large custom visit forms on crm.lead: Site Visit and Company Visit |
| [`archer_meta_lead_ads`](odoo18/archer_meta_lead_ads/) | Odoo 18 | Import Meta lead ads into CRM leads |
| [`archer_meta_lead_ads`](odoo19/archer_meta_lead_ads/) | Odoo 19 | Import Meta lead ads into CRM leads |
| [`crm_project_linker`](odoo19/crm_project_linker/) | Odoo 19 | Create and link projects from CRM opportunities |
| [`partner_request`](odoo19/partner_request/) | Odoo 19 | Approval workflow for creating new customers via sales requests |

### Construction

| Addon | Version | Summary |
|---|---|---|
| [`el_construction_management`](odoo19/el_construction_management/) | Odoo 19 | Construction Management \| Job Costing \| BOQ \| Work Orders \| RA Billing \| Material Requisition \| Subcontracting \| Budget |
| [`el_construction_tender`](odoo19/el_construction_tender/) | Odoo 19 | Client Tenders (Bid Costing & Submission) + Subcontractor/Vendor RFQ & Bid Comparison |

### Healthcare & Services

| Addon | Version | Summary |
|---|---|---|
| [`bi_health_care_center_management`](odoo18/bi_health_care_center_management/) | Odoo 18 | Manage Health Care Center Management Operations Industry Management Services Custom Health Care Solution |
| [`bi_sport_center_management`](odoo18/bi_sport_center_management/) | Odoo 18 | Sport club / fitness centre operations |
| [`el_hospital`](odoo19/el_hospital/) | Odoo 19 | Patient registration and management |

### E-Commerce & Connectors

| Addon | Version | Summary |
|---|---|---|
| [`odoo_multi_channel_sale`](odoo18/odoo_multi_channel_sale/) | Odoo 18 | Base connector that links Odoo to several marketplaces (Webkul) |
| [`odoo_salla_integration`](odoo18/odoo_salla_integration/) | Odoo 18 | Salla (Saudi e-commerce) connector on top of odoo_multi_channel_sale |
| [`whatsapp_mail_messaging`](odoo18/whatsapp_mail_messaging/) | Odoo 18 | Send WhatsApp messages and emails from the systray, sale orders, invoices and the website portal |
| [`connector_foodics`](odoo19/connector_foodics/) | Odoo 19 | Bidirectional synchronization bridge between Odoo and Foodics POS |
| [`ebook_serial_delivery`](odoo19/ebook_serial_delivery/) | Odoo 19 | Deliver eBook licenses using standard Inventory Serial Numbers (stock.lot) — no custom "activation code" model |
| [`el_ebook_store`](odoo19/el_ebook_store/) | Odoo 19 | Sell e-books with unique access codes — online reader + download |
| [`whatsapp_mail_messaging`](odoo19/whatsapp_mail_messaging/) | Odoo 19 | Odoo 19 port of the WhatsApp connector (systray, sale orders, invoices, portal and share URLs) |

### Payment Gateways

| Addon | Version | Summary |
|---|---|---|
| [`payment_alrajhi_arb`](odoo19/payment_alrajhi_arb/) | Odoo 19 | Official-style ARB integration: token API, encrypted trandata, bank-hosted redirect, KSA Card/Mada checkout (Odoo 19) |
| [`payment_applepay`](odoo19/payment_applepay/) | Odoo 19 | Apple Pay acquirer button on top of the HyperPay (OPPWA) acquirer |
| [`payment_hyperpay`](odoo19/payment_hyperpay/) | Odoo 19 | Website Hyper Pay Payment Acquirer |

### Printing, Reports & PDF

| Addon | Version | Summary |
|---|---|---|
| [`ie_crm_lead_pdf`](odoo17/ie_crm_lead_pdf/) | Odoo 17 | Adds a Lead Report QWeb-PDF action on crm.lead |
| [`pdf_print_preview`](odoo18/pdf_print_preview/) | Odoo 18 | Preview and print PDF report in your browser \| Pdf direct preview \| Print without Download |
| [`prt_report_attachment_preview`](odoo18/prt_report_attachment_preview/) | Odoo 18 | Overrides the core ReportController.report_routes to force Content-Disposition: inline |
| [`advanced_accounting_reports`](odoo19/advanced_accounting_reports/) | Odoo 19 | Advanced General Ledger, Trial Balance with Analytic Dimensions & Multi-Currency |
| [`direct_print_auto`](odoo19/direct_print_auto/) | Odoo 19 | Auto-prints reports to the browser print dialog when a document is confirmed |
| [`el_pdf_print_preview`](odoo19/el_pdf_print_preview/) | Odoo 19 | Preview PDF reports in-browser before printing — no download needed |
| [`ie_stock_movement_report`](odoo19/ie_stock_movement_report/) | Odoo 19 | PDF stock movement report with opening balance and running valuation |
| [`partner_balance_confirmation`](odoo19/partner_balance_confirmation/) | Odoo 19 | Customer Balance Confirmation (Imdad / Namo templates) |
| [`saudi_tax_invoice`](odoo19/saudi_tax_invoice/) | Odoo 19 | Saudi-style tax invoice PDF with action button |

### Security & Access Control

| Addon | Version | Summary |
|---|---|---|
| [`el_readonly_user`](odoo18/el_readonly_user/) | Odoo 18 | Grant controlled read-only access to users |
| [`el_warehouse_access`](odoo18/el_warehouse_access/) | Odoo 18 | Control user access based on warehouse assignments - Global backend security enforcement |
| [`pos_restrict`](odoo18/pos_restrict/) | Odoo 18 | Restricts User access to pos and orders |
| [`el_button_access_control`](odoo19/el_button_access_control/) | Odoo 19 | Control button visibility per user group — show/hide buttons in any view without editing XML |

### Tools & Utilities

| Addon | Version | Summary |
|---|---|---|
| [`bi_global_custom_fields`](odoo18/bi_global_custom_fields/) | Odoo 18 | Adds custom fields to any model without writing XML |
| [`el_mobile_webhook`](odoo18/el_mobile_webhook/) | Odoo 18 | Reliable outbound status webhooks for mobile backends |
| [`wk_wizard_messages`](odoo18/wk_wizard_messages/) | Odoo 18 | To show messages/warnings in Odoo |
| [`auto_project_stages`](odoo19/auto_project_stages/) | Odoo 19 | Auto-create project stages (New, In Progress, Approval One/Two) and starter tasks on project creation |
| [`transaction_tracker`](odoo19/transaction_tracker/) | Odoo 19 | Track all user transactions across every Odoo module |
| [`el_dashboard_builder`](odoo20/el_dashboard_builder/) | Odoo 20 | Drag-and-drop dashboards with KPI, charts, tables, sharing, permissions and exports |

### Manufacturing

| Addon | Version | Summary |
|---|---|---|
| [`mrp_lock_lines`](odoo19/mrp_lock_lines/) | Odoo 19 | Lock all component lines in Manufacturing Order except the last one |

### Investment & Finance Products

| Addon | Version | Summary |
|---|---|---|
| [`investment_club`](odoo18/investment_club/) | Odoo 18 | Investment club management for Al-Namaa with a unified return system |
| [`vehicle_installment`](odoo19/vehicle_installment/) | Odoo 19 | Manage vehicle installments with automatic calculation |

### AI & Analytics

| Addon | Version | Summary |
|---|---|---|
| [`ai_finance_suite`](odoo19/ai_finance_suite/) | Odoo 19 | AI-Powered Finance Suite: Virtual CFO, OCR Engine & Smart Reconciliation for Odoo 19 |
| [`test_AI_finance`](odoo19/test_AI_finance/) | Odoo 19 | AI Finance V1: OCR engine for vendor bills plus a Virtual CFO chatbot (superseded by ai_finance_suite) |

### Core / Base

| Addon | Version | Summary |
|---|---|---|
| [`meno`](odoo17/meno/) | Odoo 17 | Writes a database.create_date system parameter if missing |
| [`meno`](odoo18/meno/) | Odoo 18 | Same database expiry bypass as odoo17/meno, targeting Odoo 18 |
| [`meno`](odoo19/meno/) | Odoo 19 | Same database expiry bypass as odoo17/meno, targeting Odoo 19 |
| [`meno`](odoo20/meno/) | Odoo 20 | Same database expiry bypass as odoo17/meno, targeting Odoo 20 |

## Odoo 17

### Sales

#### `ie_print_document_linked_order` — IE Print Document Linked Order

> version `0.1` · license `LGPL-3` · author: Ibrahim Elmasry · category: Sales

Show all product attachments directly from Quotation.

- Adds a button on the sale order form that lists every attachment linked to the order's product lines
- No context switch — attachments are shown inside the order itself

**Depends on** `base`, `sale`

### CRM

#### `ie_costem_lead_form` — ie_costem_lead_form

> version `0.1` · author: Ibrahim Elmasry · category: CRM

- Two large custom visit forms on `crm.lead`: Site Visit and Company Visit
- ~140 custom fields covering project details, contractor/consultant/supervisor contacts, and per-system data (Fire Alarm, Public Address, Data System, Access Control, BMS, CCTV, MATV)
- Signature fields and per-system notes/requirements
- 10 follow-up status checkboxes (Pending / In Progress / Done)
- `Specifications` many2many of product templates used to pre-fill quotations
- Quotation creation is blocked until specifications exist; products are injected as `default_order_line`

> **Note** — The `controllers/` folder is scaffolded but fully commented out.
> **Note** — `security/ir.model.access.csv` exists but is commented out in the manifest, so it is not loaded.

**Depends on** `base`, `crm`, `sale_management`

### Printing, Reports & PDF

#### `ie_crm_lead_pdf` — CRM Lead Print

> version `1.0` · author: Ibrahim Elmasry · category: CRM

- Adds a **Lead Report** QWeb-PDF action on `crm.lead`
- `binding_type=report`, so a print button appears on both the form and list views
- Print name pattern: `Lead - %s`

> **Note** — Only the report definition and its template are listed in the manifest; the other files under `views/` are not loaded.

**Depends on** `crm`

### Core / Base

#### `meno` — meno

> version `18.0` · author: meno

- Writes a `database.create_date` system parameter if missing
- Forces `database.expiration_date` far into the future
- Hooks `ir.module.module.button_immediate_upgrade()` and adds a 1-minute cron

> **Note** — **Not a business module.** It bypasses the Odoo Enterprise/online subscription expiry. Do not install it in production and do not redistribute it.

**Depends on** `base`, `base_setup`

## Odoo 18

### Point of Sale

#### `el_pos_customer_payment_method` — POS Customer Payment Method

> version `18.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Sales/Point of Sale · `README`](odoo18/el_pos_customer_payment_method/README.md), tests, JS

Restrict POS payment methods per customer, with POS-level defaults for customers without a specific list.

- Cashiers only see the payment methods each customer is allowed to use
- *Allowed POS Payment Methods* field on the customer form (Sales and Purchase tabs)
- Live filtering in the POS payment screen — the list refreshes as soon as the order partner changes
- *Default Payment Methods* per POS config for customers without their own list
- README + unit tests

> **Note** — Available for Odoo 18, 19 and 20.

**Depends on** `point_of_sale`

#### `pos_cashier_handover` — POS Cashier Handover Report

> version `18.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Point of Sale · JS

طباعة تسليم الخزينة عند إغلاق جلسة نقطة البيع.

- Arabic cashier handover sheet printed from the POS session
- Aggregates cash / card / transfer totals per payment method
- Includes cash-in and cash-out from the statement lines plus amounts delivered to accounts
- Prints automatically when the session is closed from the POS UI (`ClosePosPopup` patch)
- Own QWeb-PDF report and paper format

**Depends on** `point_of_sale`

#### `pos_get_weight_button` — POS Get Weight Button

> version `1.0` · license `LGPL-3` · category: Sales/Point of Sale

Get Weight POS button that reads a local scale and sets the line quantity.

- *Get Weight* control button in the POS product screen
- Reads the weight from a local scale service at `http://localhost:8000/api/weight`
- Writes the value into the selected order line quantity
- Validates that a line is selected and the weight is a positive finite number

> **Note** — Requires a local scale bridge service on port 8000.

**Depends on** `point_of_sale`

#### `pos_receipt_price_before_discount` — POS Receipt: Price Before Discount

> version `18.0.1.0.0` · license `LGPL-3` · category: Point of Sale · JS

Show product list price (before discount) under each receipt line when discounted.

- Shows the product list price under each receipt line when the sold price is lower
- Parses currency-formatted strings, handling `.` and `,` as decimal or thousand separators
- Resolves the product from the POS record cache to read `lst_price`

**Depends on** `point_of_sale`

#### `pos_refund_restriction` — POS Refund Restriction

> version `18.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Sales/Point of Sale · JS

Restrict refund operations in POS to administrators only.

- Refunds are limited to cashiers with the **manager** role
- Patches `TicketScreen` (`getHasItemsToRefund`, `_onUpdateSelectedOrderline`, `onDoRefund`) and shows an Access Denied dialog otherwise
- Also rejects negative quantities on `PosOrderline.set_quantity`

**Depends on** `point_of_sale`

### Sales

#### `bi_so_product_quantity_limit` — Sale Order Product Quantity Limit

> version `18.0.0.0` · license `OPL-1` · author: Ibrahim Elmasry · category: Sales

- Minimum and maximum orderable quantity per product
- Blocks saving or confirming a sale order that violates the limit
- Raises a warning instead of silently clamping the quantity

**Depends on** `base`, `sale`, `sale_management`

#### `el_kitchen_receipt` — Kitchen Receipt from Quotation

> version `18.0.4.1.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Sales/Sales · `README`](odoo18/el_kitchen_receipt/README.md), tests

Print kitchen receipt from sales quotation with customer delivery info auto-fill + pilot name sync with delivery.

- 80 mm thermal kitchen receipt printed straight from a quotation
- Pilot (driver) report as A4 PDF grouped by driver
- Delivery info fields on partner, sale order, picking and invoice
- Auto-fills delivery info from the contact, and syncs it back with a chatter entry
- Two-way sync of the driver name between the order and the contact
- README + unit tests

**Depends on** `sale`, `sale_stock`, `account`, `stock`

#### `el_sale_order_confirmation_user` — Sale Order Confirmation User

> version `18.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Sales/Sales · tests

Track which user actually confirmed each sales order.

- Adds *Confirmed By* on `sale.order` — the user who actually clicked Confirm
- Distinct from the salesperson, the creator and the last writer
- Adds a *Confirmed By* filter and group-by in the search view

**Depends on** `sale`

#### `ie_restrict_qty` — Ie Restrict Qty

> version `1.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Uncategorized

- `qty_restrict` maximum orderable quantity on `product.template`
- Constraint on `sale.order.line` raising an Arabic validation error when exceeded
- A limit of 0 means unrestricted

> **Note** — `security/ir.model.access.csv` exists but is commented out in the manifest.

**Depends on** `base`, `mail`, `stock`, `sale_management`

#### `sale_barcode_scanner` — Sale Order Barcode Scanner

> version `18.0.1.0.0` · license `LGPL-3` · author: Mohamed Helmy · category: Sales · JS

Scan products by Barcode/QRCode in sales orders using mobile camera or webcam.

- Scan product barcodes and QR codes inside a sale order using the device camera or a webcam
- `add_product_by_barcode()` matches `barcode` or `default_code`, incrementing existing lines or creating new ones at list price
- OWL scanner dialog with audio feedback and mobile camera support
- Button injected into the sale order form

> **Note** — Third-party module (Mohamed Helmy).

**Depends on** `sale_management`, `product`, `barcodes`

#### `sale_contract_auto` — Sale Contract Auto

> version `1.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Sales

Automatically generate contracts from sale orders.

- Create customer contracts automatically from sale orders
- Link contracts with their sale orders
- Generate contract PDFs and email the link to the customer
- Customers can read the contract from the portal

**Depends on** `base`, `sale_management`, `account`, `portal`, `mail`

#### `sale_kitchen_receipt` — Kitchen Receipt from Quotation

> version `18.0.1.0.0` · license `LGPL-3` · author: Your Company · category: Sales/Sales

Print kitchen receipt from sales quotation.

- 80 mm kitchen receipt printed from a sale order quotation
- Adds `x_building_floor`, `x_landmark` and `x_driver_name` on `sale.order`
- Own paper format and QWeb-PDF report

> **Note** — Earlier, simpler version of `el_kitchen_receipt`.

**Depends on** `sale`, `account`

#### `sale_order_automation` — Sale Order Automation

> version `1.1` · license `LGPL-3` · author: Ibrahim Elmasry

One-click invoice creation and delivery validation from the sale order.

- One-click invoice creation and delivery validation from the sale order

**Depends on** `sale_stock`

#### `sale_order_contract` — Sale Order Contract

> version `0.1` · license `LGPL-3` · author: Ibrahim Elmasry · category: Sales

Bilingual AR/EN supply-and-installation contract PDF rendered from a sale order (QWeb only).

- Bilingual (AR/EN) supply-and-installation contract PDF rendered from a sale order
- QWeb-only module — no Python models
- Contract terms for payment, delivery, warranty and cancellation
- Tailored to the Qatar market

> **Note** — `paperformat.xml` exists but is commented out in the manifest.

**Depends on** `base`, `sale`, `account`

#### `sale_order_contract_terms` — Sales Order Contract Terms (AR/EN) - 4 Pages

> version `18.0.1.0.0` · license `LGPL-3` · category: Sales

Sales order plus 4 contract pages with 9 bilingual AR/EN clauses.

- Improved version of the contract report: sales order plus 4 contract pages, 9 bilingual AR/EN clauses
- `technical_specification` on the product and sale order line, rolled up on the order
- Legal fields: `x_id_no` on the partner; establishment registration, representative and PO box on company and partner
- Arabic date formatting helper `get_date_arabic()`

**Depends on** `sale`

#### `sale_stock_restrict` — Sale Stock Restrict

> version `18.0.1.0.0` · license `AGPL-3` · author: Ibrahim Elmasry · category: Sales

Module helps to restrict out of stock products.

- Restricts out-of-stock products based on on-hand or forecast quantity

**Depends on** `base`, `sale_management`, `stock`, `account`

#### `sales_credit_limit` — Customer Credit Limit with Due Amount Warning

> version `18.0.1.0.0` · license `OPL-1` · author: Ibrahim Elmasry · category: Sales

An advanced way to handle customer credit limit through warning and blocking stage.

- Customer credit limit with a warning stage and a blocking stage
- Shows the customer's due amount while creating an order

**Depends on** `base`, `sale_management`

### Purchase

#### `el_purchase_actual_qty` — Purchase Actual Quantity

> version `18.0.2.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Purchases · `README`](odoo18/el_purchase_actual_qty/README.md), tests, JS

Actual purchase quantity with preserved value, dashboard and reporting.

- `actual_qty`, `effective_price_unit`, `variance_qty`, `variance_percent` on purchase order lines
- Original commercial value is preserved while the invoice bills the physical quantity
- `_prepare_stock_moves()` prorates quantities and uses the effective unit cost
- `_prepare_account_move_line()` keeps the ordered value and overrides `qty_to_invoice`
- SQL view `el.purchase.actual.report` with variance bands (none / low / medium / high)
- OWL dashboard, CSV export controller and settings (allow-over, warning & critical thresholds)
- README + unit tests

**Depends on** `purchase`, `purchase_stock`, `stock_account`

#### `wm_purchase_global_discount` — Purchase Order Global Discount (Same as Odoo Sales Discount)

> version `1.0.0` · license `OPL-1` · author: Ibrahim Elmasry · category: Purchase

- Global discount on purchase orders, mirroring the Odoo sales discount behaviour

**Depends on** `purchase`

### Inventory & Warehouse

#### `delivery_return_reason` — Delivery Return Reasons

> version `18.0.1.0.1` · license `LGPL-3` · author: Your Company · category: Inventory/Delivery

تتبع أسباب رجوع الطلبات مع إحصائيات وتحليلات.

- New model `delivery.return.reason` (name, sequence, active, company)
- `stock.picking` tracks returned state, reason and note
- `stock.return.picking` makes the reason mandatory and stamps it on the generated return
- Pivot and graph views on `stock.picking` grouped by return reason
- Also carries the driver name from the sale order

> **Note** — Depends on `el_kitchen_receipt`, but its code reads `sale.order.x_driver_name` from `sale_kitchen_receipt` — install `sale_kitchen_receipt` too.

**Depends on** `stock`, `el_kitchen_receipt`

#### `el_barcode_price_display` — Barcode Price Display

> version `18.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Inventory/Inventory · `README`](odoo18/el_barcode_price_display/README.md), tests, JS

Standalone barcode scanner price display page — no login needed.

- Standalone page at `/price-display` — **no login required**
- Listens to raw scanner keyboard input (200 ms debounce), no input field or Enter key needed
- Shows product name, large price and image; red "Product Not Found" otherwise
- Result clears after 3 seconds, ready for the next scan
- README + unit tests

**Depends on** `base`, `product`

#### `el_product_traceability_dashboard` — Product Traceability Dashboard

> version `18.0.2.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Inventory/Inventory · `README`](odoo18/el_product_traceability_dashboard/README.md), JS

Product traceability dashboard with returns, scrap and manufacturing genealogy.

- SQL view `el.product.traceability.report` classifying nine operation types with signed quantities
- Unit cost / total value taken from `stock_valuation_layer` and purchase price
- `el.product.traceability.manufacturing` for finished-good and component genealogy
- OWL dashboard transient model with `get_dashboard_data()` and current-stock from quants
- List, pivot, graph views plus two QWeb-PDF reports
- Company-scoped behind its own access group

**Depends on** `stock`, `purchase`, `sale_management`, `mrp`, `account`

#### `inventory_report_generator` — Inventory All In One Report Generator

> version `18.0.1.0.0` · license `AGPL-3` · author: Ibrahim Elmasry · category: Productivity · JS

- Dynamic inventory reports generated from a wizard
- Pick products, dates and grouping; export the result

> **Note** — The manifest summary still says "for Odoo 17" although the module lives under `odoo18/`.


**Development batch 01 changes (Odoo 18/19):** company restrictions were added to relevant SQL report queries; date values are parameterized; redundant report computation was removed; spreadsheet formula/link auto-conversion was disabled; export routes were restricted to the expected report model and XLSX format; exception details are logged server-side instead of returned to clients. Runtime multi-company and export tests are still pending.

**Depends on** `stock`

#### `invoice_stock_move` — Stock Picking From Invoice

> version `18.0.1.0.0` · license `AGPL-3` · author: Ibrahim Elmasry · category: Accounting

Create stock deliveries and receipts from a customer invoice or vendor bill.

- Create customer deliveries / supplier receipts directly from an invoice or bill

**Depends on** `account`, `stock`, `payment`

#### `product_movement_report` — Product Movement Lifecycle Report

> version `18.0.1.0.0` · license `LGPL-3` · category: Inventory/Reporting

Full movement history of a product/lot from first receipt until fully sold.

- Full movement history of a product or lot from the first receipt until fully sold
- Every done stock move in chronological order with a running balance
- Split into cycles — a cycle ends when on-hand returns to zero
- List view plus landscape PDF

**Depends on** `stock`

#### `stock_move_invoice` — Invoice From Stock Picking

> version `18.0.1.0.0` · license `AGPL-3` · author: Ibrahim Elmasry · category: Extra Tools

Create invoice for stock picking.

- Create customer invoices, vendor bills, credit notes and refunds from a stock picking

**Depends on** `stock`, `account`

#### `stock_split_transfer` — Stock Split Transfer

> version `18.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Inventory/Warehouse

Two-step internal transfers with per-user location visibility.

- Splits internal transfers into two legs: Source → Transit → Destination
- Each leg is only visible to users with access to its location
- The second leg appears only after the first leg is validated

**Depends on** `base`, `stock`

#### `transfer_wizard` — trade_paints_wizard

> version `1.1` · author: Ibrahim Elmasry · category: Uncategorized

- Delivery transfer wizard recording the driver and vehicle on stock pickings
- `expected_weight` defaults to the summed weight of the selected pickings
- `validate()` writes driver, car number and `printed_before`, then prints the delivery report
- Adds `driver_name`, `car_number` and `printed_before` to `stock.picking`

> **Note** — **Broken:** `validate()` calls `env.ref('trad_paints_delivery_report')`, a module that does not exist in this repository — printing will fail.
> **Note** — Folder and manifest names say `trade_paints_wizard`.
> **Note** — `security/ir.model.access.csv` is commented out in the manifest.

**Depends on** `base`, `sale`, `sale_management`, `stock`, `purchase`

### Accounting & Finance

#### `account_invoice_fixed_discount` — Account Fixed Discount

> version `18.0.1.0.0` · license `AGPL-3` · author: Ibrahim Elmasry · category: Accounting & Finance · tests

Allows to apply fixed amount discounts in invoices.

- Monetary `discount_fixed` on invoice and bill lines
- Internally converted to a percentage so taxes and totals stay correct
- `_compute_totals()` recomputes subtotal/total for fixed-discount lines with unrounded values
- Mutual onchange between percentage and fixed discount
- Restricted to a `group_fixed_discount` group inside the invoicing group
- Discount is printed on the invoice report
- Includes unit tests

> **Note** — OCA / ForgeFlow code.

**Depends on** `account`

#### `el_restrict_journal` — Restrict Journal for Users (Whitelist)

> version `18.0.2.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Accounting/Management · `README`](odoo18/el_restrict_journal/README.md), tests

Per-user journal whitelist — only allowed journals are visible.

- *Allowed Journals* whitelist field on `res.users`
- Users only see and use the whitelisted journals — the rest are completely hidden, not just read-only
- Empty list means full access
- README + unit tests

**Depends on** `base`, `account`

### CRM

#### `archer_meta_lead_ads` — Meta Lead Ads

> version `18.0.1.0.0` · license `LGPL-3` · author: Archer Solutions · category: Sales/CRM · `README`](odoo18/archer_meta_lead_ads/README.md)

Import Meta lead ads into CRM leads.

- Stores Meta (Facebook) credentials, pages, lead forms and field mappings
- Imports Meta leads into `crm.lead` with UTM attribution
- Has its own README with setup steps

**Depends on** `crm`, `mail`, `contacts`, `utm`

### Healthcare & Services

#### `bi_health_care_center_management` — Health Care Center Management

> version `18.0.0.0` · license `OPL-1` · author: BrowseInfo · JS

Manage Health Care Center Management Operations Industry Management Services Custom Health Care Solution.

- Patients, appointments, departments, services and billing
- Portal for guest/registered inquiries and registration requests
- Membership registrations, invoice payments and event registrations
- Dashboard for sports/activity oversight

> **Note** — Third-party (BrowseInfo) module with a very broad dependency list (mail, account, product, website, contacts, event, stock, hr_attendance, purchase).

**Depends on** `base`, `mail`, `account`, `product`, `website`, `contacts`, `event`, `website_event_sale`, `stock`, `hr_attendance`, `purchase`

#### `bi_sport_center_management` — Sport Center Management

> version `18.0.0.0` · license `OPL-1` · author: Ibrahim Elmasry · JS

- Sport club / fitness centre operations
- Member registrations, inquiries and invoice payments
- Event registrations and activity dashboards
- Customer portal for guests and registered users

**Depends on** `base`, `mail`, `account`, `product`, `website`, `contacts`, `event`, `website_event_sale`, `stock`, `purchase`

### E-Commerce & Connectors

#### `odoo_multi_channel_sale` — Odoo Multi-Channel Sale

> version `2.8.24` · license `Other proprietary` · author: Webkul Software Pvt. Ltd. · category: eCommerce · tests, JS

- Base connector that links Odoo to several marketplaces (Webkul)
- Channel configuration, mapping of products, categories, partners and orders
- Import and export wizards, order feeds and a status connector
- Shared message/warning dialogs via `wk_wizard_messages`
- Unit tests

> **Note** — Foundation for `odoo_salla_integration`.


**Development batch 01 changes (Odoo 18):** unsafe `eval()` parsing was replaced with `ast.literal_eval()`/controlled attribute lookup; dashboard filters were allowlisted; SQL date/channel values were parameterized; dashboard queries and channel access were constrained by allowed companies; error-counter table names were restricted to an internal allowlist. Public webhook authentication/signature verification remains a separate critical review item.

**Depends on** `stock_delivery`, `wk_wizard_messages`

#### `odoo_salla_integration` — Salla Odoo Connector | Odoo Multichannel

> version `2.0.4` · license `Other proprietary` · author: Webkul Software Pvt. Ltd. · category: eCommerce · `README`](odoo18/odoo_salla_integration/README.md), tests

- Salla (Saudi e-commerce) connector on top of `odoo_multi_channel_sale`
- Product, category, partner and order sync in both directions
- Order feeds with dedicated models for orders and products
- Audit log, repair wizard and backfill wizard for historic data
- Refund sync and adjustment handling
- ZATCA e-invoicing XML generation (depends on `l10n_sa_edi`)
- Webhook fallback sweep re-checks the last 14 days of orders every run, because Salla's order list does not follow the update sort
- Access token is checked once per import run instead of once per page
- Configurable 0% tax applied to order lines that arrive without a tax (`salla_zero_tax_id`)
- New crons, server actions and security access file
- changelog.md, README and unit tests


**Development batch 01 changes (Odoo 18):** stored product option/variant values are parsed with `ast.literal_eval()` instead of `eval()`. Integration behavior still requires live Salla sandbox tests.

**Depends on** `odoo_multi_channel_sale`, `l10n_sa_edi`

#### `whatsapp_mail_messaging` — Odoo Whatsapp Connector

> version `18.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Extra Tools · JS

- Send WhatsApp messages and emails from the systray, sale orders, invoices and the website portal
- Share access URLs for documents through the share action using WhatsApp Web

**Depends on** `sale`, `account`, `website`, `sale_management`

### Printing, Reports & PDF

#### `pdf_print_preview` — Pdf Print Preview

> version `18.0.1.0.0` · license `OPL-1` · author: Ibrahim Elmasry · JS

Preview and print PDF report in your browser | Pdf direct preview | Print without Download.

- Preview and print PDF reports in the browser without downloading the file

> **Note** — Early version of the feature later reworked as `odoo19/el_pdf_print_preview`.


**Development batch 01 changes (Odoo 18):** raw traceback details are no longer exposed in generated error PDFs; technical details are logged server-side and users receive a generic message while functional `UserError`/`ValidationError` messages remain available.

**Depends on** `web`

#### `prt_report_attachment_preview` — Open PDF Reports and PDF Attachments in Browser

> version `18.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Productivity · tests, JS

- Overrides the core `ReportController.report_routes` to force `Content-Disposition: inline`
- Adds `/report/check_wkhtmltopdf` with sticky wkhtmltopdf state notifications
- Client-side `open_report_handler` opens the PDF in a new browser tab, warning if the popup was blocked
- Unit tests

**Depends on** `web`

### Security & Access Control

#### `el_readonly_user` — EL Readonly User Access

> version `18.0.1.2.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Extra Tools · JS

Grant controlled read-only access to users.

- A user group that can read permitted business data but cannot create, write or delete
- Hides Configuration and Settings menus for the group
- Inventory and stock movements stay readable

**Depends on** `base`, `web`

#### `el_warehouse_access` — Warehouse-Based Access Control

> version `18.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Inventory · `README`](odoo18/el_warehouse_access/README.md), tests

Control user access based on warehouse assignments - Global backend security enforcement.

- Assign one or more warehouses to each user
- Global `ir.rule` enforcement across every stock model
- Filters stock operations, locations and reports by the user's warehouses
- README + unit tests

**Depends on** `base`, `stock`, `sale_stock`

#### `pos_restrict` — POS User Restrict

> version `18.0.1.0.0` · license `AGPL-3` · author: Cybrosys Techno Solutions · category: Point of Sale

Restricts User access to pos and orders.

- Restricts user access to POS sessions and orders
- A user may manage several POS locations according to their permissions

**Depends on** `point_of_sale`

### Tools & Utilities

#### `bi_global_custom_fields` — All in one add custom fields -Global Custom Fields

> version `18.0.0.5` · license `OPL-1` · author: BROWSEINFO · category: Extra Tools · JS

- Adds custom fields to any model without writing XML
- Global custom fields and global tabs

> **Note** — Large third-party (BrowseInfo) module; several hundred fields across many models.

**Depends on** `base`

#### `el_mobile_webhook` — Mobile Webhook

> version `18.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Technical · `README`](odoo18/el_mobile_webhook/README.md), tests

Reliable outbound status webhooks for mobile backends.

- Reliable outbound webhooks for sale order, delivery, invoice and payment status changes
- Queue model `mobile.webhook.event` with UUID, event type, JSON payload and state (pending / retrying / sent / failed / cancelled)
- HMAC-SHA256 signature in `X-Odoo-Webhook-Signature`, plus id/event headers
- Cron drains the queue in batches of 50 using savepoints, with exponential backoff
- Settings for endpoint, secret, timeout and retry limit with HTTPS validation
- Manual retry / cancel / send-now actions
- README + unit tests

**Depends on** `base_setup`, `sale`, `stock`, `account`

#### `wk_wizard_messages` — Webkul Message Wizard

> version `1.0.0` · license `Other proprietary` · author: Webkul Software Pvt. Ltd. · category: Extra Tools

To show messages/warnings in Odoo.

- `wk.wizard.message` transient model with a single HTML field
- `genrated_message(message, name)` returns a popup `act_window` view
- Used by `odoo_multi_channel_sale` to surface connector warnings
- Banner image asset

> **Note** — Declares no `depends` — it is a standalone Webkul helper module (Other proprietary).

### Investment & Finance Products

#### `investment_club` — Investment Clubs Management

> version `18.0.12.0.0` · license `LGPL-3` · author: Woledge · category: Investment · JS

- Investment club management for Al-Namaa with a unified return system
- Unique customer membership number
- Clubs, projects, memberships, investments and return payments
- Investments and returns are shown by membership number
- Bilingual (Arabic / English) club data

**Depends on** `base`, `mail`, `account`, `analytic`, `product`, `contacts`, `crm`, `sale_contract_auto`, `web`

### Core / Base

#### `meno` — meno

> version `18.0` · author: meno

- Same database expiry bypass as `odoo17/meno`, targeting Odoo 18

> **Note** — **Not a business module.** Bypasses the Odoo subscription expiry — do not use in production or redistribute.

**Depends on** `base`, `base_setup`

## Odoo 19

### Point of Sale

#### `el_pos_customer_payment_method` — POS Customer Payment Method

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Sales/Point of Sale · `README`](odoo19/el_pos_customer_payment_method/README.md), tests, JS

Restrict POS payment methods per customer, with POS-level defaults for customers without a specific list.

- Odoo 19 port — see `odoo18/el_pos_customer_payment_method`

**Depends on** `point_of_sale`

#### `pos_daily_sequence` — POS Daily Sequence

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Point of Sale

Automatically reset POS order numbering every day.

- Daily POS order numbering per POS configuration — each config gets its own date-range sequence
- Numbering restarts at 1 every day
- Configurable prefix with date placeholders
- Independent counters for multiple POS locations

**Depends on** `point_of_sale`, `mail`, `stock`, `account`

#### `pos_get_weight_button` — POS Get Weight Button

> version `1.0` · license `LGPL-3` · category: Sales/Point of Sale

Get Weight POS button reading a local scale (Odoo 19 port, logs only).

- *Get Weight* button in the POS control buttons
- Fetches `http://localhost:8000/api/weight` from the local scale service

> **Note** — **Incomplete on Odoo 19:** the response is only logged — no quantity update, validation or user notification.

**Depends on** `point_of_sale`

### Sales

#### `bi_so_product_quantity_limit` — Sale Order Product Quantity Limit

> version `19.0.0.0` · license `OPL-1` · author: BROWSEINFO · category: Sales

- Odoo 19 port of the sale order min/max quantity limit

**Depends on** `base`, `sale`, `sale_management`

#### `customer_classification` — Customer Classification & Credit Control

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Sales/Sales · `README`](odoo19/customer_classification/README.md)

Classify customers into tiers (A-E) with inherited price lists, credit limits, and payment terms.

- Customer tiers A–E, each with a default price list, credit limit and payment term
- Changing the tier cascades the price list to every customer in it
- Credit limit applies the Block / Warning policy
- Individual overrides stay possible
- README

**Depends on** `sale`, `account`

#### `el_commission_type` — Commission Types

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Sales

Manage sales commission types by team member role.

- Sales commission types per team member role (General Manager, Team Manager, Team Leader, Salesperson)
- Auto-generated commission names such as `General Manager 0%`
- Commission percentage with a visual widget
- Multi-company support

**Depends on** `base`, `mail`

#### `el_nmo_classification` — El-Nmo - Customer Classification

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Sales/Sales

- Customer tiers A–E with price list, credit limit, payment term and credit policy per tier
- Auto-classification based on sales, balance and age metrics
- Daily cron re-classifies customers automatically

> **Dependency status** — `el_nmo_sale_payment_gateway` is included in this repository under Odoo 19.

**Depends on** `base`, `mail`, `sale`, `account`, `el_nmo_sale_payment_gateway`

#### `el_nmo_credit_approval` — El-Nmo - Credit Limit Approval Workflow

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Sales/Sales · `README`](odoo19/el_nmo_credit_approval/README.md), tests

Approval workflow for sale orders exceeding customer credit limits.

- Credit check on sale order confirmation
- When the policy is *Block Sale* and the limit is exceeded, creates an approval request instead of raising a hard error
- Supervisor approves or rejects with the full credit context
- README + unit tests

> **Note** — Depends on `el_nmo_classification`.

**Depends on** `base`, `mail`, `sale`, `el_nmo_classification`


### Sales

#### `el_nmo_sale_payment_gateway` — Sale Payment Gateway

> version `19.0.1.2.0` · license `LGPL-3` · author: Zelal Alhayek · category: Sales

Centralizes payment-gateway configuration and propagates the selected gateway across partner, sales, accounting and stock documents.

**Business workflow**
1. An administrator creates a Payment Gateway from Sales → Configuration → Payment Gateways.
2. The gateway can define company-dependent default receivable and payable accounts.
3. Selecting the gateway on a partner fills the partner's receivable/payable account properties; the partner form presents those account values as read-only.
4. A sales order stores the selected gateway. Its invoice receives the gateway and delivery-carrier values during invoice preparation.
5. Stock moves and pickings carry the gateway reference; carrier changes are synchronized between the sales order and non-completed/non-cancelled pickings.
6. Updating gateway account defaults propagates the configured values to linked partners.

**Technical components**
- `sale.payment.gateway`: gateway master with active flag and company-dependent receivable/payable accounts.
- Extensions: `res.partner`, `sale.order`, `account.move`, `stock.picking`, and `stock.move`.
- Server-side synchronization: partner `create()`/`write()`, gateway `write()`, sales-order `write()` and invoice preparation, picking `write()`, stock-move picking-value preparation.
- Views: gateway configuration, partner, sales order, invoice and stock picking forms.
- Security: `security/ir.model.access.csv`.

**Dependencies**: `sale_management`, `account`, `stock`, `delivery`.

**Review notes**: the gateway `write()` uses `sudo()` to update linked partners across record-rule boundaries. Validate company ownership, allowed-company behavior and audit expectations in a multi-company test database. The partner synchronization code should also be tested when a gateway account is cleared, when multiple companies use different property accounts, and when a batch write contains partners from different companies.

### Purchase

#### `wm_purchase_global_discount` — Purchase Order Global Discount (Same as Odoo Sales Discount)

> version `1.0.0` · license `OPL-1` · author: Ibrahim Elmasry · category: Purchase

- Odoo 19 port of the purchase order global discount

**Depends on** `purchase`

### Inventory & Warehouse

#### `el_barcode_price_display` — Barcode Price Display

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Inventory/Inventory · `README`](odoo19/el_barcode_price_display/README.md), tests, JS

Standalone barcode scanner price display page — no login needed.

- Odoo 19 port of the standalone `/price-display` scanner page
- README + unit tests

**Depends on** `base`, `product`

#### `el_inter_company_transfer` — Inter Company Transfer

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Warehouse / Inventory

Automate inter-company stock, sale, purchase, and accounting documents.

- Automates stock and accounting transactions between companies in one database
- Creates and links sale orders, purchase orders, pickings, customer invoices, vendor bills and returns
- Rules are configured per company pair

**Depends on** `base`, `mail`, `stock`, `sale_management`, `sale_stock`, `purchase`, `purchase_stock`, `account`

#### `el_prevent_negative_stock` — Prevent Negative Stock

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Inventory/Security · `README`](odoo19/el_prevent_negative_stock/README.md), tests

- Rejects any stock move that would make a product's quantity negative (delivery, internal, MRP)
- Blocks sale order confirmation when products are short
- No exceptions — even managers cannot override
- README + unit tests

> **Note** — Depends on `nmo_sale_order_approval_workflow` and `nmo_stock_user_restriction`, modules not present in this repository.

**Depends on** `base`, `stock`, `mail`, `sale_management`, `nmo_sale_order_approval_workflow`, `nmo_stock_user_restriction`

#### `inventory_report_generator` — Inventory All In One Report Generator

> version `19.0.1.0.0` · license `AGPL-3` · author: Cybrosys Techno Solutions · category: Productivity · JS

- Odoo 19 port of the dynamic inventory report generator

> **Note** — The manifest summary still says "for Odoo 17".

**Depends on** `stock`

#### `invoice_stock_move` — Stock Picking From Invoice

> version `19.0.1.0.0` · license `AGPL-3` · author: Cybrosys Techno Solutions · category: Accounting

Create stock deliveries and receipts from a customer invoice or vendor bill.

- Odoo 19 port — create deliveries and receipts from an invoice or bill

**Depends on** `account`, `stock`, `payment`

#### `smsa_express_delivery_carrier` — SMSA Express Shipping Integration

> version `1.0.3` · license `Other proprietary` · author: Webkul Software Pvt. Ltd. · category: Warehouse · tests

- SMSA Express integration with the SECOM customer application
- Shipment creation and tracking against Odoo deliveries
- Unit tests

> **Note** — Depends on `odoo_shipping_service_apps`, a module not present in this repository.

**Depends on** `odoo_shipping_service_apps`

#### `stock_intercompany_transfer` — Inter Company Stock Transfer

> version `19.0.1.0.0` · license `AGPL-3` · author: Cybrosys Techno Solutions · category: Inventory

Create counterpart Receipt/Delivery Orders between companies.

- Automatically creates the counterpart receipt or delivery in the other company when a transfer is validated

> **Note** — Simpler alternative to `el_inter_company_transfer`, which also covers sales, purchase and accounting documents.

**Depends on** `stock`, `account`

### Accounting & Finance

#### `account_invoice_fixed_discount` — Account Fixed Discount

> version `19.0.1.0.0` · license `AGPL-3` · author: ForgeFlow, Odoo Community Association (OCA) · category: Accounting & Finance · tests

Allows to apply fixed amount discounts in invoices.

- Odoo 19 port of `account_invoice_fixed_discount`
- Monetary `discount_fixed` on invoice and bill lines converted to a percentage
- `_compute_totals()` recomputes subtotal/total with taxes for discounted lines
- Mutual percentage / fixed onchange guarded by the `ignore_discount_onchange` context
- Restricted to a `group_fixed_discount` group
- Disables itself when `account_invoice_triple_discount` is installed
- Includes unit tests

**Depends on** `account`

#### `cheque_tracking` — Cheque Tracking

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Accounting/Payment

Track received and issued cheques with accounting lifecycle entries.

- Received and issued cheque lifecycles
- Automatic accounting entries at every transition (receipt, deposit, clearance, return, issue, cash) using configurable accounts
- Batch deposit and return processing, including bank charges and penalties
- Post-dated and stale cheque monitoring
- Cheque printing and deposit slip reports
- Per-partner cheque counters and audit chatter

> **Note** — Base module for `cheque_tracking_endorsement`.

**Depends on** `base`, `mail`, `account`

#### `cheque_tracking_endorsement` — Cheque Tracking Endorsement

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Accounting/Payment

- Full cheque endorsement workflow with audit records
- `cheque.endorsement` model with its own sequence, endorser/endorsee and state (draft / confirmed / cancelled)
- Automatic journal entries through a configurable endorsement payable account (2 or 4 lines)
- Optional vendor bill for the new beneficiary
- New cheque state *endorsed* plus `action_endorse()` and a reversal path on cancel
- Endorsement wizard with group checks and post-dated cheque rules
- Cron reminders for maturing and stale endorsed cheques

> **Note** — Requires `cheque_tracking`. Includes an `init()` SQL migration for legacy column names.

**Depends on** `cheque_tracking`

#### `el_cheque_tracking` — EL Cheque Tracking

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Accounting/Payment · `README`](odoo19/el_cheque_tracking/README.md), tests

Track received and issued cheques with accounting lifecycle entries.

- Odoo 19 version of the cheque module, with the same state machine and accounting behaviour as `cheque_tracking`
- Full received / issued lifecycle, batch deposit wizard, return wizard (bank charges + penalty), print wizard
- PDC maturity reminders and stale-cheque monitoring
- README + unit tests

> **Note** — A maintained replacement for `odoo19/cheque_tracking` — install one of the two, not both.

**Depends on** `base`, `mail`, `account`

#### `invoice_tracking` — Invoice Tracking

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: accounting

- Tracks inbound vendor invoices through receive → administration → bill
- `invoice.tracking` with PO link, vendor references, sequence and an EGP/USD percentage split constrained to 100%
- Computes conversions from USD/EGP rates, plus oil-well number
- `action_create_bill_from_invoice_tracking` generates the vendor bill from the PO's billable lines
- `check.tracking` cheque lifecycle with automatic journal entries per stage (receive, deposit, clear, bounce, issue, cash)
- `partner.code` model linking partners, bills and purchase orders
- Cheque accounts exposed in company settings; smart buttons on purchase orders

> **Note** — The manifest still carries the placeholder description "Detailed description of the module".

**Depends on** `base`, `mail`, `account`, `purchase`

### Human Resources

#### `WPS` — WPS

> version `1.0`

Export payroll payslips as a WPS SIF CSV for Qatar wage protection.

- Exports payroll payslips as a WPS (Qatar Wages Protection System) SIF CSV file
- Builds the WPS header: employer/payer EID, creation date, payer bank, IBAN, salary year-month, totals, record count, SIF version
- One row per employee with QID (from `employee.barcode`), bank, IBAN, frequency and 30 working days
- One column per distinct payslip line name
- Returns the CSV as an `ir.attachment` download action

> **Note** — Employer EID, IBAN and bank name are hard-coded.
> **Note** — The manifest has no summary or description.

**Depends on** `base`, `hr_payroll`

#### `bi_employee_travel_managment` — HR Employee Travel Expense in Odoo

> version `19.0.0.0` · license `OPL-1` · author: BROWSEINFO · category: human resources

- Employee travel requests and travel expense management
- Expense advances, claims and reimbursement workflow
- Menus for Employee Travel and Travel Expense

> **Note** — Third-party (BrowseInfo) module.

**Depends on** `base`, `hr`, `hr_expense`, `project`

#### `deduction_management` — Deduction

> version `19.0.2.0.0` · license `Other proprietary` · author: Abdullah Al-Habbal · category: Hidden

- Employee deductions with automatic payroll integration
- Depends on `hr_work_entry_enterprise` (Odoo Enterprise HR)

**Depends on** `base`, `hr_payroll`, `hr_work_entry_enterprise`

#### `el_hr_attendance_sheet` — HR Attendance Sheet And Policies

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Human Resources/Attendance · `README`](odoo19/el_hr_attendance_sheet/README.md), tests

Calculate overtime, lateness, absence from attendance and feed payslip.

- Public holidays with employee / department / tag scoping
- Configurable overtime rules per type (working day, weekend, public holiday)
- Multi-step lateness penalty matrix (rate or amount based)
- Multi-step absence penalty rules and escalation tiers
- Attendance policies and payslip feed
- README, docs/ and unit tests

> **Note** — Ports available for Odoo 19 and Odoo 20.

**Depends on** `base`, `hr_attendance`, `hr`, `hr_payroll`, `hr_holidays`, `mail`, `calendar`

#### `el_payroll_wps` — Payroll WPS Export

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Human Resources/Payroll · `README`](odoo19/el_payroll_wps/README.md), tests

Adds an 'Others' field to payslips and a WPS CSV export action.

- Adds an *Others* field to the payslip (informational, does not affect net salary)
- *WPS Export* wizard producing the CSV required for WPS bank submission
- Columns: bank, account, salary, notice (month), name, ID number
- README + unit tests

**Depends on** `base`, `hr_payroll`

#### `loan_management` — Loans Management

> version `19.0.2.0.0` · license `Other proprietary` · author: Abdullah Al-Habbal · category: Hidden

- Employee loans with payroll deduction and repayment tracking

**Depends on** `base`, `hr_payroll`

#### `rm_hr_attendance_sheet` — HR Attendance Sheet and Policies

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Human Resources/Attendances

- Policy-driven attendance sheets
- Overtime, lateness and absence calculation with public holiday handling
- Batch sheet creation and payslip linkage
- Audit notes for manual changes

> **Note** — An alternative implementation to `el_hr_attendance_sheet` — pick one.

**Depends on** `hr_attendance`, `hr_holidays`, `hr_payroll`, `mail`

#### `zk_attendance_integration_v19` — TechScope | ZK Attendance Integration

> version `1.0` · category: Human Resources

Integration with ZK Attendance Machines.

- Imports attendance punches from ZK attendance machines

**Depends on** `base`, `hr`, `hr_attendance`

### CRM

#### `archer_meta_lead_ads` — Meta Lead Ads

> version `18.0.1.0.0` · license `LGPL-3` · author: Archer Solutions · category: Sales/CRM · `README`](odoo19/archer_meta_lead_ads/README.md)

Import Meta lead ads into CRM leads.

- Odoo 19 port of the Meta Lead Ads connector
- Credentials, pages, forms, field mappings and lead import into `crm.lead` with UTM
- README

**Depends on** `crm`, `mail`, `contacts`, `utm`

#### `crm_project_linker` — CRM Project Linker

> version `1.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: CRM

Create and link projects from CRM opportunities.

- Create a project directly from an opportunity or link an existing one
- Open the opportunity from the project
- Share quotations between the opportunity and the project

**Depends on** `base`, `project`, `crm`, `sale_management`

#### `partner_request` — Partner Request

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Sales/Sales · `README`](odoo19/partner_request/README.md)

Approval workflow for creating new customers via sales requests.

- Sales team submits a request to create a customer, instead of creating it directly
- Five-state workflow: Draft → Pending → Approved / Rejected / Sent Back
- Auto-generated request numbers (`PRQ-YYYY-NNNNN`)
- Manager approval with reject and send-back
- README

**Depends on** `sale`, `sales_team`, `customer_classification`

### Construction

#### `el_construction_management` — Construction Management

> version `19.0.1.24.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Construction · `README`](odoo19/el_construction_management/README.md), tests, JS

Construction Management | Job Costing | BOQ | Work Orders | RA Billing | Material Requisition | Subcontracting | Budget.

- Projects, sub-projects, BOQ, budgets and rate analysis
- Phases (WBS), work orders, material requisitions with approvals
- Subcontracting, progress / RA billing, consume orders and completion certificates
- Quality checks, tasks and extra expenses
- Real-time dashboard
- README + unit tests

> **Note** — Foundation for `el_construction_tender`.

**Depends on** `base`, `mail`, `contacts`, `hr`, `stock`, `stock_account`, `purchase`, `account`, `project`, `web_gantt`

#### `el_construction_tender` — Construction Tendering

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Construction · JS

Client Tenders (Bid Costing & Submission) + Subcontractor/Vendor RFQ & Bid Comparison.

- Client tenders: track the tenders you bid for, price each BOQ item (direct cost + overhead % + profit %) and submit
- On a win, generates a Project / Sub Project / BOQ in `el_construction_management`
- Subcontractor and vendor RFQ with bid comparison

**Depends on** `base`, `mail`, `contacts`, `el_construction_management`

### Healthcare & Services

#### `el_hospital` — Hospital Management System

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Services/Hospital · tests, JS

- Patient registration and management
- Appointment scheduling with a calendar view
- Electronic Medical Records and prescriptions with PDF printing
- Departments, wards and beds with occupancy tracking
- Admission / discharge workflow
- Laboratory tests, radiology orders, pharmacy and billing
- Unit tests


**Development batch 01 changes (Odoo 19):** dashboard API responses no longer expose internal exception details; full details are retained in server logs.

**Depends on** `base`, `mail`, `hr`, `stock`, `account`, `sale_management`, `web`

### E-Commerce & Connectors

#### `connector_foodics` — Foodics Connector

> version `19.0.1.0.0` · license `LGPL-3` · author: Woledge · category: Sales/Point of Sale · tests

Bidirectional synchronization bridge between Odoo and Foodics POS.

- Bidirectional sync with the Foodics POS API v2
- Products, categories, customers, orders, inventory, taxes
- Webhooks, mapping, monitoring and retries
- Unit tests


**Development batch 01 changes (Odoo 19):** webhook payloads are validated as JSON objects; malformed JSON is distinguished from internal processing errors; internal exception text is not returned by the public endpoint. Signature/secret verification and live webhook replay tests remain required.

**Depends on** `account`, `contacts`, `mail`, `point_of_sale`, `product`, `sale_management`, `stock`

#### `ebook_serial_delivery` — eBook Serial Delivery

> version `19.0.1.1.0` · license `LGPL-3` · author: Custom Development · category: Website/eCommerce · tests

Deliver eBook licenses using standard Inventory Serial Numbers (stock.lot) — no custom "activation code" model.

- Delivers e-book licenses using the standard Inventory serial numbers (`stock.lot`) instead of a custom activation-code model
- Licenses are stocked the normal way: Inventory > Products > Update Quantity > Serial Numbers
- On sale, a license is reserved and delivered as an attachment
- README + unit tests

**Depends on** `website_sale`, `sale_stock`, `mail`

#### `el_ebook_store` — E-Book Store

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Website/eCommerce · `README`](odoo19/el_ebook_store/README.md), tests

Sell e-books with unique access codes — online reader + download.

- Sell e-books on the Odoo eCommerce website
- Generates unique access codes (random or manual), each usable once per customer
- Online PDF reader in the portal plus a per-book download option
- *My Library* page for customers and an admin sales dashboard
- README + unit tests

**Depends on** `base`, `sale`, `sale_management`, `website_sale`, `payment`, `portal`, `mail`

#### `whatsapp_mail_messaging` — Odoo Whatsapp Connector

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Extra Tools · JS

- Odoo 19 port of the WhatsApp connector (systray, sale orders, invoices, portal and share URLs)

**Depends on** `sale`, `account`, `website`, `sale_management`

### Payment Gateways

#### `payment_alrajhi_arb` — Al Rajhi Bank (ARB) Payment Gateway

> version `19.0.1.4.12` · license `LGPL-3` · author: Sirelkhatim Gamal · category: Accounting/Payment Providers

Official-style ARB integration: token API, encrypted trandata, bank-hosted redirect, KSA Card/Mada checkout (Odoo 19).

- Al Rajhi Bank (ARB) payment acquirer for Saudi merchants
- Token API and AES-encrypted `trandata`
- Bank-hosted redirect flow with SAR, Card and Mada checkout
- Detailed setup notes in `static/description/index.html`

**Depends on** `payment`

#### `payment_applepay` — Hyperpay Payment Acquirer - Applepay

> version `19.0.1.0.0` · license `Other proprietary` · author: Technaureus Info Solutions Pvt. Ltd. · category: Accounting/Payment Providers

- Apple Pay acquirer button on top of the HyperPay (OPPWA) acquirer

**Depends on** `payment`, `website`

#### `payment_hyperpay` — Hyperpay Payment Acquirer

> version `19.0.1.0.1` · license `Other proprietary` · author: Webkul Software Pvt. Ltd. · category: Accounting/Payment Providers

Website Hyper Pay Payment Acquirer.

- HyperPay (OPPWA) payment gateway for website checkout

> **Note** — `payment_applepay` builds on this module.

**Depends on** `account`, `payment`, `website_sale`

### Printing, Reports & PDF

#### `advanced_accounting_reports` — Advanced Accounting Reports

> version `1.20.0` · license `LGPL-3` · author: Woledge · category: Accounting · `README`](odoo19/advanced_accounting_reports/README.md), tests, JS

Advanced General Ledger, Trial Balance with Analytic Dimensions & Multi-Currency.

- Analytic dimensions: features, cost centers and patch numbers
- Multi-currency: secondary currency, manual exchange rate per journal entry, automatic secondary amount
- General Ledger with dimensions and secondary currency
- Trial Balance with analytic dimensions and multi-currency
- README + unit tests


**Development batch 01 changes (Odoo 19):** export exceptions no longer expose traceback details to users; details are logged server-side; spreadsheet formula/link auto-conversion is disabled. **Critical pending issue:** the existing `pre_init_hook` has potentially destructive view/constraint operations and must be reviewed on a database clone before installation/upgrade.

**Depends on** `account`, `account_reports`, `base`, `web`

#### `direct_print_auto` — Direct Print Auto

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Sales/Sales · `README`](odoo19/direct_print_auto/README.md), tests, JS

- Auto-prints reports to the browser print dialog when a document is confirmed
- Fires on `account.move.action_post()`, `sale.order.action_confirm()` and delivery validation
- Manual *Direct Print* button on each supported form view
- Works with invoices, sale orders, delivery slips and purchase orders
- README + unit tests

**Depends on** `base`, `web`, `sale_management`, `account`, `stock`, `purchase`

#### `el_pdf_print_preview` — PDF Print Preview

> version `19.0.1.1.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Extra Tools/Usability · `README`](odoo19/el_pdf_print_preview/README.md), tests, JS

Preview PDF reports in-browser before printing — no download needed.

- Intercepts report actions and opens a PDF.js viewer dialog in the browser
- Preview, then print or download without leaving Odoo
- Per-user toggle for preview on/off and for automatic printing
- Friendly error dialog if the report fails to render
- README + unit tests

**Depends on** `base`, `web`

#### `ie_stock_movement_report` — Stock Movement Report

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Inventory/Reporting · `README`](odoo19/ie_stock_movement_report/README.md), tests

PDF stock movement report with opening balance and running valuation.

- PDF report of inventory movements per product over a selected period
- One page per product with opening balance (quantity and value) computed from all earlier movements
- Movement table with date, reference, partner, source, destination and IN / OUT / BALANCE split into qty, unit, unit price and total
- Running balance and valuation
- README + unit tests

**Depends on** `base`, `stock`, `stock_account`, `web`

#### `partner_balance_confirmation` — Balance Confirmation

> version `19.0.3.6.0` · license `LGPL-3` · author: Z.ai · category: Accounting · `README`](odoo19/partner_balance_confirmation/README.md)

Customer Balance Confirmation (Imdad / Namo templates).

- Arabic customer balance confirmation statement (مطابقة رصيد العميل)
- *Print Confirmation* button on the customer form, with Imdad or Namo templates
- Auto-fills the date, customer name, balance as of the confirmation date and employee name
- PDF output matching the Word template (same fonts, stamps and layout) plus a `.docx` export
- README

**Depends on** `base`, `mail`, `account`

#### `saudi_tax_invoice` — Saudi Tax Invoice

> version `1.0` · license `LGPL-3` · category: Accounting

Saudi-style tax invoice PDF with action button.

- Saudi-style (Arabic, RTL) tax invoice PDF available as a button on invoices
- Own A4 portrait paper format at 90 dpi
- Shows company logo, VAT number, commercial registration, customer name and customer VAT number
- Dedicated CSS in `static/src/css/saudi_invoice.css`

**Depends on** `account`

### Security & Access Control

#### `el_button_access_control` — Button Access Control

> version `19.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Tools/Security · `README`](odoo19/el_button_access_control/README.md), tests, JS

Control button visibility per user group — show/hide buttons in any view without editing XML.

- Show or hide buttons per user group in **any** view, without editing the original XML
- Whitelist mode (show only for these groups) and blacklist mode (hide from these groups)
- Works on form, list, kanban views or all of them
- Any model — no code change needed in the target module
- README + unit tests

**Depends on** `base`

### Tools & Utilities

#### `auto_project_stages` — Project Task Visit Forms

> version `1.0` · author: Elmasry · category: Project

Auto-create project stages (New, In Progress, Approval One/Two) and starter tasks on project creation.

- On project creation, automatically creates the stages `New`, `In Progress`, `Approval One`, `Approval Two`
- Seeds two starter tasks (*Site Visit*, *specification*) in the `New` stage

> **Note** — The manifest is named "Project Task Visit Forms" and mentions Site Visit / Company Visit tabs that do not exist in the code.

**Depends on** `project`

#### `transaction_tracker` — Transaction Tracker

> version `1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Tools · `README`](odoo19/transaction_tracker/README.md), JS

Track all user transactions across every Odoo module.

- Tracks every create, write and unlink performed by users across all installed models
- Per-model enable/disable for each operation
- Dashboard with pivot and graph views
- Configurable tracking settings per model
- README

**Depends on** `base`, `web`

### Manufacturing

#### `mrp_lock_lines` — MRP Lock Lines

> version `19.0.1.0.0` · license `LGPL-3` · author: Masry · category: Manufacturing/Manufacturing · `README`](odoo19/mrp_lock_lines/README.md)

Lock all component lines in Manufacturing Order except the last one.

- Locks every component line in a manufacturing order and keeps only the last line editable
- Prevents accidental changes to raw material quantities, lots and locations
- README

**Depends on** `mrp`, `stock`

### Investment & Finance Products

#### `vehicle_installment` — Vehicle Installment Management

> version `19.0.2.0.0` · license `LGPL-3` · author: Abdullah Al-Habbal · category: Fleet · `README`](odoo19/vehicle_installment/README.md)

Manage vehicle installments with automatic calculation.

- Links installments to `fleet` vehicles
- Rate percentage with automatic installment calculation, including fractional handling
- Monthly payment tracking and an approval workflow
- README

**Depends on** `base`, `mail`, `fleet`, `hr`, `hr_payroll`

### AI & Analytics

#### `ai_finance_suite` — AI Finance

> version `19.0.1.0.0` · license `LGPL-3` · author: Woledge Team · category: Accounting/Finance · `README`](odoo19/ai_finance_suite/README.md), JS

AI-Powered Finance Suite: Virtual CFO, OCR Engine & Smart Reconciliation for Odoo 19.

- Six AI tools bundled in one install: Virtual CFO, OCR Engine, Smart Reconciliation and more
- Covers the finance workflow from bill capture to CFO-level analysis
- Woledge Team product — README with the full feature list

**Depends on** `base`, `mail`, `account`

#### `test_AI_finance` — AI Finance V1

> version `1.8` · license `LGPL-3` · author: AI Finance Team · category: Accounting/Finance · `README`](odoo19/test_AI_finance/README.md), JS

AI Finance V1: OCR engine for vendor bills plus a Virtual CFO chatbot (superseded by ai_finance_suite).

- AI Finance V1: OCR engine for vendor bills (PDF and images) with confidence scoring, and a Virtual CFO chatbot
- Natural-language questions over sales, expenses and trends
- One-click bill review and creation
- README

> **Note** — Test / prototype module — superseded by `ai_finance_suite`.

**Depends on** `base`, `mail`, `account`

### Core / Base

#### `meno` — meno

> version `18.0` · author: meno

- Same database expiry bypass as `odoo17/meno`, targeting Odoo 19

> **Note** — **Not a business module.** Bypasses the Odoo subscription expiry — do not use in production or redistribute.

**Depends on** `base`, `base_setup`

## Odoo 20

### Point of Sale

#### `el_pos_customer_payment_method` — POS Customer Payment Method

> version `20.0.1.0.0` · license `LGPL-3` · author: Ibrahim Elmasry · category: Sales/Point of Sale · `README`](odoo20/el_pos_customer_payment_method/README.md), tests, JS

Restrict POS payment methods per customer, with POS-level defaults for customers without a specific list.

- Odoo 20 port — see `odoo18/el_pos_customer_payment_method`

**Depends on** `point_of_sale`

### Human Resources

#### `el_hr_attendance_sheet` — HR Attendance Sheet And Policies

> version `20.0.1.0.1` · license `LGPL-3` · author: Ibrahim Elmasry · category: Human Resources/Attendance · `README`](odoo20/el_hr_attendance_sheet/README.md), tests

Calculate overtime, lateness, absence from attendance and feed payslip.

- Odoo 20 port: payroll structure model, record rules, server action and migrations
- Updated attendance report and data files
- Same feature set as the Odoo 19 port — overtime, lateness, absence, public holidays, payslip feed
- README, docs/ and unit tests

**Depends on** `base`, `hr_attendance`, `hr`, `hr_payroll`, `hr_holidays`, `mail`, `calendar`


### Inventory & Warehouse

#### `el_inter_company_transfer` — Inter Company Internal Transfer

> version `20.0.1.0.1` · license `LGPL-3` · author: Ibrahim Elmasry · category: Inventory/Warehouse Management

Creates controlled stock-transfer requests between warehouses owned by different companies. The requesting company is the goods recipient; the source company owns the requested stock.

**Business workflow**
1. A user creates a request in the requesting company and selects its destination warehouse.
2. The user selects the source company and the warehouse holding the stock.
3. Product lines and positive quantities are entered; available quantity is computed from source-company stock quants.
4. The request remains Draft until a user authorized for the source company (or a stock manager) confirms it.
5. Confirmation creates an outgoing picking in the source company and an incoming picking in the requesting company, using the inter-company transit location, then records the confirmer and confirmation date.
6. The request tracks both stock pickings, status, chatter and activities.

**Technical components**
- `inter.company.transfer.request`: request header, sequence reference, requesting/source companies, warehouses, status, requester/confirmer, dates, notes and links to both pickings.
- `inter.company.transfer.request.line`: requested product, quantity and computed available quantity.
- `stock.warehouse` extension: context-controlled warehouse `name_search()` to select the source company's warehouse.
- Views and menus: request forms/lists and navigation menus.
- Security: `security/ir.access.csv` (Odoo 20 access model).
- Data: request sequence.
- Chatter/activity integration through `mail.thread` and `mail.activity.mixin`.

**Dependencies**: `base`, `stock`, `mail`, `portal`.

**Review notes**: this module uses `sudo()` for source-warehouse and stock-quant reads and may activate the shared inter-company transit location. Validate access boundaries, transit-location company behavior, picking validation/receipt lifecycle, partial deliveries, cancellation, insufficient stock and rollback behavior in a multi-company runtime test. The manifest describes the workflow as Draft → Confirmed → Done, while the model also includes Cancelled.

### Tools & Utilities

#### `el_dashboard_builder` — Dashboard Builder

> version `20.0.1.0.0` · license `LGPL-3` · author: Elmasry · category: Tools

Builds user-configurable dashboards with a drag-and-drop 12-column layout and configurable data widgets. The module README describes the target as Odoo 20 Enterprise; the manifest itself depends on `base`, `web`, `mail` and `base_setup` only, so Community/Enterprise compatibility must be confirmed against the actual runtime and all referenced assets.

**Business workflow**
1. A user creates a dashboard, configures its name, company, owner, visibility and layout.
2. The user opens the visual editor and adds widgets from the widget library.
3. Widgets are positioned/resized on a responsive grid and configured with models, fields, aggregations, domains, labels and display options.
4. Dashboards can be tagged, favorited, duplicated and shared with users/groups or through share links.
5. Users view the dashboard; widgets retrieve data through controller endpoints.
6. Dashboard configuration and reports can be exported to JSON, PDF or Excel where supported by the module implementation.

**Built-in widget families**
- KPI cards and grouped KPI cards.
- Bar, line, pie/donut charts.
- Data tables and pivot tables.
- Gauge and progress indicators.
- HTML/Markdown content, action buttons and calendar/schedule widgets.

**Technical components**
- Models: `dashboard.builder`, `dashboard.builder.item`, `dashboard.builder.widget`, `dashboard.builder.share`, `dashboard.builder.tag`.
- Wizard: widget/item configuration wizard.
- Controllers: dashboard view/edit, shared dashboard, widget data/configuration/reordering and export routes.
- Frontend: Owl/JavaScript widgets, GridStack-style drag-and-drop layout, Chart.js charts and SCSS styling.
- Data: default widgets, demo records and sequence.
- Security: dashboard groups, access rules and model ACLs.
- Reports: dashboard PDF templates and report model.
- Tests: `tests/test_dashboard_builder.py`.


**Development batch 01 changes (Odoo 20):** controller/widget/preview errors return generic user-facing messages and log technical details server-side. The earlier XML-template parse defects were also repaired in the delivered Odoo 20 module archive. Runtime install and browser tests remain pending.

**Dependencies**: `base`, `web`, `mail`, `base_setup`.

**Review notes**: the module has a broad custom data-query surface. Before production use, test model/field/domain allowlisting, read access under the current user's rights, company isolation, shared-link token expiry/revocation, HTML/CSS sanitization, export permissions and widget query limits. Static parsing does not validate the frontend compatibility layer or the actual Odoo 20 web client APIs. The module's earlier XML-template defects were repaired in the supplied development batch; runtime installation and browser tests remain required.

### Core / Base

#### `meno` — meno

> version `1.1` · author: meno

- Same database expiry bypass as `odoo17/meno`, targeting Odoo 20

> **Note** — **Not a business module.** Bypasses the Odoo subscription expiry — do not use in production or redistribute.


**Depends on** `base`, `base_setup`

## Enterprise dependencies

These addons require Odoo Enterprise modules in addition to Community.

| Module | Enterprise addons |
|---|---|
| `account_reports` | `odoo19/advanced_accounting_reports` |
| `hr_payroll` | `odoo19/WPS`, `odoo19/deduction_management`, `odoo19/el_hr_attendance_sheet`, `odoo19/el_payroll_wps`, `odoo19/loan_management`, `odoo19/rm_hr_attendance_sheet`, `odoo19/vehicle_installment`, `odoo20/el_hr_attendance_sheet` |
| `hr_work_entry_enterprise` | `odoo19/deduction_management` |
| `web_gantt` | `odoo19/el_construction_management` |

## Unresolved dependencies

These addons declare dependencies that were not found in this repository, in the Odoo Community addons or in the Enterprise tree scanned for this inventory — they require the missing addon before installation. The previously missing `el_nmo_sale_payment_gateway` is now included in this repository and is therefore not listed here.

| Missing addon | Required by |
|---|---|
| `nmo_sale_order_approval_workflow` | `odoo19/el_prevent_negative_stock` |
| `nmo_stock_user_restriction` | `odoo19/el_prevent_negative_stock` |
| `odoo_shipping_service_apps` | `odoo19/smsa_express_delivery_carrier` |

## Conventions

**Layout** — `<version>/<addon>/`, addon folder name equals the Python module name.

**Manifest** — `name`, `summary`, `version` (`<odoo>.0.x.y.z`), `license`, `author`, `depends`, `data`.

**Tests** — `tests/test_*.py` using `odoo.tests.common.TransactionCase`; enable with `--test-enable`.

**Commits** — `[ADD]` for a new addon, `[UPD]` for changes to an existing one.


## Technical Inventory — All 112 Modules
This appendix is generated from the delivered development-batch source archive. It records static declarations discoverable in manifests, Python AST and XML files. It is not a substitute for runtime behavior testing. A method/field not listed here may be dynamically provided, inherited, or defined through decorators/JavaScript/XML.

### ODOO17 / `ie_costem_lead_form` — ie_costem_lead_form

- **Manifest version:** `0.1`  
- **Summary:** Short (1 phrase/line) summary of the module's purpose  
- **Category / license / author:** `CRM` / `not declared` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `crm`, `sale_management`  
- **Source inventory:** 13 files; 8 Python, 4 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ProjectTask` extends `crm.lead` — `models/form_site_visit.py`; fields: `sales_eng:Char`, `company_reference:Char`, `date:Date`, `site_company_name:Char`, `site_project_name:Char`, `site_project_address:Char`, `contractor_name:Char`, `contractor_mobile:Char`, `contractor_email:Char`, `consultant_name:Char`, `consultant_email:Char`, `consultant_site_name:Char`, `consultant_site_mobile:Char`, `consultant_site_email:Char`, `supervisor_name:Char`, `supervisor_mobile:Char`, `supervisor_email:Char`, `fire_alarm_supplier:Char` …
  - `AssignmentUser` extends `crm.lead` — `models/assignment_user.py`; fields: `assignment_username:Many2many`
  - `CheckBoxFields` extends `crm.lead` — `models/check_box_fields.py`; fields: `GetSpecifications:Selection`, `GetProjectLocation:Selection`, `SiteVisit:Selection`, `GetConsultantName:Selection`, `GetSystemSupplierName:Selection`, `FollowUpTechnicalOffer:Selection`, `FollowUpConsultantApproval:Selection`, `FollowUpSystemSupplierApproval:Selection`, `FinancialOfferFollowUp:Selection`, `Specifications:Many2many`, `notes:Text`; methods: `action_sale_quotations_new()`
- **View architectures detected:** xpath: 4
- **ACL entries:** `access.crm.lead.specification.line.user` (group `base.group_user/1/1/1`), `access.crm.lead.specification.line.manager` (group `base.group_system/1/1/1`), `res.users access for sales` (group `sales_team.group_sale_salesman/1/1/1`)
- **Functional file groups:** Controllers: `controllers/controllers.py`, `controllers/__init__.py`; Security: `security/ir.model.access.csv`; Views: `views/check_box_fields_view.xml`, `views/assignment_user_view.xml`, `views/form_site_visit_view.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO17 / `ie_crm_lead_pdf` — CRM Lead Print

- **Manifest version:** `1.0`  
- **Summary:** Print Leads as PDF  
- **Category / license / author:** `CRM` / `not declared` / `Ibrahim Elmasry`  
- **Dependencies:** `crm`  
- **Source inventory:** 6 files; 2 Python, 4 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:** No model/class declarations detected by the static extractor; inspect source files for dynamic definitions.
- **Functional file groups:** Reports: `report/crm_lead_report.xml`, `report/crm_lead_templates.xml`; Views: `views/views.xml`, `views/templates.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO17 / `ie_print_document_linked_order` — IE Print Document Linked Order

- **Manifest version:** `0.1`  
- **Summary:** Show all product attachments directly from Quotation.  
- **Category / license / author:** `Sales` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `sale`  
- **Source inventory:** 5 files; 4 Python, 1 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; methods: `action_view_product_attachments()`
  - `IrAttachment` extends `ir.attachment` — `models/sale_order.py`; methods: `action_print_selected()`
- **View architectures detected:** xpath: 1
- **Functional file groups:** Views: `views/sale_order_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO17 / `meno` — meno

- **Manifest version:** `18.0`  
- **Summary:** Crack odoo v18  
- **Category / license / author:** `not declared` / `not declared` / `meno`  
- **Dependencies:** `base`, `base_setup`  
- **Source inventory:** 10 files; 6 Python, 3 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ir_module_module` extends `ir.module.module` — `models/models.py`; methods: `crack()`, `cracks()`, `button_immediate_upgrade()`
  - `IrConfigParameter` extends `ir.config_parameter` — `models/models.py`; methods: `cracks()`
- **ACL entries:** `crack.crack` (group `/1/0/0`)
- **Functional file groups:** Controllers: `controllers/controllers.py`, `controllers/__init__.py`; Security: `security/ir.model.access.csv`; Data: `data/cracks_test.xml`; Views: `views/views.xml`, `views/templates.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `account_invoice_fixed_discount` — Account Fixed Discount

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Allows to apply fixed amount discounts in invoices.  
- **Category / license / author:** `Accounting & Finance` / `AGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `account`  
- **Source inventory:** 26 files; 7 Python, 3 XML, 0 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestInvoiceFixedDiscount` — `tests/test_account_fixed_discount.py`; methods: `setUpClass()`, `test_01_discounts_fixed_single_unit()`, `test_02_discounts_fixed_multiple_units()`, `test_03_discount_fixed_no_tax()`, `test_03_discount_fixed_no_unit_prise()`, `test_04_base_line_set_to_none()` …
  - `AccountMoveLine` extends `account.move.line` — `models/account_move_line.py`; fields: `discount_fixed:Monetary`; methods: `_compute_totals()`, `_onchange_discount_fixed()`, `_onchange_discount()`, `_get_discount_from_fixed_discount()`
  - `AccountTax` extends `account.tax` — `models/account_tax.py`; methods: `_prepare_base_line_for_taxes_computation()`
- **View architectures detected:** xpath: 1
- **Functional file groups:** Security: `security/res_groups.xml`; Views: `views/account_move_view.xml`
- **Tests present:** `tests/test_account_fixed_discount.py`, `tests/__init__.py`

### ODOO18 / `archer_meta_lead_ads` — Meta Lead Ads

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Import Meta lead ads into CRM leads  
- **Category / license / author:** `Sales/CRM` / `LGPL-3` / `Archer Solutions`  
- **Dependencies:** `crm`, `mail`, `contacts`, `utm`  
- **Source inventory:** 25 files; 12 Python, 9 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ArcherMetaLeadAdsController` — `controllers/oauth.py`; methods: `meta_oauth_callback()`
  - `MetaSyncLog` (`_name = meta.sync.log`) — `models/meta_sync_log.py`; fields: `name:Char`, `company_id:Many2one`, `level:Selection`, `category:Char`, `message:Text`, `credential_id:Many2one`, `page_id:Many2one`, `form_id:Many2one`, `lead_id:Many2one`; methods: `log()` …
  - `MetaAppCredential` (`_name = meta.app.credential`) extends `mail.thread`, `mail.activity.mixin` — `models/meta_app_credential.py`; fields: `name:Char`, `company_id:Many2one`, `app_id:Char`, `app_secret:Char`, `user_access_token:Text`, `token_expiry_date:Datetime`, `state:Selection`, `redirect_uri:Char`, `page_ids:One2many`, `page_count:Integer`, `sync_issue_count:Integer`, `last_sync_date:Datetime`, `notes:Html`, `active:Boolean`; methods: `action_generate_token()`, `action_exchange_oauth_code()`, `action_test_connection()`, `action_fetch_pages()`, `action_view_pages()`, `action_view_sync_issues()` …
  - `ResConfigSettings` extends `res.config.settings` — `models/res_config_settings.py`; methods: `action_open_meta_lead_ads()`
  - `MetaLeadFieldMapping` (`_name = meta.lead.field.mapping`) — `models/meta_lead_field_mapping.py`; fields: `sequence:Integer`, `form_id:Many2one`, `company_id:Many2one`, `meta_field_key:Char`, `odoo_field_id:Many2one`, `odoo_field_name:Char`, `odoo_field_ttype:Selection`, `relation:Char`, `lookup_field:Char`, `transform:Selection`, `is_default:Boolean`, `active:Boolean`; methods: `_onchange_odoo_field_id()`
  - `MetaLeadForm` (`_name = meta.lead.form`) extends `mail.thread`, `mail.activity.mixin` — `models/meta_lead_form.py`; fields: `name:Char`, `company_id:Many2one`, `page_id:Many2one`, `form_id:Char`, `status:Char`, `locale:Char`, `created_time:Datetime`, `crm_team_id:Many2one`, `utm_source_id:Many2one`, `utm_medium_id:Many2one`, `fetch_frequency_minutes:Selection`, `mapping_ids:One2many`, `mapping_count:Integer`, `lead_count:Integer`, `last_fetch_date:Datetime`, `questions_json:Text`, `active:Boolean`; methods: `action_view_leads()`, `action_fetch_form_fields()`, `action_fetch_leads()` …
  - `CrmLead` extends `crm.lead` — `models/crm_lead.py`; fields: `x_meta_leadgen_id:Char`, `x_meta_platform:Selection`, `x_meta_page_id:Many2one`, `x_meta_form_id:Many2one`, `x_meta_campaign_name:Char`, `x_meta_ad_name:Char`, `x_meta_created_time:Datetime`
  - `MetaPage` (`_name = meta.page`) extends `mail.thread`, `mail.activity.mixin` — `models/meta_page.py`; fields: `name:Char`, `company_id:Many2one`, `credential_id:Many2one`, `page_id:Char`, `page_access_token:Text`, `category:Char`, `platform:Selection`, `instagram_account_id:Char`, `fan_count:Integer`, `is_active:Boolean`, `form_ids:One2many`, `form_count:Integer`, `lead_count:Integer`; methods: `action_view_forms()`, `action_view_leads()`, `action_fetch_forms()` …
- **HTTP routes:**
  - `/meta_lead_ads/oauth/callback` → `meta_oauth_callback()` in `controllers/oauth.py`
- **Menu declarations:** `Meta Lead Ads`, `Credentials`, `Pages`, `Forms`, `Sync Issues`
- **View architectures detected:** form: 4, list: 4, search: 4, xpath: 3
- **Record rules:** `Meta Credential multi company`, `Meta Page multi company`, `Meta Form multi company`, `Meta Field Mapping multi company`, `Meta Sync Log multi company`
- **ACL entries:** `meta.app.credential.user` (group `archer_meta_lead_ads.group_meta_lead_ads_user/1/0/0`), `meta.app.credential.manager` (group `archer_meta_lead_ads.group_meta_lead_ads_manager/1/1/1`), `meta.page.user` (group `archer_meta_lead_ads.group_meta_lead_ads_user/1/1/0`), `meta.page.manager` (group `archer_meta_lead_ads.group_meta_lead_ads_manager/1/1/1`), `meta.lead.form.user` (group `archer_meta_lead_ads.group_meta_lead_ads_user/1/1/0`), `meta.lead.form.manager` (group `archer_meta_lead_ads.group_meta_lead_ads_manager/1/1/1`), `meta.lead.field.mapping.user` (group `archer_meta_lead_ads.group_meta_lead_ads_user/1/1/1`), `meta.lead.field.mapping.manager` (group `archer_meta_lead_ads.group_meta_lead_ads_manager/1/1/1`), `meta.sync.log.user` (group `archer_meta_lead_ads.group_meta_lead_ads_user/1/0/0`), `meta.sync.log.manager` (group `archer_meta_lead_ads.group_meta_lead_ads_manager/1/0/0`)
- **Functional file groups:** Controllers: `controllers/__init__.py`, `controllers/oauth.py`; Security: `security/ir.model.access.csv`, `security/security.xml`; Data: `data/ir_cron_data.xml`; Views: `views/meta_app_credential_views.xml`, `views/meta_sync_log_views.xml`, `views/menus.xml`, `views/meta_page_views.xml`, `views/meta_lead_form_views.xml`, `views/crm_lead_views.xml`, `views/res_config_settings_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `bi_global_custom_fields` — All in one add custom fields -Global Custom Fields

- **Manifest version:** `18.0.0.5`  
- **Summary:** Add custom fields global custom field add dynamic fields custom dynamic fields all in one add new fields all in one custom add fields update view update custom fields update fields assign custom fields update global custom fields easy to add custom field  
- **Category / license / author:** `Extra Tools` / `OPL-1` / `BROWSEINFO`  
- **Dependencies:** `base`  
- **Source inventory:** 14 files; 7 Python, 5 XML, 1 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `IrModelSelectionFieldInherit` (`_name = ir.model.fields.selection.custom`) — `models/global_custom_fields.py`; fields: `fields_id:Many2one`, `custom_fields_id:Many2one`, `field:Many2one`, `value:Char`, `name:Char`
  - `IrModelsFieldsCustom` (`_name = ir.models.fields.custom`) — `models/global_custom_fields.py`; fields: `name:Char`, `field_description:Char`, `model_id:Many2one`, `ttype:Selection`, `help:Text`, `required:Boolean`, `readonly:Boolean`, `copied:Boolean`, `groups:Many2many`, `selection_ids:One2many`, `state:Char`, `relation:Char`, `relation_field:Char`, `model_field:Char`, `where_to_add:Selection`, `after_which_field:Many2one`, `domain:Text`, `domain_list:Char` …; methods: `change_field_vals()`, `change_tab_vals()`, `field_domain()`, `domain_fields()`, `default_get()`, `create_global_custome_field()` …
  - `View` extends `ir.ui.view` — `models/custom_fields.py`; methods: `_check_groups()`
  - `CustomFields` (`_name = custom.fields`) — `models/custom_fields.py`; fields: `name:Char`, `field_description:Char`, `model_id:Many2one`, `ttype:Selection`, `help:Text`, `required:Boolean`, `readonly:Boolean`, `copied:Boolean`, `groups:Many2many`, `on_delete:Selection`, `state:Char`, `selection_ids:One2many`, `relation:Char`, `relation_field:Char`, `where_to_add:Selection`, `after_which_field:Many2one`, `domain:Text`, `tab_list:Many2one` …; methods: `change_field_vals()`, `change_tab_vals()`, `field_domain()`, `update_field()`, `write_fields()`, `unlink()`, `create_global_custome_field()` …
  - `IrGlobalCustomTabs` (`_name = ir.global.tabs`) — `models/global_custom_tabs.py`; fields: `name:Char`, `field_description:Char`, `model_id:Many2one`, `groups:Many2many`, `tab_list:Many2one`, `where_to_add:Selection`, `view_id:Many2one`; methods: `default_get()`, `create_global_custome_tabs()`, `update_tab()`, `update_current_tab()`, `unlink()`
  - `IrModelTabs` (`_name = ir.model.tabs`) — `models/ir_model_tabs.py`; fields: `tab_string:Char`, `tab_name:Char`, `model_id:Many2one`, `position:Integer`, `view_id:Many2one`
  - `IrModelFieldInherit` extends `ir.model.fields` — `models/ir_model_tabs.py`; fields: `view_id:Many2one`
- **Menu declarations:** `Custom Fields`, `Custom Global Fields`, `Custom Global Tabs`
- **View architectures detected:** form: 4, list: 3, search: 3
- **ACL entries:** `access_custom_global_tabs` (group `bi_global_custom_fields.global_custom_fields_group/1/1/1`), `access_ir_model_tabs` (group `bi_global_custom_fields.global_custom_fields_group/1/1/1`), `access_custom_fields` (group `bi_global_custom_fields.global_custom_fields_group/1/1/1`), `access_ir_models_fields_custom` (group `bi_global_custom_fields.global_custom_fields_group/1/1/1`), `access_ir_model_fields_selection_custom` (group `bi_global_custom_fields.global_custom_fields_group/1/1/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`, `security/global_custom_fields_security.xml`; Views: `views/global_custom_fields_menu.xml`, `views/global_custom_tabs_view.xml`, `views/custom_fields_view.xml`, `views/global_custom_fields.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `bi_health_care_center_management` — Health Care Center Management

- **Manifest version:** `18.0.0.0`  
- **Summary:** Manage Health Care Center Management Operations  Industry  Management Services Custom Health Care Solution   
- **Category / license / author:** `not declared` / `OPL-1` / `BrowseInfo`  
- **Dependencies:** `base`, `mail`, `account`, `product`, `website`, `contacts`, `event`, `website_event_sale`, `stock`, `hr_attendance`, `purchase`  
- **Source inventory:** 182 files; 32 Python, 37 XML, 3 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `NurseReservationReportWizard` (`_name = nurse.reservation.report.wizard`) — `wizard/nurse_reservation_report_wizard.py`; fields: `trainer_id:Many2one`, `date_from:Datetime`, `date_to:Datetime`; methods: `action_print_report()`
  - `AdmissionRenewalWizard` (`_name = admission.renewal.wizard`) — `wizard/admission_renewal_wizard.py`; fields: `admission_id:Many2one`, `client_id:Many2one`, `nurse_specialty_id:Many2one`, `package_id:Many2one`, `package_line_id_domain:Many2many`, `package_line_ids:Many2one`, `trainer_id:Many2one`, `weekday_ids:Many2many`, `start_duration:Date`, `start_time:Float`, `end_time:Float`, `n_of_reservations:Integer`, `is_vip:Boolean`, `duration:Integer`, `end_duration:Date`, `driver_id:Many2one`, `city_distance:Many2one`; methods: `default_get()`, `action_confirm()`, `action_create_invoice()` …
  - `CreateInvoice` (`_name = create.invoice`) — `wizard/create_invoice.py`; methods: `action_create_invoice()`
  - `ReservationConflictWizard` (`_name = reservation.conflict.wizard`) — `wizard/reservation_conflict_wizard.py`; fields: `trainer_id:Many2one`, `conflict_message:Text`, `flag:Boolean`; methods: `confirm_reservation()`, `confirm_change_details()`, `cancel_reservation()`
  - `ReservationConflictWizard` (`_name = reservation.driver.conflict.wizard`) — `wizard/reservation_driver_conflict_wizard.py`; fields: `driver_id:Many2one`, `conflict_message:Text`, `flag:Boolean`; methods: `confirm_reservation()`, `confirm_change_details()`, `cancel_reservation()`
  - `ReservationChangeWizard` (`_name = reservation.change.wizard`) — `wizard/reservation_change_wizard.py`; fields: `reservation_id:Many2one`, `new_start_date:Datetime`, `new_end_date:Datetime`, `new_trainer_id:Many2one`; methods: `action_confirm()`
  - `DriverReservationChangeWizard` (`_name = reservation.driver.change.wizard`) — `wizard/driver_reservation_change_wizard.py`; fields: `reservation_id:Many2one`, `new_start_date:Datetime`, `new_end_date:Datetime`, `new_driver_id:Many2one`; methods: `action_confirm()`
  - `StudentRegistration` — `controllers/main.py`; methods: `remove()`, `registration_create()`, `inquiry_create()`, `registration()`, `inquiry()`, `confirm_registration()`, `book_ground_confirm()`, `check_book_availability()`, `book_ground()`, `get_sports()`
  - `EventPortal` — `controllers/main.py`; methods: `get_domain_my_event()`, `portal_my_events()`, `event_followup()`, `download_qweb_report()` …
  - `CityDistance` (`_name = city.distance`) — `models/city_distance.py`; fields: `name:Char`, `from_city:Selection`, `to_city:Selection`, `distance_km:Float`, `travel_time:Float`; methods: `_on_change_joker()`, `_compute_name()`
  - `Level` (`_name = level.level`) — `models/level.py`; fields: `name:Char`, `description:Text`
  - `HrEmployeeBaseInherit` extends `hr.employee.base` — `models/hr_employee_base.py`; methods: `_create_work_contacts()`
  - `CenterBooking` (`_name = center.booking`) — `models/center_booking.py`; fields: `name:Char`, `user_id:Many2one`, `student_id:Many2one`, `mobile:Char`, `email:Char`, `sport_id:Many2one`, `space_id:Many2one`, `start_date:Datetime`, `end_date:Datetime`, `state:Selection`, `is_paid:Boolean`, `duration:Float`, `sale_order:Boolean`, `desc:Text`; methods: `check_end_date()`, `create()`, `action_make_payment()`, `action_confirm()`, `action_view_sale_order()` …
  - `StudentAdmission` (`_name = student.admission`) — `models/student_admission.py`; fields: `weekday_ids:Many2many`, `day_one:Selection`, `day_two:Selection`, `name:Char`, `student_id:Many2one`, `mobile:Char`, `p_name:Char`, `parent_mobile:Char`, `p1_name:Char`, `parent1_mobile:Char`, `email:Char`, `is_disability:Boolean`, `disability_description:Text`, `sport_id:Many2one`, `level_id:Many2one`, `trainer_id:Many2one`, `trainer_id_domain:Many2many`, `driver_id:Many2one` …; methods: `create()`, `action_enroll()`, `action_make_student()`, `action_cancel()`, `action_cancel_cron()`, `action_new()`, `action_view_invoice()`, `action_create_reservation()`, `action_create_driver_reservation()`, `action_create_reservation_auto()`, `action_create_reservation_auto_multi()`, `action_view_reservations()` …
  - `AccountMoveInherit` extends `account.move` — `models/account_move.py`; fields: `student_admission_id:Many2one`
  - `StudentInquiry` (`_name = student.inquiry`) — `models/student_inquiry.py`; fields: `name:Char`, `first_name:Char`, `last_name:Char`, `mobile:Char`, `email:Char`, `level_id:Many2one`, `sport_id:Many2many`, `p_name:Char`, `parent_mobile:Char`, `duration:Float`, `query:Text`, `state:Selection`, `is_admission:Boolean`, `check_parent:Boolean`; methods: `remove()`, `create()`, `action_admission()`, `action_cancel()`, `action_open_admission()`, `action_send_ans()` …
  - `Event` extends `event.event` — `models/event.py`; fields: `sport_id:Many2one`, `center_id:Many2one`, `ground_id:Many2one`
  - `CenterCertificate` (`_name = center.certificate`) — `models/center_certificate.py`; fields: `name:Char`, `user_name:Char`, `title:Char`, `user_id:Many2one`, `user_type:Selection`, `description:Text`, `date:Date`, `content:Html`; methods: `create()`
  - `StudentReservation` (`_name = student.reservation`) — `models/student_reservation.py`; fields: `name:Char`, `ref:Char`, `student_id:Many2one`, `sport_id:Many2one`, `level_id:Many2one`, `trainer_id:Many2one`, `state:Selection`, `is_finished:Boolean`, `check_register:Boolean`, `start_date:Datetime`, `end_date:Datetime`, `day_name:Char`, `color:Integer`, `admission_id:Many2one`, `is_vip:Boolean`, `c_level_id:Many2one`, `package_id:Many2one`, `package_line_id:Many2one` …; methods: `action_finish()`, `update_reservation_states()`, `action_change_details()`, `unlink()`, `create()` …
  - `Weekday` (`_name = weekday`) — `models/weekday.py`; fields: `name:Char`
  - `Package` (`_name = package.package`) — `models/package.py`; fields: `name:Char`, `description:Text`, `line_ids:One2many`
  - `PackageLine` (`_name = package.package.line`) — `models/package.py`; fields: `name:Char`, `package_id:Many2one`, `n_of_session:Integer`, `n_of_hours_peer_session:Integer`, `is_with_friday:Boolean`, `price:Float`, `product_id:Many2one`; methods: `check_invalid_session_numbers()`, `check_invalid_price()` …
  - `ResPartner` extends `res.partner` — `models/res_partner.py`; fields: `is_student:Boolean`, `is_coach:Boolean`, `is_driver:Boolean`, `p_name:Char`, `short_name:Char`, `is_disability:Boolean`, `disability_description:Text`, `trainer_id:Many2one`, `is_sport:Boolean`, `sport_id:Many2many`, `admission_id:Many2one`, `admission_end_date:Date`, `is_admission_finished:Boolean`, `birth_date:Date`, `level_id:Many2one`, `reservation_ids:One2many`, `n_of_reservations:Integer`, `n_of_reservations_unfinished:Integer` …; methods: `create()`, `get_data()`, `default_get()`, `update_student_admission_state()` …
  - `NurseSpecialty` (`_name = nurse.specialty`) — `models/nurse_specialty.py`; fields: `name:Char`, `description:Text`, `nurse_ids:One2many`
  - `ProductTemplate` extends `product.template` — `models/product.py`; fields: `is_equipment:Boolean`, `is_space:Boolean`, `is_sportname:Boolean`, `sport_id:Many2many`
  - `ProductProduct` extends `product.product` — `models/product.py`; fields: `is_equipment:Boolean`, `is_space:Boolean`, `is_sportname:Boolean`, `sport_id:Many2many`
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; fields: `booking_id:Many2one`
  - `SportCenter` (`_name = sport.center`) — `models/sport_center.py`; fields: `name:Char`
  - `SportName` (`_name = sport.name`) — `models/sport_center.py`; fields: `name:Char`
  - `DriverReservation` (`_name = driver.reservation`) — `models/driver_reservation.py`; fields: `name:Char`, `ref:Char`, `student_id:Many2one`, `sport_id:Many2one`, `level_id:Many2one`, `trainer_id:Many2one`, `driver_id:Many2one`, `city_distance_id:Many2one`, `state:Selection`, `is_finished:Boolean`, `check_register:Boolean`, `start_date:Datetime`, `end_date:Datetime`, `day_name:Char`, `color:Integer`, `admission_id:Many2one`, `is_vip:Boolean`, `c_level_id:Many2one` …; methods: `action_finish()`, `update_driver_reservation_states()`, `action_change_details()`, `unlink()`, `create()` …
  - `StudentCertificate` (`_name = student.certificate`) — `models/student_certificate.py`; fields: `name:Char`, `appraisal:Char`, `description:Text`
- **HTTP routes:**
  - `/registration/create` → `registration_create()` in `controllers/main.py`
  - `/inquiry/create` → `inquiry_create()` in `controllers/main.py`
  - `/registration/` → `registration()` in `controllers/main.py`
  - `/inquiry/` → `inquiry()` in `controllers/main.py`
  - `/confirm/<int:id>/registration` → `confirm_registration()` in `controllers/main.py`
  - `/book_ground/confirm` → `book_ground_confirm()` in `controllers/main.py`
  - `/check_book/availability` → `check_book_availability()` in `controllers/main.py`
  - `/book_ground/` → `book_ground()` in `controllers/main.py`
  - `/get_sports` → `get_sports()` in `controllers/main.py`
  - `/my/events` → `portal_my_events()` in `controllers/main.py`
  - `/my/events/page/<int:page>` → `portal_my_events()` in `controllers/main.py`
  - `/event/<int:event_id>` → `event_followup()` in `controllers/main.py`
  - `/event/<int:event_id>/<access_token>` → `event_followup()` in `controllers/main.py`
  - `/my/event/<int:event_id>` → `event_followup()` in `controllers/main.py`
  - `/my/event/<int:event_id>/<access_token>` → `event_followup()` in `controllers/main.py`
  - `/event/ticket/report/<int:event_id>` → `download_qweb_report()` in `controllers/main.py`
- **Menu declarations:** `Nurse Reservations`, `Health Care Management Center`, `Admission`, `Registrations`, `Admission`, `Clients`, `Driver Reservations`, `Packages`, `Cases`, `Events`, `Certificates`, `Reports`, `Nurse Reservation Report`, `City Distance`, `Configuration`, `Branches`, `Nurses`, `Drivers`, `Equipments`, `Dashboard`
- **View architectures detected:** calendar: 2, form: 19, list: 11, search: 3, xpath: 7
- **ACL entries:** `access_sport_center` (group `base.group_user/1/1/1`), `access_student_admission` (group `base.group_user/1/1/1`), `access_student_reservation` (group `base.group_user/1/1/1`), `access_driver_reservation` (group `base.group_user/1/1/1`), `access_reservation_conflict_wizard` (group `base.group_user/1/1/1`), `access_reservation_driver_conflict_wizard` (group `base.group_user/1/1/1`), `access_reservation_change_wizard` (group `base.group_user/1/1/1`), `access_reservation_driver_change_wizard` (group `base.group_user/1/1/1`), `access_create_invoice` (group `base.group_user/1/1/1`), `access_student_certificate` (group `base.group_user/1/1/1`), `access_student_inquiry` (group `base.group_user/1/1/1`), `event.registration.portal` (group `base.group_portal/1/1/0`), `access_center_booking` (group `base.group_user/1/1/1`), `access_center_certificate` (group `base.group_user/1/1/1`), `access_sport_name` (group `base.group_user/1/1/1`), `access_level_level` (group `base.group_user/1/1/1`), `access_package_package` (group `base.group_user/1/1/1`), `access_package_package_line` (group `base.group_user/1/1/1`), `access_weekday` (group `/1/0/0`), `access_city_distance` (group `/1/1/1`) …
- **Functional file groups:** Wizards: `wizard/nurse_reservation_report_wizard.py`, `wizard/admission_renewal_wizard.py`, `wizard/nurse_reservation_report_wizard.xml`, `wizard/create_invoice.py`, `wizard/reservation_conflict_wizard.py`, `wizard/__init__.py`, `wizard/reservation_driver_conflict_wizard.py`, `wizard/reservation_conflict_wizard_view.xml` …; Reports: `report/center_certificate_report.xml`, `report/student_reservation_report_action.xml`; Controllers: `controllers/main.py`, `controllers/__init__.py`; Security: `security/ir.model.access.csv`; Data: `data/web_menu.xml`, `data/admission_enroll_email.xml`, `data/admission_data.xml`, `data/center_sport_dashboard_views.xml`, `data/weekdays.xml`, `data/student_inquiry_mail.xml`, `data/driver_reservation_cron.xml`, `data/student_reservation_cron.xml` …; Views: `views/student_reservation_views.xml`, `views/res_partner_views.xml`, `views/purchase_views.xml`, `views/student_admission_views.xml`, `views/driver_reservation_views.xml`, `views/package_views.xml`, `views/student_inquiry_views.xml`, `views/nurse_specialty_views.xml` …
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `bi_so_product_quantity_limit` — Sale Order Product Quantity Limit

- **Manifest version:** `18.0.0.0`  
- **Summary:** sale product quantity limit sales product limit sales order product maximum quantity limit product minimum quantity restrict product quantity limit sales order minimum product quantity max product quantity limit min product quantity limit  
- **Category / license / author:** `Sales` / `OPL-1` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `sale`, `sale_management`  
- **Source inventory:** 10 files; 5 Python, 1 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ProductTemplate` extends `product.template` — `models/product_template.py`; fields: `min_qty:Float`, `max_qty:Float`; methods: `qty_validate()`
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; methods: `create()`, `action_confirm()`
  - `SaleOrderLine` extends `sale.order.line` — `models/sale_order.py`; methods: `onchange_product_uom_qty()`
- **View architectures detected:** xpath: 1
- **Functional file groups:** Views: `views/product_template_view.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `bi_sport_center_management` — Sport Center Management

- **Manifest version:** `18.0.0.0`  
- **Summary:** Manage Sport Club Fitness Center Management Sports Operations Sports Industry Sports Club Activities Sports Management Services Custom Sports Solution Sports Management Agency Student Sport Registrations Sports Inquiry Sports Trainers Booking Sports Center  
- **Category / license / author:** `not declared` / `OPL-1` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `mail`, `account`, `product`, `website`, `contacts`, `event`, `website_event_sale`, `stock`, `purchase`  
- **Source inventory:** 60 files; 24 Python, 28 XML, 3 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `AdmissionRenewalWizard` (`_name = admission.renewal.wizard`) — `wizard/admission_renewal_wizard.py`; fields: `admission_id:Many2one`, `weekday_ids:Many2many`, `name:Char`, `student_id:Many2one`, `sport_id:Many2one`, `level_id:Many2one`, `trainer_id:Many2one`, `start_date:Float`, `end_date:Float`, `start_duration:Date`, `old_start_duration:Date`, `end_duration:Date`, `duration:Integer`, `n_of_reservations:Integer`, `is_vip:Boolean`, `c_level_id:Many2one`; methods: `action_confirm()`, `action_create_invoice()` …
  - `CreateInvoice` (`_name = create.invoice`) — `wizard/create_invoice.py`; methods: `action_create_invoice()`
  - `ReservationConflictWizard` (`_name = reservation.conflict.wizard`) — `wizard/reservation_conflict_wizard.py`; fields: `trainer_id:Many2one`, `conflict_message:Text`, `flag:Boolean`; methods: `confirm_reservation()`, `confirm_change_details()`, `cancel_reservation()`
  - `ReservationChangeWizard` (`_name = reservation.change.wizard`) — `wizard/reservation_change_wizard.py`; fields: `reservation_id:Many2one`, `new_start_date:Datetime`, `new_end_date:Datetime`, `new_trainer_id:Many2one`; methods: `action_confirm()`
  - `StudentRegistration` — `controllers/main.py`; methods: `remove()`, `registration_create()`, `inquiry_create()`, `registration()`, `inquiry()`, `confirm_registration()`, `book_ground_confirm()`, `check_book_availability()`, `book_ground()`, `get_sports()`
  - `EventPortal` — `controllers/main.py`; methods: `get_domain_my_event()`, `portal_my_events()`, `event_followup()`, `download_qweb_report()` …
  - `Level` (`_name = level.level`) — `models/level.py`; fields: `name:Char`, `distribution:Text`
  - `CenterBooking` (`_name = center.booking`) — `models/center_booking.py`; fields: `name:Char`, `user_id:Many2one`, `student_id:Many2one`, `mobile:Char`, `email:Char`, `sport_id:Many2one`, `space_id:Many2one`, `start_date:Datetime`, `end_date:Datetime`, `state:Selection`, `is_paid:Boolean`, `duration:Float`, `sale_order:Boolean`, `desc:Text`; methods: `check_end_date()`, `create()`, `action_make_payment()`, `action_confirm()`, `action_view_sale_order()` …
  - `StudentAdmission` (`_name = student.admission`) — `models/student_admission.py`; fields: `weekday_ids:Many2many`, `day_one:Selection`, `day_two:Selection`, `name:Char`, `student_id:Many2one`, `mobile:Char`, `p_name:Char`, `parent_mobile:Char`, `p1_name:Char`, `parent1_mobile:Char`, `email:Char`, `is_disability:Boolean`, `disability_description:Text`, `sport_id:Many2one`, `level_id:Many2one`, `trainer_id:Many2one`, `state:Selection`, `is_invoiced:Boolean` …; methods: `create()`, `action_enroll()`, `action_make_student()`, `action_create_invoice()`, `action_cancel()`, `action_cancel_cron()`, `action_new()`, `action_view_invoice()`, `action_create_reservation()`, `action_create_reservation_auto_multi()`, `action_view_reservations()`, `action_open_renewal_wizard()` …
  - `AccountMoveInherit` extends `account.move` — `models/account_move.py`; fields: `student_admission_id:Many2one`, `admission_n_of_reservations:Integer`, `admission_weekday_ids:Many2many`, `admission_start_date:Float`, `admission_end_date:Float`, `admission_start_duration:Date`, `admission_end_duration:Date`
  - `StudentInquiry` (`_name = student.inquiry`) — `models/student_inquiry.py`; fields: `name:Char`, `first_name:Char`, `last_name:Char`, `mobile:Char`, `email:Char`, `level_id:Many2one`, `sport_id:Many2many`, `p_name:Char`, `parent_mobile:Char`, `duration:Float`, `query:Text`, `state:Selection`, `is_admission:Boolean`, `check_parent:Boolean`; methods: `remove()`, `create()`, `action_admission()`, `action_cancel()`, `action_open_admission()`, `action_send_ans()` …
  - `Event` extends `event.event` — `models/event.py`; fields: `sport_id:Many2one`, `center_id:Many2one`, `ground_id:Many2one`
  - `CenterCertificate` (`_name = center.certificate`) — `models/center_certificate.py`; fields: `name:Char`, `user_name:Char`, `title:Char`, `user_id:Many2one`, `user_type:Selection`, `description:Text`, `date:Date`, `content:Html`; methods: `create()`
  - `StudentReservation` (`_name = student.reservation`) — `models/student_reservation.py`; fields: `name:Char`, `ref:Char`, `student_id:Many2one`, `sport_id:Many2one`, `level_id:Many2one`, `trainer_id:Many2one`, `state:Selection`, `is_finished:Boolean`, `check_register:Boolean`, `start_date:Datetime`, `end_date:Datetime`, `day_name:Char`, `color:Integer`, `admission_id:Many2one`, `is_vip:Boolean`, `c_level_id:Many2one`, `student_age:Integer`, `student_mobile:Char` …; methods: `action_finish()`, `update_reservation_states()`, `action_change_details()`, `unlink()`, `create()` …
  - `Weekday` (`_name = weekday`) — `models/weekday.py`; fields: `name:Char`
  - `ResPartner` extends `res.partner` — `models/res_partner.py`; fields: `is_student:Boolean`, `is_coach:Boolean`, `p_name:Char`, `short_name:Char`, `is_disability:Boolean`, `disability_description:Text`, `trainer_id:Many2one`, `is_sport:Boolean`, `sport_id:Many2many`, `admission_id:Many2one`, `admission_end_date:Date`, `is_admission_finished:Boolean`, `birth_date:Date`, `level_id:Many2one`, `reservation_ids:One2many`, `n_of_reservations:Integer`, `n_of_reservations_unfinished:Integer`, `is_warning:Boolean`; methods: `get_data()`, `default_get()`, `update_student_admission_state()` …
  - `ProductTemplate` extends `product.template` — `models/product.py`; fields: `is_equipment:Boolean`, `is_space:Boolean`, `is_sportname:Boolean`, `sport_id:Many2many`
  - `ProductProduct` extends `product.product` — `models/product.py`; fields: `is_equipment:Boolean`, `is_space:Boolean`, `is_sportname:Boolean`, `sport_id:Many2many`
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; fields: `booking_id:Many2one`
  - `SportCenter` (`_name = sport.center`) — `models/sport_center.py`; fields: `name:Char`
  - `SportName` (`_name = sport.name`) — `models/sport_center.py`; fields: `name:Char`
  - `StudentCertificate` (`_name = student.certificate`) — `models/student_certificate.py`; fields: `name:Char`, `appraisal:Char`, `description:Text`
- **HTTP routes:**
  - `/registration/create` → `registration_create()` in `controllers/main.py`
  - `/inquiry/create` → `inquiry_create()` in `controllers/main.py`
  - `/registration/` → `registration()` in `controllers/main.py`
  - `/inquiry/` → `inquiry()` in `controllers/main.py`
  - `/confirm/<int:id>/registration` → `confirm_registration()` in `controllers/main.py`
  - `/book_ground/confirm` → `book_ground_confirm()` in `controllers/main.py`
  - `/check_book/availability` → `check_book_availability()` in `controllers/main.py`
  - `/book_ground/` → `book_ground()` in `controllers/main.py`
  - `/get_sports` → `get_sports()` in `controllers/main.py`
  - `/my/events` → `portal_my_events()` in `controllers/main.py`
  - `/my/events/page/<int:page>` → `portal_my_events()` in `controllers/main.py`
  - `/event/<int:event_id>` → `event_followup()` in `controllers/main.py`
  - `/event/<int:event_id>/<access_token>` → `event_followup()` in `controllers/main.py`
  - `/my/event/<int:event_id>` → `event_followup()` in `controllers/main.py`
  - `/my/event/<int:event_id>/<access_token>` → `event_followup()` in `controllers/main.py`
  - `/event/ticket/report/<int:event_id>` → `download_qweb_report()` in `controllers/main.py`
- **Menu declarations:** `Reservations`, `Sports Management Center`, `Admission`, `Registrations`, `Admission`, `Trainees`, `Sports`, `Coach`, `Sports Equipments`, `Events`, `Certificates`, `Levels`, `Booking`, `Configuration`, `Sports name`, `Sports Center`, `Ground / Court`, `Dashboard`
- **View architectures detected:** calendar: 1, form: 11, list: 7, search: 2, xpath: 6
- **ACL entries:** `access_sport_center` (group `base.group_user/1/1/1`), `access_student_admission` (group `base.group_user/1/1/1`), `access_student_reservation` (group `base.group_user/1/1/1`), `access_reservation_conflict_wizard` (group `base.group_user/1/1/1`), `access_reservation_change_wizard` (group `base.group_user/1/1/1`), `access_admission_renewal_wizard` (group `base.group_user/1/1/1`), `access_create_invoice` (group `base.group_user/1/1/1`), `access_student_certificate` (group `base.group_user/1/1/1`), `access_student_inquiry` (group `base.group_user/1/1/1`), `event.registration.portal` (group `base.group_portal/1/1/0`), `access_center_booking` (group `base.group_user/1/1/1`), `access_center_certificate` (group `base.group_user/1/1/1`), `access_sport_name` (group `base.group_user/1/1/1`), `access_level_level` (group `base.group_user/1/1/1`), `access_weekday` (group `/1/0/0`)
- **Functional file groups:** Wizards: `wizard/admission_renewal_wizard.py`, `wizard/create_invoice.py`, `wizard/reservation_conflict_wizard.py`, `wizard/__init__.py`, `wizard/reservation_conflict_wizard_view.xml`, `wizard/reservation_change_wizard_view.xml`, `wizard/reservation_change_wizard.py`, `wizard/create_invoice_views.xml` …; Reports: `report/center_certificate_report.xml`, `report/account_move_reports.xml`; Controllers: `controllers/main.py`, `controllers/__init__.py`; Security: `security/ir.model.access.csv`; Data: `data/web_menu.xml`, `data/admission_enroll_email.xml`, `data/admission_data.xml`, `data/center_sport_dashboard_views.xml`, `data/weekdays.xml`, `data/student_inquiry_mail.xml`, `data/student_reservation_cron.xml`, `data/booking_mail_template.xml`; Views: `views/student_reservation_views.xml`, `views/res_partner_views.xml`, `views/purchase_views.xml`, `views/student_admission_views.xml`, `views/student_inquiry_views.xml`, `views/event_views.xml`, `views/center_certificate_views.xml`, `views/level_views.xml` …
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `delivery_return_reason` — Delivery Return Reasons

- **Manifest version:** `18.0.1.0.1`  
- **Summary:** تتبع أسباب رجوع الطلبات مع إحصائيات وتحليلات  
- **Category / license / author:** `Inventory/Delivery` / `LGPL-3` / `Your Company`  
- **Dependencies:** `stock`, `el_kitchen_receipt`  
- **Source inventory:** 13 files; 6 Python, 6 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `DeliveryReturnReason` (`_name = delivery.return.reason`) — `models/delivery_return_reason.py`; fields: `name:Char`, `sequence:Integer`, `active:Boolean`, `company_id:Many2one`
  - `StockPicking` extends `stock.picking` — `models/stock_picking.py`; fields: `x_returned:Boolean`, `x_return_reason_id:Many2one`, `x_return_note:Text`; methods: `create()`
  - `StockReturnPicking` extends `stock.return.picking` — `models/stock_picking_return.py`; fields: `x_return_reason_id:Many2one`, `x_return_note:Text`; methods: `_prepare_picking_default_values()`
- **Menu declarations:** `أسباب الرجوع`, `إدارة الأسباب`, `تحليل المرتجعات`
- **View architectures detected:** field: 1, form: 1, graph: 1, list: 1, pivot: 1, search: 1, xpath: 2
- **ACL entries:** `delivery.return.reason` (group `base.group_user/1/1/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`; Data: `data/delivery_return_reason_data.xml`; Views: `views/delivery_return_reason_views.xml`, `views/stock_picking_search.xml`, `views/stock_picking_views.xml`, `views/stock_picking_analysis.xml`, `views/stock_picking_return_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `el_barcode_price_display` — Barcode Price Display

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Standalone barcode scanner price display page — no login needed  
- **Category / license / author:** `Inventory/Inventory` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `product`  
- **Source inventory:** 17 files; 6 Python, 2 XML, 1 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestBarcodePriceDisplay` — `tests/test_price_display.py`; methods: `setUpClass()`, `test_01_page_loads()`, `test_02_product_found()`, `test_03_product_not_found()`, `test_04_short_barcode_rejected()`, `test_05_placeholder_for_no_image()`, `test_06_placeholder_color_deterministic()`, `test_07_product_with_image()`, `test_08_empty_barcode()`, `test_09_no_barcode_param()`, `test_10_groups_exist()`
  - `BarcodePriceDisplay` — `controllers/main.py`; methods: `price_display_page()`, `price_display_search()`
- **HTTP routes:**
  - `/price-display` → `price_display_page()` in `controllers/main.py`
  - `/price-display/search` → `price_display_search()` in `controllers/main.py`
- **ACL entries:** `barcode.price.user` (group `group_barcode_price_user/1/0/0`)
- **Functional file groups:** Controllers: `controllers/main.py`, `controllers/__init__.py`; Security: `security/ir.model.access.csv`, `security/groups.xml`; Views: `views/templates.xml`
- **Tests present:** `tests/test_price_display.py`, `tests/__init__.py`

### ODOO18 / `el_kitchen_receipt` — Kitchen Receipt from Quotation

- **Manifest version:** `18.0.4.1.0`  
- **Summary:** Print kitchen receipt from sales quotation with customer delivery info auto-fill + pilot name sync with delivery  
- **Category / license / author:** `Sales/Sales` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `sale`, `sale_stock`, `account`, `stock`  
- **Source inventory:** 41 files; 11 Python, 10 XML, 0 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestKitchenReceipt` — `tests/test_kitchen_receipt.py`; methods: `setUpClass()`, `test_01_partner_delivery_fields_exist()`, `test_02_sale_order_delivery_fields_exist()`, `test_03_onchange_partner_fills_fields()`, `test_04_sync_delivery_to_partner()`, `test_05_driver_name_passed_to_invoice()`, `test_06_wizard_print_report()`, `test_06b_wizard_print_all()`, `test_07_stock_picking_driver_field()`, `test_08_account_move_driver_field()`, `test_09_kitchen_receipt_report_exists()`, `test_10_pilot_report_exists()` …
  - `AccountMove` extends `account.move` — `models/account_move.py`; fields: `x_driver_name:Many2one`; methods: `write()` …
  - `XPilot` (`_name = x.pilot`) — `models/x_pilot.py`; fields: `name:Char`
  - `PilotReportWizard` (`_name = pilot.report.wizard`) — `models/pilot_report_wizard.py`; fields: `x_driver_name:Many2many`, `date_from:Date`, `date_to:Date`, `sale_order_id:Many2one`; methods: `action_print_report()` …
  - `ResPartner` extends `res.partner` — `models/res_partner.py`; fields: `x_building_floor:Char`, `x_landmark:Char`, `x_driver_name:Many2one`
  - `StockPicking` extends `stock.picking` — `models/stock_picking.py`; fields: `x_driver_name:Many2one`; methods: `create()`, `write()` …
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; fields: `x_building_floor:Char`, `x_landmark:Char`, `x_driver_name:Many2one`; methods: `create()`, `write()` …
- **Menu declarations:** `الطيارين`, `تقرير الطيار`
- **View architectures detected:** form: 2, list: 1, search: 1, xpath: 8
- **ACL entries:** `access.x.pilot.user` (group `sales_team.group_sale_salesman/1/1/1`), `access.x.pilot.manager` (group `sales_team.group_sale_manager/1/1/1`), `access.pilot.report.wizard.user` (group `sales_team.group_sale_salesman/1/0/1`), `access.pilot.report.wizard.manager` (group `sales_team.group_sale_manager/1/0/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`; Views: `views/res_partner_views.xml`, `views/pilot_report_wizard.xml`, `views/sale_order_views.xml`, `views/stock_picking_views.xml`, `views/x_pilot_views.xml`, `views/pilot_report_buttons.xml`, `views/sale_order_search.xml`, `views/account_move_views.xml`
- **Tests present:** `tests/__init__.py`, `tests/test_kitchen_receipt.py`

### ODOO18 / `el_mobile_webhook` — Mobile Webhook

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Reliable outbound status webhooks for mobile backends  
- **Category / license / author:** `Technical` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base_setup`, `sale`, `stock`, `account`  
- **Source inventory:** 29 files; 11 Python, 4 XML, 0 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestMobileWebhook` — `tests/test_webhook.py`; methods: `test_queue_payload_has_unique_event_id()`, `test_failed_delivery_is_retried()`
  - `MobileWebhookEvent` (`_name = mobile.webhook.event`) — `models/webhook_event.py`; fields: `event_uuid:Char`, `event_type:Char`, `res_model:Char`, `res_id:Integer`, `record_name:Char`, `company_id:Many2one`, `previous_status:Char`, `status:Char`, `payload_json:Text`, `state:Selection`, `attempts:Integer`, `next_attempt_at:Datetime`, `sent_at:Datetime`, `last_error:Char`; methods: `action_retry()`, `action_cancel()`, `action_send_now()` …
  - `AccountMove` extends `account.move` — `models/account_move.py`; methods: `write()`
  - `ResConfigSettings` extends `res.config.settings` — `models/res_config_settings.py`; fields: `mobile_webhook_endpoint:Char`, `mobile_webhook_secret:Char`, `mobile_webhook_timeout:Integer`, `mobile_webhook_retry_limit:Integer`; methods: `_check_mobile_webhook_settings()`
  - `StockPicking` extends `stock.picking` — `models/stock_picking.py`; methods: `write()`
  - `AccountPayment` extends `account.payment` — `models/account_payment.py`; methods: `write()`
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; methods: `write()`
- **Menu declarations:** `Mobile Webhook`, `Events`
- **View architectures detected:** form: 1, list: 1, search: 1, xpath: 1
- **Record rules:** `Mobile webhook event multi-company`
- **ACL entries:** `mobile.webhook.event.manager` (group `base.group_system/1/1/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`, `security/security.xml`; Data: `data/ir_cron.xml`; Views: `views/mobile_webhook_event_views.xml`, `views/res_config_settings_views.xml`
- **Tests present:** `tests/__init__.py`, `tests/test_webhook.py`

### ODOO18 / `el_pos_customer_payment_method` — POS Customer Payment Method

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Restrict POS payment methods per customer, with POS-level defaults for customers without a specific list.  
- **Category / license / author:** `Sales/Point of Sale` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `point_of_sale`  
- **Source inventory:** 13 files; 8 Python, 2 XML, 1 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestElPosPaymentMethodFilter` — `tests/test_payment_filter.py`; methods: `setUpClass()`, `test_01_partner_field_stored()`, `test_02_pos_data_fields_include_allowed_methods()`, `test_03_child_partner_resolves_to_commercial_partner()`, `test_04_partner_data_read_returns_method_ids()`, `test_05_pos_config_defaults_field_loaded()`, `test_06_settings_related_field_roundtrip()`
  - `ResPartner` extends `res.partner` — `models/res_partner.py`; fields: `el_allowed_pos_payment_method_ids:Many2many`; methods: `_load_pos_data_fields()`
  - `ResConfigSettings` extends `res.config.settings` — `models/res_config_settings.py`; fields: `pos_el_default_payment_method_ids:Many2many`
  - `PosConfig` extends `pos.config` — `models/pos_config.py`; fields: `el_pos_default_payment_method_ids:Many2many`
- **View architectures detected:** xpath: 2
- **Functional file groups:** Views: `views/res_partner_views.xml`, `views/res_config_settings_views.xml`
- **Tests present:** `tests/__init__.py`, `tests/test_payment_filter.py`

### ODOO18 / `el_product_traceability_dashboard` — Product Traceability Dashboard

- **Manifest version:** `18.0.2.0.0`  
- **Summary:** Product traceability dashboard with returns, scrap and manufacturing genealogy  
- **Category / license / author:** `Inventory/Inventory` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `stock`, `purchase`, `sale_management`, `mrp`, `account`  
- **Source inventory:** 16 files; 6 Python, 6 XML, 1 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `TraceabilityMovementReport` (`_name = report.el_product_traceability_dashboard.movement_pdf`) — `report/traceability_reports.py`; methods: `_get_report_values()`
  - `TraceabilityManufacturingReport` (`_name = report.el_product_traceability_dashboard.manufacturing_pdf`) — `report/traceability_reports.py`; methods: `_get_report_values()`
  - `ProductTraceabilityReport` (`_name = el.product.traceability.report`) — `models/traceability_report.py`; fields: `date:Datetime`, `company_id:Many2one`, `warehouse_id:Many2one`, `product_id:Many2one`, `product_tmpl_id:Many2one`, `categ_id:Many2one`, `lot_id:Many2one`, `move_line_id:Many2one`, `move_id:Many2one`, `picking_id:Many2one`, `production_id:Many2one`, `purchase_order_id:Many2one`, `purchase_line_id:Many2one`, `sale_order_id:Many2one`, `partner_id:Many2one`, `location_id:Many2one`, `location_dest_id:Many2one`, `uom_id:Many2one` …; methods: `init()`
  - `ProductTraceabilityManufacturing` (`_name = el.product.traceability.manufacturing`) — `models/traceability_report.py`; fields: `date:Datetime`, `company_id:Many2one`, `production_id:Many2one`, `finished_product_id:Many2one`, `finished_uom_id:Many2one`, `finished_qty:Float`, `component_product_id:Many2one`, `component_uom_id:Many2one`, `component_qty:Float`, `component_value:Float`, `state:Char`, `reference:Char`; methods: `init()`
  - `ProductTraceabilityDashboard` (`_name = el.product.traceability.dashboard`) — `models/traceability_report.py`; fields: `company_id:Many2one`, `date_from:Date`, `date_to:Date`; methods: `action_open_report()`, `get_dashboard_data()`, `get_filter_options()` …
- **Menu declarations:** `Product Traceability`, `Dashboard`, `Movement Details`, `Manufacturing Genealogy`
- **View architectures detected:** graph: 1, list: 2, pivot: 1, search: 2
- **ACL entries:** `product.traceability.report.user` (group `el_product_traceability_dashboard.group_product_traceability_user/1/0/0`), `product.traceability.dashboard.user` (group `el_product_traceability_dashboard.group_product_traceability_user/1/1/1`), `product.traceability.manufacturing.user` (group `el_product_traceability_dashboard.group_product_traceability_user/1/0/0`)
- **Functional file groups:** Reports: `report/__init__.py`, `report/traceability_reports.py`, `report/traceability_report_templates.xml`; Security: `security/ir.model.access.csv`, `security/security.xml`; Views: `views/product_traceability_views.xml`, `views/product_traceability_report_views.xml`, `views/product_traceability_menus.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `el_purchase_actual_qty` — Purchase Actual Quantity

- **Manifest version:** `18.0.2.0.0`  
- **Summary:** Actual purchase quantity with preserved value, dashboard and reporting  
- **Category / license / author:** `Purchases` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `purchase`, `purchase_stock`, `stock_account`  
- **Source inventory:** 20 files; 10 Python, 6 XML, 1 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestPurchaseActualQty` — `tests/test_purchase_actual_qty.py`; methods: `setUpClass()`, `test_effective_cost_preserves_value()`, `test_variance()`, `test_bill_line_quantity_and_value()`, `test_receipt_quantity_and_value()` …
  - `PurchaseActualExportController` — `controllers/purchase_actual_export.py`; methods: `export_csv()`
  - `PurchaseActualReport` (`_name = el.purchase.actual.report`) — `models/purchase_actual_report.py`; fields: `order_id:Many2one`, `order_name:Char`, `order_date:Datetime`, `partner_id:Many2one`, `product_id:Many2one`, `product_tmpl_id:Many2one`, `product_category_id:Many2one`, `company_id:Many2one`, `currency_id:Many2one`, `buyer_id:Many2one`, `ordered_qty:Float`, `actual_qty:Float`, `variance_qty:Float`, `variance_percent:Float`, `purchase_value:Monetary`, `effective_unit_cost:Monetary`, `variance_status:Selection`; methods: `init()`, `get_dashboard_data()`
  - `PurchaseOrderLine` extends `purchase.order.line` — `models/purchase_order_line.py`; fields: `actual_qty:Float`, `effective_price_unit:Float`, `variance_qty:Float`, `variance_percent:Float`; methods: `create()`, `write()` …
  - `ResConfigSettings` extends `res.config.settings` — `models/res_config_settings.py`; fields: `actual_qty_allow_over:Boolean`, `variance_warning_percent:Float`, `variance_critical_percent:Float`, `actual_qty_required:Boolean`
- **HTTP routes:**
  - `/purchase_actual_qty/export/csv` → `export_csv()` in `controllers/purchase_actual_export.py`
- **Menu declarations:** `Actual Quantity Dashboard`, `Actual Quantity Analysis`
- **View architectures detected:** graph: 1, list: 1, pivot: 1, search: 1, xpath: 2
- **ACL entries:** `purchase.actual.report user` (group `purchase.group_purchase_user/1/0/0`), `purchase.actual.report manager` (group `purchase.group_purchase_manager/1/0/0`)
- **Functional file groups:** Controllers: `controllers/__init__.py`, `controllers/purchase_actual_export.py`; Security: `security/ir.model.access.csv`; Data: `data/ir_actions.xml`; Views: `views/purchase_actual_report_views.xml`, `views/purchase_order_views.xml`, `views/res_config_settings_views.xml`
- **Tests present:** `tests/__init__.py`, `tests/test_purchase_actual_qty.py`

### ODOO18 / `el_readonly_user` — EL Readonly User Access

- **Manifest version:** `18.0.1.2.0`  
- **Summary:** Grant controlled read-only access to users  
- **Category / license / author:** `Extra Tools` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `web`  
- **Source inventory:** 19 files; 8 Python, 1 XML, 1 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `IrUiMenu` extends `ir.ui.menu` — `models/ir_ui_menu.py`; methods: `load_menus()`, `load_web_menus()` …
  - `IrHttp` extends `ir.http` — `models/ir_http.py`; methods: `session_info()`
  - `IrRule` extends `ir.rule` — `models/ir_rule.py`; methods: `_compute_domain()`
  - `IrModelAccess` extends `ir.model.access` — `models/ir_model_access.py`; methods: `check()`
- **Functional file groups:** Security: `security/el_readonly_user_groups.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `el_restrict_journal` — Restrict Journal for Users (Whitelist)

- **Manifest version:** `18.0.2.0.0`  
- **Summary:** Per-user journal whitelist — only allowed journals are visible  
- **Category / license / author:** `Accounting/Management` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `account`  
- **Source inventory:** 44 files; 9 Python, 4 XML, 0 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestRestrictJournal` — `tests/test_restrict_journal.py`; methods: `setUp()`, `test_01_user_allowed_journal_ids_field()`, `test_02_move_create_blocked()`, `test_03_move_write_blocked()`, `test_04_payment_create_blocked()`, `test_05_payment_write_blocked()`, `test_06_admin_not_restricted()`, `test_07_move_create_allowed()`, `test_08_payment_create_allowed()`, `test_09_multi_journal_allowed()`, `test_10_privilege_escalation_prevented()`, `test_11_constrains_layer()` …
  - `AccountJournal` extends `account.journal` — `models/account_journal.py`; fields: `allowed_user_count:Integer`; methods: `_compute_allowed_user_count()`
  - `ResUsers` extends `res.users` — `models/res_users.py`; fields: `allowed_journal_ids:Many2many`; methods: `write()`
  - `AccountMove` extends `account.move` — `models/account_move.py`; methods: `create()`, `write()` …
  - `AccountPayment` extends `account.payment` — `models/account_payment.py`; methods: `create()`, `write()` …
- **View architectures detected:** xpath: 2
- **Record rules:** `Restrict Journal: only show allowed journals`, `Restrict Journal: only show moves in allowed journals`, `Restrict Journal: only show payments in allowed journals`
- **ACL entries:** `res.users.restrict.journal.admin` (group `base.group_system/1/1/1`), `res.users.restrict.journal.manager` (group `el_restrict_journal.group_restrict_journal_manager/1/1/0`)
- **Functional file groups:** Security: `security/ir.model.access.csv`, `security/account_restrict_journal_rules.xml`, `security/account_restrict_journal_groups.xml`; Views: `views/res_users_views.xml`, `views/account_move_views.xml`
- **Tests present:** `tests/__init__.py`, `tests/test_restrict_journal.py`

### ODOO18 / `el_sale_order_confirmation_user` — Sale Order Confirmation User

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Track which user actually confirmed each sales order  
- **Category / license / author:** `Sales/Sales` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `sale`  
- **Source inventory:** 7 files; 6 Python, 1 XML, 0 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestSaleOrderConfirmationUser` — `tests/test_sale_order_confirmation_user.py`; methods: `setUpClass()`, `test_01_confirmed_by_set_to_confirming_user()`, `test_02_group_by_and_filter_confirmed_by()`, `test_03_confirmed_by_readonly_via_write()`, `test_04_confirmed_by_not_copied()`, `test_05_batch_confirmation()`, `test_06_programmatic_confirmation()`, `test_07_reconfirmation_after_cancel()`, `test_08_idempotent_confirm_does_not_overwrite()`, `test_09_pre_existing_order_not_backfilled()` …
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; fields: `confirmed_by_id:Many2one`; methods: `action_confirm()`, `write()`
- **View architectures detected:** xpath: 2
- **Functional file groups:** Views: `views/sale_order_views.xml`
- **Tests present:** `tests/test_sale_order_confirmation_user.py`, `tests/__init__.py`

### ODOO18 / `el_warehouse_access` — Warehouse-Based Access Control

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Control user access based on warehouse assignments - Global backend security enforcement  
- **Category / license / author:** `Inventory` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `stock`, `sale_stock`  
- **Source inventory:** 21 files; 13 Python, 5 XML, 0 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestWarehouseAccessControl` — `tests/test_warehouse_access.py`; methods: `setUpClass()`, `test_01_single_warehouse_user_can_see_own_warehouse()`, `test_02_single_warehouse_user_cannot_see_other_warehouses()`, `test_03_single_warehouse_picking_access()`, `test_04_single_warehouse_location_access()`, `test_05_multi_warehouse_user_sees_all_assigned()`, `test_06_multi_warehouse_user_cannot_see_unassigned()`, `test_07_multi_warehouse_picking_from_any_assigned()`, `test_08_multi_warehouse_count()`, `test_09_no_warehouse_user_has_empty_list()`, `test_10_no_warehouse_user_has_empty_locations()`, `test_11_no_warehouse_user_cannot_create_picking()` …
  - `TestWarehouseAccessRecordRules` — `tests/test_warehouse_access.py`; methods: `setUpClass()`, `test_stock_picking_rule_filters_correctly()`, `test_stock_quant_rule_filters_by_location()`
  - `TestWarehouseAccessPerformance` — `tests/test_warehouse_access.py`; methods: `setUpClass()`, `test_get_allowed_warehouse_ids_performance()`, `test_get_allowed_location_ids_performance()`
  - `StockLocation` extends `stock.location` — `models/stock_location_extension.py`; fields: `is_user_accessible:Boolean`, `warehouse_id:Many2one`; methods: `get_allowed_location_tree()` …
  - `StockMove` extends `stock.move` — `models/stock_move_extension.py`; fields: `is_user_accessible:Boolean`; methods: `create()` …
  - `StockQuant` extends `stock.quant` — `models/stock_quant_extension.py`; fields: `is_user_accessible:Boolean`, `warehouse_id:Many2one`; methods: `create()`, `write()`, `action_view_inventory()` …
  - `SaleOrder` extends `sale.order` — `models/sale_order_extension.py`; fields: `warehouse_id:Many2one`; methods: `create()` …
  - `StockPickingType` extends `stock.picking.type` — `models/stock_picking_type_extension.py`; fields: `is_user_accessible:Boolean`; methods: `create()` …
  - `ResUsers` extends `res.users` — `models/res_users_extension.py`; fields: `warehouse_ids:Many2many`, `warehouse_count:Integer`; methods: `write()`, `action_view_warehouses()`, `get_users_for_warehouse()` …
  - `StockScrap` extends `stock.scrap` — `models/stock_scrap_extension.py`; fields: `is_user_accessible:Boolean`, `warehouse_id:Many2one`; methods: `create()`, `action_validate()` …
  - `StockPicking` extends `stock.picking` — `models/stock_picking_extension.py`; fields: `is_user_accessible:Boolean`, `user_warehouse_count:Integer`, `is_single_warehouse_user:Boolean`, `location_dest_id:Many2one`; methods: `create()` …
- **Menu declarations:** `Warehouse Access Control`, `User Warehouse Assignments`, `Warehouse Access Matrix`
- **View architectures detected:** pivot: 1, xpath: 2
- **Record rules:** `Stock Picking: Warehouse-Based Access`, `Stock Move: Warehouse-Based Access`, `Stock Move Line: Warehouse-Based Access`, `Stock Quant: Location-Based Access`, `Stock Location: Warehouse-Based Access`, `Stock Warehouse: Assigned Only`, `Picking Type: Warehouse-Based Access`, `Stock Scrap: Location-Based Access`, `Sale Order: Warehouse-Based Access`, `Sale Order Line: Warehouse-Based Access`
- **ACL entries:** `res.users warehouse user` (group `el_warehouse_access.group_warehouse_user/1/0/0`), `res.users warehouse manager` (group `el_warehouse_access.group_warehouse_manager/1/1/0`), `res.users warehouse admin` (group `el_warehouse_access.group_warehouse_manager/1/1/1`), `stock.warehouse warehouse user` (group `el_warehouse_access.group_warehouse_user/1/0/0`), `stock.warehouse warehouse manager` (group `el_warehouse_access.group_warehouse_manager/1/1/1`), `stock.location warehouse user` (group `el_warehouse_access.group_warehouse_user/1/0/0`), `stock.location warehouse manager` (group `el_warehouse_access.group_warehouse_manager/1/1/1`), `stock.picking warehouse user` (group `el_warehouse_access.group_warehouse_user/1/1/1`), `stock.picking warehouse manager` (group `el_warehouse_access.group_warehouse_manager/1/1/1`), `stock.move warehouse user` (group `el_warehouse_access.group_warehouse_user/1/1/1`), `stock.move warehouse manager` (group `el_warehouse_access.group_warehouse_manager/1/1/1`), `stock.move.line warehouse user` (group `el_warehouse_access.group_warehouse_user/1/1/1`), `stock.move.line warehouse manager` (group `el_warehouse_access.group_warehouse_manager/1/1/1`), `stock.quant warehouse user` (group `el_warehouse_access.group_warehouse_user/1/1/1`), `stock.quant warehouse manager` (group `el_warehouse_access.group_warehouse_manager/1/1/1`), `stock.picking.type warehouse user` (group `el_warehouse_access.group_warehouse_user/1/0/0`), `stock.picking.type warehouse manager` (group `el_warehouse_access.group_warehouse_manager/1/1/1`), `stock.scrap warehouse user` (group `el_warehouse_access.group_warehouse_user/1/1/1`), `stock.scrap warehouse manager` (group `el_warehouse_access.group_warehouse_manager/1/1/1`)
- **Functional file groups:** Security: `security/ir.rule.xml`, `security/ir.model.access.csv`, `security/groups.xml`; Views: `views/menu.xml`, `views/stock_picking_views.xml`, `views/res_users_views.xml`
- **Tests present:** `tests/__init__.py`, `tests/test_warehouse_access.py`

### ODOO18 / `ie_restrict_qty` — Ie Restrict Qty

- **Manifest version:** `1.0`  
- **Summary:** Brief description of the module  
- **Category / license / author:** `Uncategorized` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `mail`, `stock`, `sale_management`  
- **Source inventory:** 6 files; 4 Python, 1 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ProductTemplate` extends `product.template` — `models/ie_restrict_qty.py`; fields: `qty_restrict:Float`
  - `SaleOrderLine` extends `sale.order.line` — `models/ie_restrict_qty.py`; methods: `_check_product_qty_restriction()`
- **View architectures detected:** xpath: 1
- **ACL entries:** `access.ie.restrict.qty.user` (group `base.group_user/1/1/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`; Views: `views/ie_restrict_qty_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `inventory_report_generator` — Inventory All In One Report Generator

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Dynamic Inventory Report Generator for Odoo 17  
- **Category / license / author:** `Productivity` / `AGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `stock`  
- **Source inventory:** 18 files; 8 Python, 3 XML, 1 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `InventoryPDFReport` (`_name = report.inventory_report_generator.inventory_pdf_report`) — `report/inventory_pdf_report.py`; methods: `_get_report_values()`
  - `InventoryReportGenerator` — `controllers/inventory_report_generator.py`; methods: `get_report_xlsx()`
  - `DynamicInventoryReport` (`_name = dynamic.inventory.report`) — `models/dynamic_inventory_report.py`; fields: `purchase_report:Char`, `date_from:Datetime`, `date_to:Datetime`, `report_type:Selection`; methods: `inventory_report()`, `get_filter()`, `get_filter_data()`, `create()`, `write()`, `get_inventory_xlsx_report()` …
- **HTTP routes:**
  - `/inventory_dynamic_xlsx_reports` → `get_report_xlsx()` in `controllers/inventory_report_generator.py`
- **Menu declarations:** `All In One Inventory Report`
- **ACL entries:** `access.dynamic.inventory.report.user` (group `base.group_user/1/1/1`)
- **Functional file groups:** Reports: `report/inventory_pdf_report.py`, `report/__init__.py`, `report/inventory_pdf_report_templates.xml`; Controllers: `controllers/__init__.py`, `controllers/inventory_report_generator.py`; Security: `security/ir.model.access.csv`; Views: `views/inventory_report_views.xml`
- **Tests present:** No test files detected in the addon archive.
- **Implemented development-batch changes:** Batch 01: SQL company scoping, parameterized date filters, reduced duplicate computation, spreadsheet formula-injection mitigation, constrained XLSX endpoint, sanitized client errors.

### ODOO18 / `investment_club` — Investment Clubs Management

- **Manifest version:** `18.0.12.0.0`  
- **Summary:** Complete investment management system with Unified Return System  
- **Category / license / author:** `Investment` / `LGPL-3` / `Woledge`  
- **Dependencies:** `base`, `mail`, `account`, `analytic`, `product`, `contacts`, `crm`, `sale_contract_auto`, `web`  
- **Source inventory:** 69 files; 35 Python, 29 XML, 1 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `InvestmentDashboardController` — `controllers/dashboard.py`; methods: `dashboard_stats()`
  - `MonthlyReturnsReport` (`_name = report.investment_club.monthly_returns`) — `reports/returns_report.py`; methods: `_get_report_values()`
  - `RenewalDueReport` (`_name = report.investment_club.renewal_due`) — `reports/renewal_due_report.py`; methods: `_get_report_values()`
  - `InvestorSummaryReport` (`_name = report.investment_club.investor_summary`) — `reports/investor_report.py`; methods: `_get_report_values()`
  - `InvestorStatementReport` (`_name = report.investment_club.investor_statement`) — `reports/investor_statement_report.py`; methods: `_get_report_values()`
  - `InvestmentMaturityReport` (`_name = report.investment_club.investment_maturity`) — `reports/investment_maturity_report.py`; methods: `_get_report_values()`
  - `ReturnPaymentLedgerReport` (`_name = report.investment_club.return_payment_ledger`) — `reports/return_payment_ledger_report.py`; methods: `_get_report_values()`
  - `ProjectProfitReport` (`_name = report.investment_club.project_profit`) — `reports/project_profit_report.py`; methods: `_get_report_values()`
  - `ProjectSummaryReport` (`_name = report.investment_club.project_summary`) — `reports/project_report.py`; methods: `_get_report_values()`
  - `InvestmentSubscriptionRejectWizard` (`_name = investment.subscription.reject.wizard`) — `models/investment_reject_wizard.py`; fields: `subscription_id:Many2one`, `rejection_reason:Text`; methods: `action_confirm_rejection()`
  - `AccountPayment` extends `account.payment` — `models/account_payment_inherit.py`; fields: `investment_subscription_id:Many2one`, `investment_amount:Monetary`, `investment_admin_fees:Monetary`, `investment_line_ids:One2many`; methods: `action_view_investment_subscription()`, `action_post()`, `action_cancel()`
  - `MembershipTerminateWizard` (`_name = membership.terminate.wizard`) — `models/membership_terminate_wizard.py`; fields: `membership_id:Many2one`, `partner_id:Many2one`, `club_id:Many2one`, `membership_date:Date`, `investor_code:Char`, `original_paid_fee:Float`, `current_fee:Float`, `termination_attachment:Binary`, `termination_attachment_name:Char`, `increase_amount:Float`, `months_elapsed:Integer`, `is_first_3_months:Boolean`, `deduction_amount:Float`, `actual_deduction:Float`, `client_share_increase:Float`, `company_share_increase:Float`, `company_income:Float`, `refund_amount:Float` …; methods: `action_confirm_termination()` …
  - `AccountMove` extends `account.move` — `models/account_move.py`; fields: `investor_code_id:Many2one`, `investor_code:Char`; methods: `_investment_activate_membership_if_paid()`
  - `AccountFullReconcile` extends `account.full.reconcile` — `models/account_move.py`; methods: `create()`
  - `AccountPartialReconcile` extends `account.partial.reconcile` — `models/account_move.py`; methods: `create()`
  - `TerminateReason` (`_name = terminate.reason`) — `models/terminate_reason.py`; fields: `name:Char`, `type:Selection`, `active:Boolean`, `sequence:Integer`
  - `InvestmentDashboard` (`_name = investment.dashboard`) — `models/dashboard.py`; fields: `total_clubs:Integer`, `total_projects:Integer`, `total_memberships:Integer`, `active_memberships:Integer`, `terminated_memberships:Integer`, `expired_memberships:Integer`, `total_subscriptions:Integer`, `active_subscriptions:Integer`, `terminated_subscriptions:Integer`, `total_returns:Integer`, `paid_returns:Integer`, `due_returns:Integer`, `total_invested:Float`, `overdue_renewals:Integer`; methods: `create()`, `write()`, `action_refresh()` …
  - `SaleContract` extends `sale.contract` — `models/sale_contract_inherit.py`; fields: `investment_subscription_id:Many2one`, `investment_membership_id:Many2one`; methods: `action_view_investment_subscription()`, `action_view_investment_membership()`
  - `InvestmentMembership` (`_name = investment.membership`) extends `mail.thread`, `mail.activity.mixin` — `models/membership.py`; fields: `membership_number:Char`, `partner_id:Many2one`, `club_id:Many2one`, `membership_product_id:Many2one`, `initial_membership_fee:Float`, `subscription_product_id:Many2one`, `annual_subscription_fee:Float`, `subscription_period:Selection`, `membership_date:Date`, `expiry_date:Date`, `auto_renew:Boolean`, `initial_invoice_id:Many2one`, `current_invoice_id:Many2one`, `payment_state:Selection`, `renewal_ids:One2many`, `next_renewal_date:Date`, `next_renewal_amount:Float`, `renewal_status:Selection` …; methods: `action_create_initial_invoice()`, `action_open_invoice()`, `action_create_renewal_invoice()`, `action_review_money_bank()`, `action_confirm_payment()`, `action_terminate()`, `action_death_case()`, `action_cancel()`, `action_reset_to_draft()`, `action_create_investment()`, `action_open_investment()`, `action_view_contract()` …
  - `InvestmentSubscription` (`_name = investment.subscription`) extends `mail.thread`, `mail.activity.mixin` — `models/investment_subscription.py`; fields: `name:Char`, `membership_id:Many2one`, `partner_id:Many2one`, `club_id:Many2one`, `project_id:Many2one`, `return_1_amount:Float`, `return_1_grace_months:Integer`, `return_1_date:Date`, `return_1_repeat_count:Integer`, `return_1_repeat_duration:Integer`, `return_1_repeat_until_membership:Boolean`, `return_2_amount:Float`, `return_2_percentage:Float`, `return_2_partner_share:Char`, `return_2_grace_months:Integer`, `return_2_period_months:Integer`, `return_2_duration_years:Integer`, `return_2_first_date:Date` …; methods: `create()`, `copy()`, `write()`, `action_submit_approval()`, `action_approve()`, `action_reject()`, `action_review_money_bank_inv()`, `action_register_payment()`, `action_reset_to_draft()`, `action_activate()`, `action_view_contract()`, `action_view_payment()` …
  - `ResConfigSettings` extends `res.config.settings` — `models/res_config_settings.py`; fields: `membership_product_id:Many2one`, `subscription_product_id:Many2one`, `admin_fees_product_id:Many2one`, `subscription_period:Selection`, `auto_renewal_days:Integer`, `payment_journal_id:Many2one`, `return_payment_journal_id:Many2one`, `auto_activate_projects:Boolean`, `grace_period_months:Integer`, `enable_renewal_notifications:Boolean`, `enable_payment_notifications:Boolean`, `restrict_project_creation:Boolean`, `require_approval_for_investment:Boolean`, `module_access_enabled:Boolean`, `invoice_prefix:Char`, `termination_allowed_months:Integer`, `termination_deduction_amount:Float`, `termination_client_share_pct:Float` …
  - `InvestmentActualReturn` (`_name = investment.actual.return`) extends `mail.thread`, `mail.activity.mixin` — `models/actual_return.py`; fields: `name:Char`, `subscription_id:Many2one`, `membership_id:Many2one`, `partner_id:Many2one`, `project_id:Many2one`, `return_type:Selection`, `period_name:Char`, `date_from:Date`, `date_to:Date`, `expected_amount:Float`, `actual_amount:Float`, `difference:Float`, `payment_journal_id:Many2one`, `payment_id:Many2one`, `state:Selection`, `notes:Text`, `company_id:Many2one`; methods: `create()`, `action_register_payment()`, `action_cancel()`, `name_get()` …
  - `InvestorDeathWizard` (`_name = investor.death.wizard`) — `models/investor_death_wizard.py`; fields: `membership_id:Many2one`, `subscription_id:Many2one`, `partner_id:Many2one`, `investor_code:Char`, `club_id:Many2one`, `membership_date:Date`, `death_date:Date`, `inheritance_document:Binary`, `inheritance_document_name:Char`, `action_type:Selection`, `new_partner_id:Many2one`, `new_investor_code:Char`, `membership_original_paid:Float`, `subscription_total:Float`, `subscription_project:Char`, `refund_amount:Float`, `refund_journal_id:Many2one`, `notes:Text`; methods: `action_confirm_death_case()` …
  - `InvestmentContact` extends `res.partner` — `models/contact_codes.py`; fields: `employee_code:Char`, `customer_code:Char`, `vendor_code:Char`, `investor_code:Char`, `employee_code_check:Boolean`, `customer_code_check:Boolean`, `vendor_code_check:Boolean`, `investor_code_check:Boolean`, `club_id:Many2one`; methods: `default_get()`, `create()`, `write()` …
  - `InvestmentClub` (`_name = investment.club`) extends `mail.thread`, `mail.activity.mixin` — `models/investment_club.py`; fields: `name_ar:Char`, `name_en:Char`, `name:Char`, `display_name:Char`, `code:Char`, `is_active:Boolean`, `active:Boolean`, `administrative_fees:Float`, `max_members:Integer`, `current_members_count:Integer`, `terms_conditions:Text`, `project_ids:One2many`, `member_ids:One2many`, `active_members_count:Integer`, `company_id:Many2one`, `notes:Text`; methods: `toggle_active()`, `create()` …
  - `CrmLead` extends `crm.lead` — `models/crm_lead.py`; fields: `interested_project_id:Many2one`, `club_id:Many2one`; methods: `action_create_membership()`, `action_view_investment_projects()`
  - `Contact` extends `res.partner` — `models/contact.py`; fields: `code:Char`
  - `InvestmentProject` (`_name = investment.project`) extends `investment.project`, `mail.thread`, `mail.activity.mixin` — `models/investment_project_inherit.py`; methods: `create()` …
  - `MembershipRenewal` (`_name = membership.renewal`) — `models/membership_renewal.py`; fields: `membership_id:Many2one`, `partner_id:Many2one`, `club_id:Many2one`, `renewal_date:Date`, `amount:Float`, `period:Selection`, `old_expiry_date:Date`, `new_expiry_date:Date`, `invoice_id:Many2one`, `state:Selection`, `notes:Text`, `company_id:Many2one`; methods: `name_get()`
  - `InvestmentActualReturn` (`_name = investment.actual.return`) extends `investment.actual.return` — `models/investment_actual_return_inherit.py`; methods: `action_process_return_payment()` …
  - `SubscriptionTerminateWizard` (`_name = subscription.terminate.wizard`) — `models/subscription_terminate_wizard.py`; fields: `subscription_id:Many2one`, `membership_id:Many2one`, `partner_id:Many2one`, `project_id:Many2one`, `investor_code:Char`, `membership_date:Date`, `investment_date:Date`, `share_count:Integer`, `share_value:Float`, `total_amount:Float`, `total_returns_paid:Float`, `membership_months_elapsed:Integer`, `is_first_3_months:Boolean`, `refund_amount:Float`, `refund_journal_id:Many2one`, `reason:Many2one`, `notes:Text`; methods: `action_confirm_termination()` …
  - `InvestmentProject` (`_name = investment.project`) extends `mail.thread`, `mail.activity.mixin` — `models/investment_project.py`; fields: `name:Char`, `code:Char`, `club_id:Many2one`, `analytic_account_id:Many2one`, `share_value:Float`, `contract_start_date:Date`, `contract_end_date:Date`, `max_shares_per_investor:Integer`, `max_investors:Integer`, `active_investor_count:Integer`, `similar_items_count:Integer`, `admin_fees_value:Float`, `return_1_amount:Float`, `return_1_grace_months:Integer`, `return_1_date:Date`, `return_1_repeat_count:Integer`, `return_1_repeat_duration:Integer`, `return_1_repeat_until_membership:Boolean` …; methods: `create()`, `action_activate()`, `action_close()` …
- **HTTP routes:**
  - `/investment/dashboard/stats` → `dashboard_stats()` in `controllers/dashboard.py`
- **Menu declarations:** `Investment`, `Dashboard`, `Clubs`, `Return Payments`, `Projects`, `Investments`, `Memberships`, `Terminations`, `Terminated Memberships`, `Terminated Subscriptions`, `Configuration`, `Settings`, `Termination Reasons`, `Reports`, `1. Renewal Due`, `2. Monthly Returns`, `3. Investor Summary`, `4. Active Investments`, `5. All Investors`, `6. Return Payments Summary` …
- **View architectures detected:** calendar: 1, form: 8, list: 15, search: 5, xpath: 7
- **Record rules:** `Investment Project: Access`, `Investment Subscription: Access`, `Investment Membership: Access`, `Actual Return: Access`, `Investment Project: User Read Only`, `Investment Project: Manager Full Access`, `Investment Subscription: User View Own`, `Investment Subscription: Manager Full Access`, `Investment Membership: User View Own`, `Investment Membership: Manager Full Access`, `Actual Return: User View Own`, `Actual Return: Manager Full Access`
- **ACL entries:** `Club` (group `group_investment_access/1/1/1`), `Project` (group `group_investment_access/1/1/1`), `Membership` (group `group_investment_access/1/1/1`), `Renewal` (group `group_investment_access/1/1/1`), `Subscription` (group `group_investment_access/1/1/1`), `Actual Return` (group `group_investment_access/1/1/1`), `Membership Terminate Wizard` (group `group_investment_access/1/1/1`), `Subscription Terminate Wizard` (group `group_investment_access/1/1/1`), `Investor Death Wizard` (group `group_investment_access/1/1/1`), `Club User` (group `group_investment_user/1/0/0`), `Club Manager` (group `group_investment_manager/1/1/1`), `Project User` (group `group_investment_user/1/0/0`), `Project Manager` (group `group_investment_manager/1/1/1`), `Membership User` (group `group_investment_user/1/1/1`), `Membership Manager` (group `group_investment_manager/1/1/1`), `Renewal User` (group `group_investment_user/1/1/1`), `Renewal Manager` (group `group_investment_manager/1/1/1`), `Subscription User` (group `group_investment_user/1/1/1`), `Subscription Manager` (group `group_investment_manager/1/1/1`), `Actual Return User` (group `group_investment_user/1/1/1`) …
- **Functional file groups:** Controllers: `controllers/dashboard.py`, `controllers/__init__.py`; Security: `security/ir.model.access.csv`, `security/security.xml`, `security/investment_club_security.xml`; Data: `data/cron_data.xml`, `data/sequences.xml`, `data/terminate_reason_data.xml`; Views: `views/menu.xml`, `views/terminate_wizards_views.xml`, `views/sale_contract_inherit_views.xml`, `views/dashboard_views.xml`, `views/actual_return_views.xml`, `views/contact_view.xml`, `views/account_payment_inherit_views.xml`, `views/crm_lead_views.xml` …
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `invoice_stock_move` — Stock Picking From Invoice

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Stock Picking From Customer/Supplier Invoice  
- **Category / license / author:** `Accounting` / `AGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `account`, `stock`, `payment`  
- **Source inventory:** 10 files; 5 Python, 1 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `AccountMoveLine` extends `account.move.line` — `models/account_move_line.py`; methods: `_create_stock_moves()`
  - `AccountMove` extends `account.move` — `models/account_move.py`; fields: `picking_count:Integer`, `invoice_picking_id:Many2one`, `picking_type_id:Many2one`; methods: `action_stock_move()`, `action_view_picking()` …
- **View architectures detected:** xpath: 1
- **Functional file groups:** Views: `views/account_move_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `meno` — meno

- **Manifest version:** `18.0`  
- **Summary:** Crack odoo v18  
- **Category / license / author:** `not declared` / `not declared` / `meno`  
- **Dependencies:** `base`, `base_setup`  
- **Source inventory:** 11 files; 6 Python, 3 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ir_module_module` extends `ir.module.module` — `models/models.py`; methods: `crack()`, `cracks()`, `button_immediate_upgrade()`
  - `IrConfigParameter` extends `ir.config_parameter` — `models/models.py`; methods: `cracks()`
- **ACL entries:** `crack.crack` (group `/1/0/0`)
- **Functional file groups:** Controllers: `controllers/controllers.py`, `controllers/__init__.py`; Security: `security/ir.model.access.csv`; Data: `data/cracks_test.xml`; Views: `views/views.xml`, `views/templates.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `odoo_multi_channel_sale` — Odoo Multi-Channel Sale

- **Manifest version:** `2.8.24`  
- **Summary:** The multi channel module is Multiple platform connector with Odoo. You can connect and manage various platforms like Bagisto, Cscart, CSV, Ebay, Etsy, Flipkart, Magento 2, Prestashop, Shopify, Walmart, Woocommerce in odoo with the help of Odoo multichannel sale bridge.  
- **Category / license / author:** `eCommerce` / `Other proprietary` / `Webkul Software Pvt. Ltd.`  
- **Dependencies:** `stock_delivery`, `wk_wizard_messages`  
- **Source inventory:** 211 files; 88 Python, 47 XML, 2 JavaScript, 0 SCSS; 5 test files.  
- **Python classes / models:**
  - `TestMultiChannelCommon` — `tests/common.py`; methods: `setUp()`
  - `TestFeedMultichannel` — `tests/test_feeds.py`; methods: `test_category_feed()`, `test_product_feeds()`, `test_partner_feeds()`, `test_partner_name_fallback_order()`, `test_order_feed()`, `test_shpping_feeds()`, `test_skip_product_images_context_flags()`
  - `TestMultichannelConnection` — `tests/test_connections.py`; methods: `test_connections()`
  - `TestMappingMultichannel` — `tests/test_mappings.py`; methods: `test_category_mappings()`, `test_product_mappings()`, `test_order_mappings()`, `test_shipping_mappings()`, `test_partner_mappings()`
  - `FeedSyncWizard` (`_name = feed.sync.wizard`) — `wizard/feed_wizard.py`; fields: `channel_id:Many2one`, `feed_type:Selection`; methods: `action_sync_feed()`
  - `UpdateMappingWizard` (`_name = update.mapping.wizard`) — `wizard/update_mapping_wizard.py`; fields: `need_sync:Selection`; methods: `save_status()`
  - `ImportPartner` (`_name = import.partners`) extends `import.operation` — `wizard/imports/import_partner.py`; fields: `partner_ids:Text`
  - `ImportProduct` (`_name = import.products`) extends `import.operation` — `wizard/imports/import_product.py`; fields: `product_ids:Text`, `source:Selection`
  - `ImportOrder` (`_name = import.orders`) extends `import.operation` — `wizard/imports/import_order.py`; fields: `source:Selection`, `order_ids:Text`
  - `ImportCategory` (`_name = import.categories`) extends `import.operation` — `wizard/imports/import_category.py`; fields: `category_ids:Text`, `parent_categ_id:Many2one`
  - `ImportOperation` (`_name = import.operation`) extends `channel.operation` — `wizard/imports/import_operation.py`; fields: `object:Selection`, `operation:Selection`; methods: `import_button()`, `import_with_filter()`
  - `ImportAttributeValue` (`_name = import.attributes.value`) extends `import.operation` — `wizard/imports/import_attribute_value.py`; fields: `attribute_value_ids:Text`
  - `ImportTemplate` (`_name = import.templates`) extends `import.operation` — `wizard/imports/import_template.py`; fields: `product_tmpl_ids:Text`, `source:Selection`
  - `ImportAttribute` (`_name = import.attributes`) extends `import.operation` — `wizard/imports/import_attribute.py`; fields: `attribute_ids:Text`
  - `WkWizardMessage` extends `wk.wizard.message` — `wizard/wizard_message.py`; methods: `operation_back()`
  - `ChannelOperation` (`_name = channel.operation`) — `wizard/channel_operation.py`; fields: `channel:Selection`, `image:Image`, `api_record_limit:Integer`, `wk_from_date:to_string`, `wk_to_date:to_string`, `from_date:Datetime`, `to_date:Datetime`, `channel_id:Many2one`, `import_order_date:Datetime`, `update_order_date:Datetime`, `import_product_date:Datetime`, `update_product_date:Datetime`, `import_customer_date:Datetime`, `update_customer_date:Datetime`; methods: `default_channel_id()`, `default_get()`, `post_feed_import_process()`, `exclude_export_data()`, `export_message()` …
  - `BarcodeConflictWizard` (`_name = barcode.conflict.wizard`) — `wizard/barcode_conflict_wizard.py`; fields: `feed_ids:Many2many`, `line_ids:One2many`, `conflict_count:Integer`, `summary:Html`; methods: `default_get()`, `create_from_feeds()`, `action_open_wizard()`, `action_apply()`, `action_apply_and_evaluate()` …
  - `BarcodeConflictLine` (`_name = barcode.conflict.line`) — `wizard/barcode_conflict_wizard.py`; fields: `wizard_id:Many2one`, `feed_id:Many2one`, `barcode:Char`, `related_barcodes:Char`, `conflict_type:Selection`, `feed_source:Char`, `product_ids:Many2many`, `product_info:Text`, `preferred_product_id:Many2one`, `recommended_action:Selection`, `action:Selection`, `note:Char`, `variant_feed_ids:Many2many`, `affects_template:Boolean`; methods: `action_open_products()` …
  - `ExportPartner` (`_name = export.partners`) extends `export.operation` — `wizard/exports/export_partner.py`; fields: `partner_ids:Many2many`
  - `ExportAttributeValue` (`_name = export.attributes.value`) extends `export.operation` — `wizard/exports/export_attribute_value.py`; fields: `attribute_value_ids:Many2many`; methods: `default_get()`
  - `ExportOrder` (`_name = export.orders`) extends `export.operation` — `wizard/exports/export_order.py`; fields: `order_ids:Many2many`; methods: `default_get()` …
  - `ExportOperation` (`_name = export.operation`) extends `channel.operation` — `wizard/exports/export_operation.py`; fields: `operation:Selection`, `object:Selection`; methods: `export_button()`
  - `ExportCategory` (`_name = export.categories`) extends `export.operation` — `wizard/exports/export_category.py`; fields: `category_ids:Many2many`; methods: `default_get()`
  - `ExportProduct` (`_name = export.products`) extends `export.operation` — `wizard/exports/export_product.py`; fields: `product_ids:Many2many`, `sku_sequence_id:Many2one`; methods: `export_odoo_products()`, `update_odoo_products()`, `default_get()`
  - `ExportAttribute` (`_name = export.attributes`) extends `export.operation` — `wizard/exports/export_attribute.py`; fields: `attribute_ids:Many2many`; methods: `default_get()`
  - `ExportTemplate` (`_name = export.templates`) extends `export.operation` — `wizard/exports/export_template.py`; fields: `product_tmpl_ids:Many2many`, `sku_sequence_id:Many2one`; methods: `export_odoo_products()`, `update_odoo_products()`, `default_get()`
  - `Transaction` — `ApiTransaction.py`; methods: `import_data()`, `getFeedObjectDictionary()`, `export_data()`, `get_remote_id()`, `create_mapping()`, `getActionMessage()` …
  - `WebsiteBackend` — `controllers/backend.py`; methods: `fetch_dashboard_data()`, `fetch_instance_dashboard_data()`
  - `Channel` — `controllers/main.py`; methods: `update_mapping()`, `core_content_image()`, `content_image()`
  - `ChannelWebhook` — `controllers/webhooks.py`; methods: `get_super_env()`, `import_common_webhook()`, `import_order_webhook()`, `create_order_data()`, `update_order_data()`, `evaluate_order_webhook()`
  - `PartnerFeed` (`_name = partner.feed`) extends `wk.feed` — `models/feeds/partner_feed.py`; fields: `email:Char`, `phone:Char`, `mobile:Char`, `website:Char`, `last_name:Char`, `street:Char`, `street2:Char`, `city:Char`, `zip:Char`, `state_name:Char`, `state_id:Char`, `country_id:Char`, `parent_id:Char`, `vat:Char`, `type:Selection`, `company_name:Char`; methods: `get_partner_fields()`, `import_partner()`, `import_items()` …
  - `ProductFeed` (`_name = product.feed`) extends `product.variant.feed` — `models/feeds/product_feed.py`; fields: `need_sync:Selection`, `feed_variants:One2many`; methods: `action_resolve_barcode_conflicts()`, `match_attribute()`, `match_attribute_value()`, `create_attribute_string()`, `update_product_variants()`, `get_variant_extra_values()`, `wk_change_product_price()`, `wk_change_product_qty()`, `check_attribute_value()`, `import_product()`, `import_items()` …
  - `OrderFeed` (`_name = order.feed`) extends `wk.feed`, `order.line.feed` — `models/feeds/order_feed.py`; fields: `partner_id:Char`, `order_state:Char`, `date_order:Char`, `confirmation_date:Char`, `date_invoice:Char`, `date_shipping:Char`, `carrier_id:Char`, `payment_method:Char`, `currency:Char`, `customer_is_guest:Boolean`, `customer_name:Char`, `customer_phone:Char`, `customer_mobile:Char`, `customer_last_name:Char`, `customer_email:Char`, `customer_company:Char`, `shipping_partner_id:Char`, `shipping_name:Char` …; methods: `get_taxes_ids()`, `get_order_date_info()`, `get_order_fields()`, `import_order()`, `import_items()` …
  - `CategoryFeed` (`_name = category.feed`) extends `wk.feed` — `models/feeds/category_feed.py`; fields: `description:Text`, `parent_id:Char`, `leaf_category:Boolean`; methods: `get_channel_specific_categ_vals()`, `import_category()`, `import_items()` …
  - `ProductVariantFeed` (`_name = product.variant.feed`) extends `wk.feed` — `models/feeds/variant_feed.py`; fields: `name_value:Text`, `extra_categ_ids:Text`, `type:Char`, `is_storable:Boolean`, `list_price:Char`, `default_code:Char`, `barcode:Char`, `description:Text`, `description_sale:Text`, `description_purchase:Text`, `standard_price:Char`, `sale_delay:Char`, `qty_available:Char`, `weight:Char`, `weight_unit:Char`, `length:Char`, `width:Char`, `height:Char` …
  - `WkFeed` (`_name = wk.feed`) — `models/feeds/feed.py`; fields: `name:Char`, `sequence:Char`, `store_id:Char`, `store_source:Char`, `message:Html`, `active:Boolean`, `state:Selection`, `channel_id:Many2one`, `channel:Selection`; methods: `write()`, `get_product_fields()`, `get_category_fields()`, `open_mapping_view()`, `set_feed_state()`, `get_feed_result()`, `get_channel_domain()`, `get_categ_id()`, `get_extra_categ_ids()`, `get_order_partner_id()`, `get_partner_id()`, `get_product_id()` …
  - `OrderLineFeed` (`_name = order.line.feed`) — `models/feeds/order_line_feed.py`; fields: `line_name:Char`, `line_product_uom_qty:Char`, `line_price_unit:Char`, `line_product_id:Char`, `line_product_default_code:Char`, `line_product_barcode:Char`, `line_taxes:Text`, `order_feed_id:Many2one`, `line_source:Selection`, `line_variant_ids:Char`
  - `ShippingFeed` (`_name = shipping.feed`) extends `wk.feed` — `models/feeds/shipping_feed.py`; fields: `description:Text`, `shipping_carrier:Char`, `is_international:Boolean`; methods: `get_shipping_fields()`, `get_shiping_carrier()`, `get_shiping_carrier_mapping()`, `create_shipping_mapping()`, `import_item()`, `import_items()` …
  - `MultiChannelWebhook` extends `multi.channel.sale` — `models/base/multi_channel_webhook.py`; fields: `is_create_order_webhook:Boolean`, `order_webhook_url:Char`, `order_webhook_id:Char`, `is_update_order_webhook:Boolean`, `order_update_webhook_url:Char`, `order_update_webhook_id:Char`, `create_order_webhook_status:Selection`; methods: `change_order_webhook()`, `change_update_order_webhook()` …
  - `MultiChannelSkeleton` (`_name = multi.channel.skeleton`) — `models/base/multi_channel_skeleton.py`; methods: `_ConfirmOdooOrder()`, `_cancel_order()`, `_SetOdooOrderState()`
  - `MultiChannelSale` extends `multi.channel.sale` — `models/base/match_records.py`; methods: `get_channel_domain()`, `match_create_pricelist_id()`, `match_attribute_mappings()`, `match_attribute_value_mappings()`, `match_product_mappings()`, `match_template_mappings()`, `match_partner_mappings()`, `match_order_mappings()`, `match_carrier_mappings()`, `match_category_mappings()`, `match_category_feeds()`, `match_product_feeds()` …
  - `MultiChannelSale` (`_name = multi.channel.sale`) extends `mail.thread`, `mail.activity.mixin` — `models/base/multi_channel_sale.py`; fields: `import_order_cron:Boolean`, `import_product_cron:Boolean`, `import_partner_cron:Boolean`, `import_category_cron:Boolean`, `channel_stock_action:Selection`, `order_ecomm_sequence:Boolean`, `sync_customer_company:Boolean`, `url:Char`, `email:Char`, `api_key:Char`, `active:Boolean`, `color_index:Integer`, `channel:Selection`, `name:Char`, `state:Selection`, `color:Char`, `image:Image`, `blog_url:Char` …; methods: `create()`, `test_connection()`, `set_to_draft()`, `open_mapping_view()`, `open_record_view()`, `open_cron_views()`, `set_info_urls()`, `get_channel_time_zone()`, `check_api_record_limit()`, `set_channel_date()`, `toggle_enviroment_value()`, `toggle_debug_value()` …
  - `MultiChannelSkeleton` extends `multi.channel.skeleton` — `models/base/invoice_order.py`; methods: `CreatePaymentMethod()`, `create_order_invoice()`, `SetOrderPaid()` …
  - `MultiChannelSale` extends `multi.channel.sale` — `models/base/sync_feeds.py`; methods: `sync_order_feeds()`, `sync_partner_feeds()`, `sync_category_feeds()`, `sync_product_feeds()`, `get_channel_dict()`
  - `MultiChannelSale` extends `multi.channel.sale` — `models/base/create_mapping.py`; methods: `create_attribute_mapping()`, `create_attribute_value_mapping()`, `create_partner_mapping()`, `create_carrier_mapping()`, `create_template_mapping()`, `create_product_mapping()`, `create_category_mapping()`, `create_order_mapping()`, `create_channel_mapping()` …
  - `MultiChannelSale` extends `multi.channel.sale` — `models/base/message_operations.py`; methods: `get_operation_message_v1()`, `get_feed_import_message()`, `display_message()`
  - `MultiChannelSale` extends `multi.channel.sale` — `models/base/cron_operations.py`; methods: `cron_feed_evaluation()`, `cron_import_product_images()`, `get_cron_fields_map()`, `cron_import_all()`, `set_channel_cron()`
  - `ExtraCategories` (`_name = extra.categories`) — `models/base/extra_categories.py`; fields: `instance_id:Many2one`, `product_id:Many2one`, `category_id:Many2one`, `extra_category_ids:Many2many`, `extra_category_domain_ids:Many2many`; methods: `get_category_list()`, `change_domain()` …
  - `ChannelOrderStates` (`_name = channel.order.states`) — `models/base/channel_order_states.py`; fields: `channel_state:Char`, `odoo_order_state:Selection`, `channel_id:Many2one`, `channel_name:Selection`, `default_order_state:Boolean`, `odoo_create_invoice:Boolean`, `odoo_set_invoice_state:Selection`, `odoo_ship_order:Boolean`; methods: `_check_default_order_state()`, `_check_order_state()`
  - `MultiChannelSkeleton` extends `multi.channel.skeleton` — `models/base/ship_order.py`; methods: `set_order_shipped()`
  - `MultiChannelSale` extends `multi.channel.sale` — `models/base/get_channel_data.py`; methods: `get_quantity()`, `get_core_feature_compatible_channels()`, `get_channel()`, `get_info_urls()`, `get_data_isoformat()`, `get_state_id()`, `get_country_id()`, `get_currency_id()`, `get_uom_id()`, `get_store_attribute_id()`, `get_store_attribute_value_id()`, `get_channel_vals()` …
  - `ChannelAttributeMappings` (`_name = channel.attribute.mappings`) extends `channel.mappings` — `models/mappings/attribute_mapping.py`; fields: `store_attribute_id:Char`, `store_attribute_name:Char`, `attribute_name:Many2one`, `odoo_attribute_id:Integer`; methods: `change_odoo_id()` …
  - `ChannelOrderMappings` (`_name = channel.order.mappings`) extends `channel.mappings` — `models/mappings/order_mapping.py`; fields: `store_order_id:Char`, `order_name:Many2one`, `odoo_order_id:Integer`, `odoo_partner_id:Many2one`, `is_delivered:Boolean`, `is_invoiced:Boolean`, `store_order_status:Char`; methods: `unlink()`, `change_odoo_id()`, `update_order_mapping_status()` …
  - `ChannelMappings` (`_name = channel.mappings`) — `models/mappings/channel_mapping.py`; fields: `name:Char`, `store_id:Char`, `channel_id:Many2one`, `ecom_store:Selection`, `need_sync:Selection`, `operation:Selection`; methods: `eComStoreUsed()`, `default_channel_id()`, `get_need_sync_mapping()`, `create()`, `write()` …
  - `ChannelCategoryMappings` (`_name = channel.category.mappings`) extends `channel.mappings` — `models/mappings/category_mapping.py`; fields: `store_category_id:Char`, `category_name:Many2one`, `odoo_category_id:Integer`, `leaf_category:Boolean`; methods: `unlink()`, `change_odoo_id()` …
  - `ChannelAttributeValueMappings` (`_name = channel.attribute.value.mappings`) extends `channel.mappings` — `models/mappings/attribute_value_mapping.py`; fields: `store_attribute_value_id:Char`, `store_attribute_value_name:Char`, `attribute_value_name:Many2one`, `odoo_attribute_value_id:Integer`; methods: `change_odoo_id()` …
  - `ChannelShippingMappings` (`_name = channel.shipping.mappings`) extends `channel.mappings` — `models/mappings/shipping_mapping.py`; fields: `shipping_service:Char`, `shipping_service_id:Char`, `odoo_shipping_carrier:Many2one`, `odoo_carrier_id:Integer`, `international_shipping:Boolean`; methods: `change_odoo_id()` …
  - `ChannelSynchronization` (`_name = channel.synchronization`) extends `channel.mappings` — `models/mappings/channel_synchronization.py`; fields: `ecomstore_refrence:Char`, `odoo_id:Text`, `summary:Text`, `status:Selection`, `action_on:Selection`, `action_type:Selection`; methods: `cron_clear_history()`
  - `ChannelProductMappings` (`_name = channel.product.mappings`) extends `channel.mappings` — `models/mappings/product_variant_mapping.py`; fields: `store_product_id:Char`, `store_variant_id:Char`, `product_name:Many2one`, `erp_product_id:Integer`, `odoo_template_id:Many2one`, `default_code:Char`, `barcode:Char`; methods: `change_odoo_id()` …
  - `ChannelAccountJournalMappings` (`_name = channel.account.journal.mappings`) extends `channel.mappings` — `models/mappings/account_journal_mapping.py`; fields: `store_journal_name:Char`, `odoo_journal:Many2one`, `journal_code:Char`, `odoo_journal_id:Integer`; methods: `change_odoo_id()` …
  - `ChannelTemplateMappings` (`_name = channel.template.mappings`) extends `channel.mappings` — `models/mappings/product_template_mapping.py`; fields: `store_product_id:Char`, `template_name:Many2one`, `odoo_template_id:Char`, `default_code:Char`, `barcode:Char`; methods: `unlink()`, `change_odoo_id()` …
  - `ChannelPricelistMappings` (`_name = channel.pricelist.mappings`) extends `channel.mappings` — `models/mappings/pricelist_mapping.py`; fields: `name:Char`, `channel_id:Many2one`, `store_currency:Many2one`, `store_currency_code:Char`, `odoo_pricelist_id:Many2one`, `odoo_currency:Many2one`, `odoo_currency_id:Integer`; methods: `set_odoo_currency_id()`, `ecom_storeUsed()` …
  - `ChannelOrderMappings` (`_name = channel.partner.mappings`) extends `channel.mappings` — `models/mappings/partner_mapping.py`; fields: `type:Selection`, `store_customer_id:Char`, `odoo_partner:Many2one`, `odoo_partner_id:Integer`; methods: `change_odoo_id()` …
  - `ChannelAccountMappings` (`_name = channel.account.mappings`) extends `channel.mappings` — `models/mappings/account_mapping.py`; fields: `store_tax_value_id:Char`, `odoo_tax_id:Integer`, `tax_name:Many2one`, `include_in_price:Boolean`, `tax_type:Selection`; methods: `change_odoo_id()` …
  - `ProductProduct` extends `product.product` — `models/core/product_product.py`; fields: `channel_mapping_ids:One2many`, `wk_extra_price:Float`, `price_extra:Float`, `attr_price_extra:Float`; methods: `write()`, `check_for_new_price()`, `get_product_attribute_id()`, `get_product_attribute_value_id()`, `check_for_new_attrs()` …
  - `PricelistItem` extends `product.pricelist.item` — `models/core/product_pricelist_item.py`; methods: `write()`, `create()`
  - `ProductCategory` extends `product.category` — `models/core/product_category.py`; fields: `channel_mapping_ids:One2many`, `channel_category_ids:One2many`; methods: `write()`, `unlink()`
  - `AccountInvoice` extends `account.move` — `models/core/account_invoice.py`; methods: `wk_get_invoice_order()`, `wk_pre_confirm_paid()`, `wk_post_confirm_paid()` …
  - `MultiChannelSaleConfig` extends `res.config.settings` — `models/core/res_config.py`; fields: `cron_import_partner:Many2one`, `cron_import_category:Many2one`, `cron_import_product:Many2one`, `cron_import_order:Many2one`, `cron_evaluation:Many2one`, `cron_import_product_images:Many2one`, `cron_clear_history:Many2one`, `avoid_duplicity:Boolean`, `avoid_duplicity_using:Selection`; methods: `set_values()`, `get_values()`
  - `ResPartner` extends `res.partner` — `models/core/res_partner.py`; fields: `channel_mapping_ids:One2many`
  - `StockPicking` extends `stock.picking` — `models/core/stock_picking.py`; methods: `wk_pre_do_transfer()`, `wk_post_do_transfer()` …
  - `ProductTemplate` extends `product.template` — `models/core/product_template.py`; fields: `wk_default_code:Char`, `wk_length:Float`, `width:Float`, `height:Float`, `dimensions_uom_id:Many2one`, `channel_mapping_ids:One2many`, `channel_category_ids:One2many`, `channel_ids:Many2many`, `wk_product_id_type:Selection`; methods: `write()`, `unlink()` …
  - `SaleOrder` extends `sale.order` — `models/core/sale_order.py`; fields: `channel_mapping_ids:One2many`; methods: `action_cancel()`, `wk_pre_cancel()`, `wk_post_cancel()`
  - `ProductAttribute` extends `product.attribute` — `models/core/product_attribute.py`; methods: `create()`
  - `StockMove` extends `stock.move` — `models/core/stock_move.py`; methods: `post_operation()`, `multichannel_sync_quantity()` …
  - `DeliveryCarrier` extends `delivery.carrier` — `models/core/delivery_carrier.py`; fields: `channel_mapping_ids:One2many`
- **HTTP routes:**
  - `/multichannel/fetch_dashboard_data` → `fetch_dashboard_data()` in `controllers/backend.py`
  - `/multichannel/fetch_dashboard_data/<int:channel_id>` → `fetch_instance_dashboard_data()` in `controllers/backend.py`
  - `/channel/update/mapping` → `update_mapping()` in `controllers/main.py`
  - `/channel/image.png` → `content_image()` in `controllers/main.py`
  - `/channel/image/<xmlid>.png` → `content_image()` in `controllers/main.py`
  - `/channel/image/<xmlid>/<int:width>x<int:height>.png` → `content_image()` in `controllers/main.py`
  - `/channel/image/<xmlid>/<field>.png` → `content_image()` in `controllers/main.py`
  - `/channel/image/<xmlid>/<field>/<int:width>x<int:height>.png` → `content_image()` in `controllers/main.py`
  - `/channel/image/<model>/<id>/<field>.png` → `content_image()` in `controllers/main.py`
  - `/channel/image/<model>/<id>/<field>/<int:width>x<int:height>.png` → `content_image()` in `controllers/main.py`
  - `/channel/image/<model>/<id>/<field>/<string:filename>.png` → `content_image()` in `controllers/main.py`
  - `/channel/image/<model>/<id>/<field>/<int:width>x<int:height>/<string:filename>.png` → `content_image()` in `controllers/main.py`
  - `/channel/image.jpg` → `content_image()` in `controllers/main.py`
  - `/channel/image/<xmlid>.jpg` → `content_image()` in `controllers/main.py`
  - `/channel/image/<xmlid>/<int:width>x<int:height>.jpg` → `content_image()` in `controllers/main.py`
  - `/channel/image/<xmlid>/<field>.jpg` → `content_image()` in `controllers/main.py`
  - `/channel/image/<xmlid>/<field>/<int:width>x<int:height>.jpg` → `content_image()` in `controllers/main.py`
  - `/channel/image/<model>/<id>/<field>.jpg` → `content_image()` in `controllers/main.py`
  - `/channel/image/<model>/<id>/<field>/<int:width>x<int:height>.jpg` → `content_image()` in `controllers/main.py`
  - `/channel/image/<model>/<id>/<field>/<string:filename>.jpg` → `content_image()` in `controllers/main.py`
  - `/channel/image/<model>/<id>/<field>/<int:width>x<int:height>/<string:filename>.jpg` → `content_image()` in `controllers/main.py`
  - `/multichannel/<string:object>/webhook/<string:channel_id>` → `import_common_webhook()` in `controllers/webhooks.py`
  - `/multichannel/<string:type>/order/webhook/<string:channel_id>` → `import_order_webhook()` in `controllers/webhooks.py`
- **Menu declarations:** `Category`, `Product`, `Order`, `Partner`, `Shipping`, `Multi-Channel`, `Dashboard`, `Channels`, `Feeds`, `Mappings`, `Miscellaneous`, `Configuration`, `Global Configuration`, `Shipping`, `Product Template`, `Synchronization History`, `Payment Method`, `Currency`, `Attribute Value`, `Attribute` …
- **View architectures detected:** field: 2, form: 29, kanban: 1, list: 21, pivot: 11, search: 19, xpath: 6
- **ACL entries:** `channel.synchronization` (group `base.group_user/1/0/0`), `channel.synchronization` (group `odoo_multi_channel_sale.group_multi_channel_user/1/1/1`), `channel.synchronization` (group `odoo_multi_channel_sale.group_multi_channel_admin/1/1/1`), `extra.categories` (group `odoo_multi_channel_sale.group_multi_channel_admin/1/1/1`), `extra.categories` (group `odoo_multi_channel_sale.group_multi_channel_user/1/1/1`), `extra.categories` (group `base.group_user/1/0/0`), `multi.channel.sale` (group `base.group_user/1/0/0`), `multi.channel.sale` (group `odoo_multi_channel_sale.group_multi_channel_user/1/1/1`), `multi.channel.sale` (group `odoo_multi_channel_sale.group_multi_channel_admin/1/1/1`), `channel.order.states` (group `base.group_user/1/0/0`), `channel.order.states` (group `odoo_multi_channel_sale.group_multi_channel_user/1/1/1`), `channel.order.states` (group `odoo_multi_channel_sale.group_multi_channel_admin/1/1/1`), `multi.channel.skeleton` (group `base.group_user/1/0/0`), `multi.channel.skeleton` (group `odoo_multi_channel_sale.group_multi_channel_user/1/1/1`), `multi.channel.skeleton` (group `odoo_multi_channel_sale.group_multi_channel_admin/1/1/1`), `access_channel_mappings` (group `base.group_user/1/0/0`), `channel.account.mappings` (group `base.group_user/1/0/0`), `channel.account.mappings` (group `odoo_multi_channel_sale.group_multi_channel_user/1/1/1`), `channel.account.mappings` (group `odoo_multi_channel_sale.group_multi_channel_admin/1/1/1`), `channel.account.journal.mappings` (group `base.group_user/1/0/0`) …
- **Functional file groups:** Wizards: `wizard/feed_wizard.py`, `wizard/update_mapping_wizard.xml`, `wizard/update_mapping_wizard.py`, `wizard/wizard_message_view.xml`, `wizard/imports/import_partner.py`, `wizard/imports/__init__.py`, `wizard/imports/import_product.py`, `wizard/imports/import_operation.xml` …; Controllers: `controllers/backend.py`, `controllers/main.py`, `controllers/__init__.py`, `controllers/webhooks.py`; Security: `security/ir.model.access.csv`, `security/security.xml`; Data: `data/export_action.xml`, `data/data.xml`, `data/evaluation_action.xml`, `data/update_mapping_action.xml`, `data/cron.xml`; Views: `views/feeds/category_feed.xml`, `views/feeds/variant_feed.xml`, `views/feeds/product_feed.xml`, `views/feeds/order_feed.xml`, `views/feeds/order_line_feed.xml`, `views/feeds/partner_feed.xml`, `views/feeds/shipping_feed.xml`, `views/menus.xml` …
- **Tests present:** `tests/common.py`, `tests/test_feeds.py`, `tests/__init__.py`, `tests/test_connections.py`, `tests/test_mappings.py`
- **Implemented development-batch changes:** Batch 01: replaced unsafe eval parsing, allowlisted dashboard filters/table identifiers, parameterized SQL values, company-scoped dashboard data and channel checks.

### ODOO18 / `odoo_salla_integration` — Salla Odoo Connector | Odoo Multichannel

- **Manifest version:** `2.0.4`  
- **Summary:** 
                            Odoo Salla Connectors integrates your Odoo with salla to make 
                            the shopping experience seamless. The module allows you to 
                            sync products, categories, and sync orders to Odoo so that 
                            you can efficiently manage.
                            Multichannel is also compatible with these webkul apps
                            Amazon Connector Ebay Connector Magento Connector Woocommerce
                            Connector Shopify Connector Shopware Connector Walmart Wix Connector
                            Connector Prestashop Connector flipkart connector odoo Apps
                            Ecommerce Connectors for salla multi-channel salla webkul connectors
                              
- **Category / license / author:** `eCommerce` / `Other proprietary` / `Webkul Software Pvt. Ltd.`  
- **Dependencies:** `odoo_multi_channel_sale`, `l10n_sa_edi`  
- **Source inventory:** 79 files; 31 Python, 9 XML, 0 JavaScript, 0 SCSS; 7 test files.  
- **Python classes / models:**
  - `TestSallaAdjust` — `tests/test_salla_adjust.py`; methods: `setUp()`, `test_lower_salla_total_gives_a_refunded_credit_note()`, `test_higher_salla_total_gives_a_paid_invoice()`, `test_every_cent_is_reached()`, `test_zero_rated_order_is_adjusted_without_vat()`, `test_mixed_vat_invoice_is_rebuilt()`, `test_locked_order_is_adjusted_and_locked_again()`, `test_audit_brings_totals_to_salla()`, `test_blocked_journal_parameters_are_accepted()`, `test_rebuild_posts_its_credit_note_with_zero_tax_on_the_untaxed_line()`, `test_lowering_credit_note_has_positive_quantity_and_price()`, `test_zatca_price_of_a_switched_credit_note_line_is_positive()` …
  - `FakeSallaApi` — `tests/test_salla_audit.py`; methods: `salla_response()` …
  - `TestSallaAudit` — `tests/test_salla_audit.py`; methods: `setUp()`, `test_list_and_compare()`, `test_compare_again_after_a_fix()`, `test_invoice_and_pay()`, `test_cancelled_in_both_is_ok()`, `test_untaxed_order_is_invoiced_with_the_zero_tax()`, `test_numbered_draft_is_replaced_by_a_new_invoice()`, `test_invoice_date_is_the_local_day_of_the_order()`, `test_currency_rounding_and_credited_returns_are_ok()`, `test_status_mismatch_is_imported_again()`, `test_zero_residual_invoice_counts_as_paid()`, `test_invoiced_net_is_compared_and_returned_totals_ignored()` …
  - `TestSallaRefunds` — `tests/test_salla_refunds.py`; methods: `setUp()`, `test_refund_paid_invoice_pays_the_money_back()`, `test_refund_unpaid_invoice_closes_it()`, `test_restored_feed_action_creates_the_credit_note()`, `test_existing_order_is_mapped_not_created_again()`, `test_duplicate_order_is_cancelled_with_its_payment_and_invoice()`, `test_paid_twin_is_kept_and_takes_the_mapping()`, `test_unpaid_invoice_twin_is_kept_when_the_mapped_order_has_none()`, `test_unpaid_duplicate_invoice_is_reversed_when_the_kept_order_is_paid()`, `test_untaxed_duplicate_invoice_is_reversed_with_the_zero_tax()`, `test_untaxed_paid_invoice_is_refunded_with_the_zero_tax()`, `test_live_copy_of_a_cancelled_order_is_refunded_and_cancelled()` …
  - `TestSallaZeroTax` — `tests/test_salla_zero_tax.py`; methods: `setUp()`, `test_lines_without_tax_get_the_channel_zero_tax()`, `test_lines_with_tax_are_untouched()`, `test_without_setting_nothing_changes()`, `test_other_channels_are_untouched()`
  - `FakeSweepApi` — `tests/test_salla_order_totals.py`; methods: `salla_response()` …
  - `TestSallaOrderTotals` — `tests/test_salla_order_totals.py`; methods: `setUp()`, `test_feed_total()`, `test_coupon_added_after_the_import_is_on_the_first_invoice()`, `test_coupon_removed_after_the_import_raises_the_first_invoice()`, `test_order_like_its_feed_is_not_touched()`, `test_total_read_by_the_sweep_wins()`, `test_mixed_vat_order_is_left_to_the_daily_check()`, `test_adjustment_follows_salla_until_the_invoice()`, `test_sweep_reimports_status_and_total_changes_of_the_last_days()` …
  - `TestSallaProductMatching` — `tests/test_product_matching.py`; methods: `setUp()`, `test_matching_archived_product_has_no_side_effect()`, `test_evaluate_rejects_archived_duplicate_combination_cleanly()` …
  - `ExportCategory` extends `export.categories` — `wizard/export_operation.py`; methods: `export_salla_categories()`
  - `ExportCategory` extends `export.templates` — `wizard/export_operation.py`; methods: `export_salla_templates()`
  - `ImportOperation` extends `import.operation` — `wizard/import_operation.py`; fields: `salla_filter_type:Selection`, `salla_object_id:Char`, `salla_from_date:Datetime`, `salla_to_date:Datetime`, `salla_enable_keyword:Boolean`, `salla_product_keyword:Char`, `salla_skip_product_images:Boolean`, `salla_order_status:Selection`; methods: `import_with_filter()`, `salla_get_filter()`
  - `OdooSallaConnector` — `controllers/main.py`; methods: `odoo_salla_connector()`, `client_salla_connected()`
  - `MultiChannelSale` extends `multi.channel.sale` — `models/salla_adjust.py`; methods: `salla_report_missing_einvoices()` …
  - `SallaOrderBackfill` (`_name = salla.order.backfill`) — `models/salla_backfill.py`; fields: `name:Char`, `channel_id:Many2one`, `date_from:Date`, `date_to:Date`, `state:Selection`, `order_ids_json:Text`, `failed_ids_json:Text`, `total_count:Integer`, `done_count:Integer`, `remaining_count:Integer`, `failed_count:Integer`, `failed_ids_display:Text`, `progress:Float`, `last_run:Datetime`, `last_error:Text`; methods: `action_start()`, `action_retry_failed()`, `action_reset()`, `action_run_now()`, `cron_process()` …
  - `MultiChannelSale` extends `multi.channel.sale` — `models/multi_channel_webhook.py`; fields: `create_order_webhook_secret:Char`, `update_order_webhook_secret:Char`; methods: `unsubscribe_active_event()`, `activate_salla_order_webhook()`, `deactivate_salla_order_webhook()`, `salla_order_webhook_data()`, `salla_webhook_create_product_data()`, `salla_webhook_update_product_data()`, `create_update_product()`, `salla_webhook_delete_product_data()`, `salla_webhook_create_customer_data()`, `salla_webhook_update_customer_data()`, `create_update_customer()`, `salla_webhook_create_category_data()` …
  - `FetchData` — `models/fetch_data.py`; methods: `get_all_categories()`, `category_for_category()`, `get_shipping_vals()`, `process_customer()`, `process_address()`, `import_product_vals()`, `get_product_basic_vals()`, `get_variant_vals()`, `get_product_options()`, `process_order()`, `get_other_line()`, `get_discount_line()` …
  - `MultiChannelSale` extends `multi.channel.sale` — `models/salla_refunds.py`; methods: `salla_credit_orders()`, `salla_credit_invoices()`, `salla_refund_restored_orders()`, `salla_cancel_duplicate_orders()` …
  - `MultiChannelSaleConnectorStatus` extends `multi.channel.sale` — `models/connector_status.py`; fields: `connector_status_html:Html`, `connector_health_banner:Char`; methods: `_compute_connector_status_html()`, `_cron_is_active()`, `_mapped_order_states()`, `_missing_reverse_sync_states()`, `_missing_recommended_order_states()`, `_line()`, `_salla_connector_feature_lines()`, `_render_salla_connector_status_html()`
  - `WkFeed` extends `wk.feed` — `models/inherit_feed.py`; methods: `required_field_not_filled()`, `get_categ_id()`
  - `OrderFeed` extends `order.feed` — `models/order_feed.py`; methods: `import_order()`
  - `OrderFeed` extends `order.feed` — `models/inherit_order_feed.py`; methods: `import_order()`, `get_taxes_ids()` …
  - `MultiChannelSkeleton` extends `multi.channel.skeleton` — `models/inherit_order_feed.py`; methods: `SetOrderPaid()` …
  - `MultiChannelSale` extends `multi.channel.sale` — `models/salla_repair.py`; methods: `salla_repair_zero_tax_invoices()`, `salla_cancel_unlinked_payments()`, `salla_fix_dates()` …
  - `MultiChannelSale` extends `multi.channel.sale` — `models/multi_channel_sale.py`; fields: `salla_client_id:Char`, `salla_client_secret:Char`, `salla_redirect_url:Char`, `refresh_token:Char`, `access_token:Char`, `salla_token_expiry:Datetime`, `salla_verification_key:Char`, `salla_store_name:Char`, `salla_store_id:Char`, `salla_zero_tax_id:Many2one`, `import_under_review_order_cron:Boolean`; methods: `get_verification_key()`, `get_redirect_url()`, `salla_available_configs()`, `validate_vefication_key()`, `create()`, `write()`, `get_core_feature_compatible_channels()`, `get_channel()`, `get_info_urls()`, `get_sallaApi()`, `get_store_info()`, `create_salla_connection()` …
  - `ChannelOrderMappings` extends `channel.order.mappings` — `models/inherit_order_mapping.py`; fields: `salla_last_resync_at:Datetime`
  - `SallaApi` — `models/sallaAPI.py`; methods: `fetch_data()`, `get_headers()`, `salla_pagination()`, `salla_response()`, `get_categories()`, `get_shippings()`, `get_partners()`, `get_products()`, `get_order_status()`, `get_orders()`, `post_category()`, `post_category_data()` …
  - `SallaOrderAudit` (`_name = salla.order.audit`) — `models/salla_audit.py`; fields: `name:Char`, `channel_id:Many2one`, `date_from:Date`, `date_to:Date`, `state:Selection`, `next_page:Integer`, `window_start:Date`, `line_ids:One2many`, `line_count:Integer`, `problem_count:Integer`, `compared_count:Integer`, `summary:Text`, `last_run:Datetime`, `last_error:Text`, `backfill_id:Many2one`; methods: `action_start()`, `action_compare_again()`, `action_run_now()`, `action_open_lines()`, `action_import_problems()`, `cron_process()`, `action_fix_invoices()`, `action_adjust_totals()` …
  - `SallaOrderAuditLine` (`_name = salla.order.audit.line`) — `models/salla_audit.py`; fields: `audit_id:Many2one`, `store_id:Char`, `reference:Char`, `order_date:Date`, `order_datetime:Char`, `status:Char`, `status_name:Char`, `total:Float`, `total_known:Boolean`, `currency:Char`, `payment_method:Char`, `checked:Boolean`, `order_id:Many2one`, `order_count:Integer`, `odoo_status:Char`, `odoo_total:Float`, `total_diff:Float`, `invoice_state:Selection` …; methods: `_compute_total_diff()`
  - `InheritWkFeed` extends `wk.feed` — `models/inherit_product.py`; methods: `get_product_fields()`, `required_field_not_filled()`, `get_product_id()`
  - `MultiChannelSale` extends `multi.channel.sale` — `models/inherit_product.py`; methods: `match_odoo_template()`, `match_odoo_product()`, `action_salla_product_dedup_diagnostics()` …
  - `ProductVariantFeed` extends `product.feed` — `models/inherit_product.py`; fields: `salla_product_attribute_options:Char`
  - `ProductProduct` extends `product.template` — `models/inherit_product.py`; fields: `salla_product_attribute_options:Char`
  - `AccountEdiXmlUbl21Zatca` extends `account.edi.xml.ubl_21.zatca` — `models/zatca_xml.py`; methods: `_get_invoice_line_price_vals()`
- **HTTP routes:**
  - `/salla/authenticate` → `odoo_salla_connector()` in `controllers/main.py`
- **Menu declarations:** `Salla Order Audit`, `Salla Order Backfill`
- **View architectures detected:** form: 2, list: 3, pivot: 1, search: 1, xpath: 5
- **ACL entries:** `salla.order.backfill user` (group `odoo_multi_channel_sale.group_multi_channel_user/1/1/1`), `salla.order.backfill admin` (group `odoo_multi_channel_sale.group_multi_channel_admin/1/1/1`), `salla.order.audit user` (group `odoo_multi_channel_sale.group_multi_channel_user/1/1/1`), `salla.order.audit admin` (group `odoo_multi_channel_sale.group_multi_channel_admin/1/1/1`), `salla.order.audit.line user` (group `odoo_multi_channel_sale.group_multi_channel_user/1/1/1`), `salla.order.audit.line admin` (group `odoo_multi_channel_sale.group_multi_channel_admin/1/1/1`)
- **Functional file groups:** Wizards: `wizard/export_operation.py`, `wizard/__init__.py`, `wizard/import_operation.xml`, `wizard/import_operation.py`, `wizard/export_operation.xml`; Controllers: `controllers/main.py`, `controllers/__init__.py`; Security: `security/ir.model.access.csv`; Data: `data/data.xml`, `data/cron.xml`, `data/server_actions.xml`; Views: `views/salla_audit_views.xml`, `views/salla_backfill_views.xml`, `views/multi_channel_sale.xml`
- **Tests present:** `tests/test_salla_adjust.py`, `tests/test_salla_audit.py`, `tests/test_salla_refunds.py`, `tests/test_salla_zero_tax.py`, `tests/test_salla_order_totals.py`, `tests/__init__.py`, `tests/test_product_matching.py`
- **Implemented development-batch changes:** Batch 01: replaced unsafe eval parsing of stored option/variant values with ast.literal_eval.

### ODOO18 / `pdf_print_preview` — Pdf Print Preview

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Preview and print PDF report in your browser | Pdf direct preview | Print without Download  
- **Category / license / author:** `not declared` / `OPL-1` / `Ibrahim Elmasry`  
- **Dependencies:** `web`  
- **Source inventory:** 408 files; 8 Python, 7 XML, 7 JavaScript, 2 SCSS; 0 test files.  
- **Python classes / models:**
  - `PrintPreviewController` — `controllers/main.py`; methods: `get_report_name()`
  - `IrHttp` extends `ir.http` — `models/ir_http.py`; methods: `session_info()`
  - `ResUsers` extends `res.users` — `models/res_users.py`; fields: `preview_print:Boolean`, `automatic_printing:Boolean`; methods: `preview_reload()`, `preview_print_save()` …
  - `IrActionsReport` extends `ir.actions.report` — `models/ir_actions_report.py`; methods: `_render_qweb_pdf()`
- **HTTP routes:**
  - `/pdf_print_preview/get_report_name` → `get_report_name()` in `controllers/main.py`
- **View architectures detected:** form: 1, xpath: 1
- **Functional file groups:** Reports: `report/ir_actions_report_templates.xml`, `report/ir_actions_report.xml`; Controllers: `controllers/main.py`, `controllers/__init__.py`; Views: `views/assets.xml`, `views/res_users.xml`
- **Tests present:** No test files detected in the addon archive.
- **Implemented development-batch changes:** Batch 01: stopped exposing traceback details in generated error PDFs; technical errors are logged server-side.

### ODOO18 / `pos_cashier_handover` — POS Cashier Handover Report

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** طباعة تسليم الخزينة عند إغلاق جلسة نقطة البيع  
- **Category / license / author:** `Point of Sale` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `point_of_sale`  
- **Source inventory:** 10 files; 4 Python, 3 XML, 1 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `PosSession` extends `pos.session` — `models/pos_session.py`; methods: `action_print_cashier_handover()` …
- **Functional file groups:** Reports: `report/report_cashier_handover_template.xml`, `report/report_cashier_handover.xml`; Security: `security/ir.model.access.csv`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `pos_get_weight_button` — POS Get Weight Button

- **Manifest version:** `1.0`  
- **Summary:** Adds a Get Weight button to POS control buttons  
- **Category / license / author:** `Sales/Point of Sale` / `LGPL-3` / `not declared`  
- **Dependencies:** `point_of_sale`  
- **Source inventory:** 4 files; 2 Python, 1 XML, 1 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:** No model/class declarations detected by the static extractor; inspect source files for dynamic definitions.
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `pos_receipt_price_before_discount` — POS Receipt: Price Before Discount

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Show product list price (before discount) under each receipt line when discounted  
- **Category / license / author:** `Point of Sale` / `LGPL-3` / `not declared`  
- **Dependencies:** `point_of_sale`  
- **Source inventory:** 5 files; 2 Python, 1 XML, 1 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:** No model/class declarations detected by the static extractor; inspect source files for dynamic definitions.
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `pos_refund_restriction` — POS Refund Restriction

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Restrict refund operations in POS to administrators only  
- **Category / license / author:** `Sales/Point of Sale` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `point_of_sale`  
- **Source inventory:** 3 files; 2 Python, 0 XML, 1 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:** No model/class declarations detected by the static extractor; inspect source files for dynamic definitions.
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `pos_restrict` — POS User Restrict

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Restricts User access to pos and orders.  
- **Category / license / author:** `Point of Sale` / `AGPL-3` / `Cybrosys Techno Solutions`  
- **Dependencies:** `point_of_sale`  
- **Source inventory:** 93 files; 5 Python, 2 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ResUsers` extends `res.users` — `models/res_users.py`; fields: `allowed_pos:Many2many`, `show_users:Boolean`
  - `PosConfig` extends `pos.config` — `models/pos_config.py`; fields: `users_allowed:Many2many`; methods: `_compute_users_allowed()`
- **View architectures detected:** field: 1, xpath: 1
- **Record rules:** `Config User`, `Config Manager`, `Orders User`, `Orders Manager`
- **Functional file groups:** Security: `security/pos_restrict_groups.xml`; Views: `views/res_users_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `product_movement_report` — Product Movement Lifecycle Report

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Full movement history of a product/lot from first receipt until fully sold  
- **Category / license / author:** `Inventory/Reporting` / `LGPL-3` / `not declared`  
- **Dependencies:** `stock`  
- **Source inventory:** 9 files; 6 Python, 2 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ProductMovementWizard` (`_name = product.movement.wizard`) — `wizard/product_movement_wizard.py`; fields: `product_id:Many2one`, `lot_id:Many2one`, `date_from:Date`, `date_to:Date`, `line_ids:One2many`, `summary_ids:One2many`, `company_id:Many2one`, `currency_id:Many2one`, `sales_revenue:Float`, `sales_cogs:Float`, `margin:Float`, `margin_pct:Float`; methods: `action_show()`, `action_print()`, `get_move_type_label()` …
  - `ProductMovementLine` (`_name = product.movement.line`) — `models/product_movement_line.py`; fields: `wizard_id:Many2one`, `sequence:Integer`, `cycle_no:Integer`, `is_sold_out:Boolean`, `date:Datetime`, `reference:Char`, `picking_id:Many2one`, `origin:Char`, `move_type:Selection`, `location_id:Many2one`, `location_dest_id:Many2one`, `partner_id:Many2one`, `lot_id:Many2one`, `user_id:Many2one`, `qty_in:Float`, `qty_out:Float`, `balance:Float`, `cost:Float` …
  - `ProductMovementSummary` (`_name = product.movement.summary`) — `models/product_movement_line.py`; fields: `wizard_id:Many2one`, `sequence:Integer`, `group:Selection`, `name:Char`, `qty:Float`, `cost:Float`, `is_bold:Boolean`
- **Menu declarations:** `Product Movement Lifecycle`
- **View architectures detected:** form: 2, list: 2, search: 1
- **ACL entries:** `product.movement.line` (group `base.group_user/1/1/1`), `product.movement.wizard` (group `base.group_user/1/1/1`), `product.movement.summary` (group `base.group_user/1/1/1`)
- **Functional file groups:** Wizards: `wizard/product_movement_wizard.py`, `wizard/__init__.py`; Reports: `report/product_movement_report.xml`; Security: `security/ir.model.access.csv`; Views: `views/product_movement_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `prt_report_attachment_preview` — Open PDF Reports and PDF Attachments in Browser

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** 
    Preview reports and pdf attachments in browser instead of downloading them.
    Open Report or PDF Attachment in new tab instead of downloading.
  
- **Category / license / author:** `Productivity` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `web`  
- **Source inventory:** 16 files; 6 Python, 0 XML, 2 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestCxReportController` — `tests/test_cx_report_controller.py`; methods: `setUpClass()`, `test_get_extra_context_for_single_record()`, `test_compose_report_file_name()`
  - `CxReportController` — `controllers/report.py`; methods: `report_routes()`, `check_wkhtmltopdf()` …
- **HTTP routes:**
  - `/report/<converter>/<reportname>` → `report_routes()` in `controllers/report.py`
  - `/report/<converter>/<reportname>/<docids>` → `report_routes()` in `controllers/report.py`
  - `/report/check_wkhtmltopdf` → `check_wkhtmltopdf()` in `controllers/report.py`
- **Functional file groups:** Controllers: `controllers/report.py`, `controllers/__init__.py`
- **Tests present:** `tests/test_cx_report_controller.py`, `tests/__init__.py`

### ODOO18 / `sale_barcode_scanner` — Sale Order Barcode Scanner

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Scan products by Barcode/QRCode in sales orders using mobile camera or webcam  
- **Category / license / author:** `Sales` / `LGPL-3` / `Mohamed Helmy`  
- **Dependencies:** `sale_management`, `product`, `barcodes`  
- **Source inventory:** 17 files; 4 Python, 2 XML, 2 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; methods: `action_open_barcode_scanner()`, `add_product_by_barcode()`
- **View architectures detected:** xpath: 1
- **ACL entries:** `access_sale_order_barcode` (group `sales_team.group_sale_salesman/1/1/1`), `access_sale_order_line_barcode` (group `sales_team.group_sale_salesman/1/1/1`), `access_product_product_barcode` (group `sales_team.group_sale_salesman/1/0/0`)
- **Functional file groups:** Security: `security/ir.model.access.csv`; Views: `views/sale_order_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `sale_contract_auto` — Sale Contract Auto

- **Manifest version:** `1.0`  
- **Summary:** Automatically generate contracts from sale orders  
- **Category / license / author:** `Sales` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `sale_management`, `account`, `portal`, `mail`  
- **Source inventory:** 28 files; 15 Python, 10 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ContractPortal` — `controllers/controllers.py`; methods: `view_contract()`, `sign_contract()`
  - `ContractTemplate` (`_name = contract.template`) extends `mail.thread`, `mail.activity.mixin` — `models/contract_template.py`; fields: `name:Char`, `content:Html`
  - `SaleContractLine` (`_name = sale.contract.line`) — `models/sale_contract_line.py`; fields: `contract_id:Many2one`, `product_id:Many2one`, `name:Char`, `quantity:Float`, `price_unit:Monetary`, `price_subtotal:Monetary`, `currency_id:Many2one`; methods: `_compute_subtotal()`
  - `ContractDocument` (`_name = contract.document`) — `models/contract_document.py`; fields: `contract_id:Many2one`, `name:Char`, `required:Boolean`, `document_type:Selection`, `attachment_id:Many2one`, `uploaded:Boolean`, `notes:Text`; methods: `_compute_uploaded()`
  - `ContractTitle` (`_name = sale.contract.title`) — `models/contract_title.py`; fields: `name:Char`
  - `ContractAmendment` (`_name = contract.amendment`) — `models/contract_amendment.py`; fields: `contract_id:Many2one`, `name:Char`, `date:Date`, `description:Text`, `previous_value:Text`, `new_value:Text`, `user_id:Many2one`; methods: `create()`
  - `AccountMove` extends `account.move` — `models/account_move.py`; fields: `contract_id:Many2one`
  - `ContractClause` (`_name = contract.clause`) — `models/contract_clause.py`; fields: `name:Char`, `clause_type:Selection`, `content:Html`, `active:Boolean`, `notes:Text`
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; fields: `contract_count:Integer`, `contract_template_id:Many2one`, `contract_id:Many2one`, `contract_title_name:Many2one`; methods: `action_view_contract()`, `action_confirm()` …
  - `ResPartner` extends `res.partner` — `models/sale_order.py`; fields: `card_id:Char`; methods: `_check_code()`
  - `SaleContract` (`_name = sale.contract`) extends `mail.thread`, `portal.mixin` — `models/sale_contract.py`; fields: `name:Char`, `partner_id:Many2one`, `sale_order_id:Many2one`, `contract_date:Date`, `amount_total:Monetary`, `currency_id:Many2one`, `agreement_terms:Text`, `contract_line_ids:One2many`, `contract_title_name:Many2one`, `contract_template_id:Many2one`, `state:Selection`, `first_party_name:Char`, `first_party_registry:Char`, `first_party_address:Char`, `second_party_name:Char`, `second_party_address:Char`, `second_party_id_card:Char`, `first_party_signature:Binary` …; methods: `create()`, `write()`, `action_set_active()`, `action_financial_approve()`, `action_legal_approve()`, `action_finish()`, `action_cancel()`, `action_reset_to_draft()`, `get_portal_url()`, `print_contract_report()`, `action_send_contract_link()`, `get_arabic_date()` …
  - `ContractPaymentSchedule` (`_name = contract.payment.schedule`) — `models/payment_schedule.py`; fields: `contract_id:Many2one`, `installment_number:Integer`, `amount:Monetary`, `currency_id:Many2one`, `due_date:Date`, `invoice_id:Many2one`, `state:Selection`; methods: `action_create_installment_invoice()`, `open_invoice()` …
- **HTTP routes:**
  - `/my/contracts/<int:contract_id>` → `view_contract()` in `controllers/controllers.py`
  - `/my/contracts/<int:contract_id>/sign` → `sign_contract()` in `controllers/controllers.py`
- **Menu declarations:** `Contracts`, `Contracts`, `Contract Titles`, `Customers`, `Contract Templates`
- **View architectures detected:** form: 3, kanban: 1, list: 3, xpath: 3
- **ACL entries:** `sale.contract.user` (group `base.group_user/1/0/0`), `sale.contract.manager` (group `sales_team.group_sale_manager/1/1/1`), `sale.contract.account.manager` (group `account.group_account_manager/1/1/1`), `sale.contract.portal` (group `base.group_portal/1/1/0`), `sale.contract.line.user` (group `base.group_user/1/0/0`), `sale.contract.line.manager` (group `sales_team.group_sale_manager/1/1/1`), `sale.contract.line.account.manager` (group `account.group_account_manager/1/1/1`), `contract.template.user` (group `base.group_user/1/0/0`), `contract.template.manager` (group `sales_team.group_sale_manager/1/1/1`), `sale.contract.title` (group `/1/1/1`)
- **Functional file groups:** Reports: `report/contract_report.xml`, `report/contract_print_template.xml`; Controllers: `controllers/controllers.py`, `controllers/__init__.py`; Security: `security/ir.model.access.csv`; Data: `data/mail_templates.xml`, `data/contract_data.xml`; Views: `views/sale_contract_views.xml`, `views/ir_sequence.xml`, `views/contract_template_views.xml`, `views/res_partner_view.xml`, `views/templates.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `sale_kitchen_receipt` — Kitchen Receipt from Quotation

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Print kitchen receipt from sales quotation  
- **Category / license / author:** `Sales/Sales` / `LGPL-3` / `Your Company`  
- **Dependencies:** `sale`, `account`  
- **Source inventory:** 6 files; 4 Python, 2 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; fields: `x_building_floor:Char`, `x_landmark:Char`, `x_driver_name:Char`
- **View architectures detected:** xpath: 2
- **Functional file groups:** Views: `views/sale_order_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `sale_order_automation` — Sale Order Automation

- **Manifest version:** `1.1`  
- **Summary:** Enable auto sale workflow with sale order confirmation. Include operations like Auto Create Invoice, Auto Validate Invoice and Auto Transfer Delivery Order.  
- **Category / license / author:** `not declared` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `sale_stock`  
- **Source inventory:** 13 files; 5 Python, 1 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `StockWarehouse` extends `stock.warehouse` — `models/warehouse.py`; fields: `is_delivery_set_to_done:Boolean`, `create_invoice:Boolean`, `validate_invoice:Boolean`
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; methods: `action_confirm()`
- **View architectures detected:** field: 1
- **Functional file groups:** Views: `views/stock_warehouse.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `sale_order_contract` — Sale Order Contract

- **Manifest version:** `0.1`  
- **Summary:** Automatically generate contracts from sale orders.  
- **Category / license / author:** `Sales` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `sale`, `account`  
- **Source inventory:** 8 files; 2 Python, 3 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:** No model/class declarations detected by the static extractor; inspect source files for dynamic definitions.
- **Functional file groups:** Reports: `report/contract_report.xml`, `report/contract_print_template.xml`, `report/paperformat.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `sale_order_contract_terms` — Sales Order Contract Terms (AR/EN) - 4 Pages

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Separate Sales Order report with bilingual contract terms (4 pages, AR/EN).  
- **Category / license / author:** `Sales` / `LGPL-3` / `not declared`  
- **Dependencies:** `sale`  
- **Source inventory:** 11 files; 6 Python, 3 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ResPartner` extends `res.partner` — `models/partner_company_fields.py`; fields: `x_id_no:Char`
  - `ResCompany` extends `res.company` — `models/partner_company_fields.py`; fields: `x_establishment_registration:Char`, `x_represented_by:Char`, `x_representative_id_no:Char`, `x_po_box:Char`
  - `ProductTemplate` extends `product.template` — `models/product_template.py`; fields: `technical_specification:Text`
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; fields: `technical_specification_id:Text`; methods: `get_date_arabic()` …
  - `SaleOrderContractTerms` extends `sale.order.line` — `models/sale_order.py`; fields: `technical_specification_id:Text`
- **View architectures detected:** xpath: 2
- **ACL entries:** `res.partner.contract.terms` (group `base.group_user/1/1/1`), `res.company.contract.terms` (group `base.group_user/1/1/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`; Views: `views/report_actions.xml`, `views/report_templates.xml`, `views/product_template_view.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `sale_stock_restrict` — Sale Stock Restrict

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Module helps to restrict out of stock products  
- **Category / license / author:** `Sales` / `AGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `sale_management`, `stock`, `account`  
- **Source inventory:** 11 files; 5 Python, 2 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ResConfigSettings` extends `res.config.settings` — `models/res_config_settings.py`; fields: `product_restriction:Boolean`, `check_stock:Selection`; methods: `get_values()`, `set_values()`
  - `SaleOrderLine` extends `sale.order.line` — `models/sale_order.py`; fields: `qty_available:Float`, `forecast_quantity:Float`; methods: `_onchange_product_id()`
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; fields: `onhand_check:Boolean`, `forecast_check:Boolean`; methods: `action_confirm()`
- **View architectures detected:** xpath: 2
- **Functional file groups:** Views: `views/sale_order.xml`, `views/res_config_settings_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `sales_credit_limit` — Customer Credit Limit with Due Amount Warning

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** An advanced way to handle customer credit limit through warning and blocking stage.  
- **Category / license / author:** `Sales` / `OPL-1` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `sale_management`  
- **Source inventory:** 9 files; 4 Python, 1 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ResPartner` extends `res.partner` — `models/credit_limit_model.py`; fields: `active_limit:Boolean`, `warning_stage:Float`, `blocking_stage:Float`, `due_amount:Float`, `warning_stage_visible:Boolean`, `blocking_stage_visible:Boolean`; methods: `_compute_limit_visibility()`, `_compute_due_amount()`, `_check_warning_blocking()`
  - `SaleOrder` extends `sale.order` — `models/credit_limit_model.py`; fields: `has_due:Boolean`, `is_warning:Boolean`, `due_amount:Float`; methods: `action_confirm()` …
- **View architectures detected:** xpath: 2
- **Functional file groups:** Views: `views/credit_limit_view.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `stock_move_invoice` — Invoice From Stock Picking

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Create invoice for stock picking  
- **Category / license / author:** `Extra Tools` / `AGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `stock`, `account`  
- **Source inventory:** 18 files; 9 Python, 4 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `PickingInvoice` (`_name = picking.invoice`) — `wizard/picking_invoice.py`; methods: `action_picking_multi_invoice()`
  - `AccountMove` extends `account.move` — `models/account_move.py`; fields: `picking_id:Many2one`, `transfer_ids:Many2many`
  - `Settings` extends `res.config.settings` — `models/res_config_settings.py`; fields: `customer_journal_id:Many2one`, `vendor_journal_id:Many2one`
  - `StockPicking` extends `stock.picking` — `models/stock_picking.py`; fields: `invoice_count:Integer`, `operation_code:Selection`, `is_return:Boolean`; methods: `action_create_invoice()`, `action_create_bill()`, `action_create_customer_credit()`, `action_create_vendor_credit()`, `action_open_picking_invoice()`, `action_create_multi_invoice_for_multi_transfer()` …
  - `StockReturnInvoicePicking` extends `stock.return.picking` — `models/stock_return_picking.py`; methods: `_create_returns()`
- **View architectures detected:** form: 1, xpath: 3
- **ACL entries:** `access_picking_invoice_manager` (group `base.group_erp_manager/1/1/1`), `access_picking_invoice_user` (group `base.group_user/1/1/1`)
- **Functional file groups:** Wizards: `wizard/picking_invoice_views.xml`, `wizard/picking_invoice.py`, `wizard/__init__.py`; Security: `security/ir.model.access.csv`; Views: `views/stock_picking_views.xml`, `views/res_config_settings_views.xml`, `views/account_move_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `stock_split_transfer` — Stock Split Transfer

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Two-step internal transfers with per-user location visibility  
- **Category / license / author:** `Inventory/Warehouse` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `stock`  
- **Source inventory:** 7 files; 5 Python, 1 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ResUsers` extends `res.users` — `models/res_users.py`; fields: `allowed_location_ids:Many2many`; methods: `_get_self_readable_fields()`, `_get_self_writeable_fields()`
  - `StockPicking` extends `stock.picking` — `models/stock_picking.py`; fields: `split_parent_id:Many2one`, `split_child_id:Many2one`, `split_visible:Boolean`, `is_split_transfer:Boolean`; methods: `action_confirm()`, `button_validate()` …
- **View architectures detected:** xpath: 4
- **Functional file groups:** Views: `views/views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `transfer_wizard` — trade_paints_wizard

- **Manifest version:** `1.1`  
- **Summary:** 
        Transfer Wizard  
- **Category / license / author:** `Uncategorized` / `not declared` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `sale`, `sale_management`, `stock`, `purchase`  
- **Source inventory:** 7 files; 4 Python, 1 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `TransferWizard` (`_name = transfer.wizard`) — `wizard/transfer_wizard.py`; fields: `expected_weight:Float`, `driver_name:Many2one`, `car_number:Char`; methods: `validate()` …
  - `StockPicking` extends `stock.picking` — `wizard/transfer_wizard.py`; fields: `driver_name:Many2one`, `car_number:Char`, `printed_before:Boolean`
- **View architectures detected:** form: 1
- **ACL entries:** `transfer_wiard` (group `//1/1`)
- **Functional file groups:** Wizards: `wizard/transfer_wizard.xml`, `wizard/__init__.py`, `wizard/transfer_wizard.py`; Security: `security/ir.model.access.csv`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `whatsapp_mail_messaging` — Odoo Whatsapp Connector

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Odoo18 Whatsapp, Whatsapp Odoo Integration, Odoo Whatsapp Connector, 
     Odoo Whatsapp, Whatsapp Connector, Whatsapp Integration, Odoo18, Whatsapp,
     Odoo Apps  
- **Category / license / author:** `Extra Tools` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `sale`, `account`, `website`, `sale_management`  
- **Source inventory:** 139 files; 14 Python, 11 XML, 4 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `PortalShare` extends `portal.share` — `wizard/portal_share.py`; fields: `share_type:Selection`, `mobile_number:Char`, `partner_id:Many2one`; methods: `action_send_whatsapp()` …
  - `WhatsappSendMessage` (`_name = whatsapp.send.message`) — `wizard/whatsapp_send_message.py`; fields: `partner_id:Many2one`, `mobile:Char`, `message:Text`, `image_1920:Binary`; methods: `send_message()` …
  - `Website` extends `website` — `model/website.py`; fields: `mobile_number:Char`
  - `AccountMove` extends `account.move` — `model/account_move.py`; methods: `action_send_whatsapp()`, `check_customers()`, `action_whatsapp_multi()`
  - `ResCompany` extends `res.company` — `model/res_company.py`; fields: `whatsapp_message:Text`
  - `ResConfigSettings` extends `res.config.settings` — `model/res_config_settings.py`; fields: `whatsapp_message:Text`
  - `SaleOrder` extends `sale.order` — `model/sale_order.py`; methods: `action_send_whatsapp()`, `check_customers()`, `action_whatsapp_multi()`
  - `SelectionMessage` (`_name = selection.message`) — `model/selection_message.py`; fields: `name:Char`, `message:Text`
  - `SendMessage` — `controllers/whatsapp_mail_messaging.py`; methods: `whatsapp_message()`, `mobile_number()`
- **HTTP routes:**
  - `/whatsapp_message` → `whatsapp_message()` in `controllers/whatsapp_mail_messaging.py`
  - `/mobile_number` → `mobile_number()` in `controllers/whatsapp_mail_messaging.py`
- **Menu declarations:** `Whatsapp Messages`
- **View architectures detected:** form: 2, list: 1, xpath: 8
- **ACL entries:** `access.whatsapp.send.message.user` (group `base.group_user/1/1/1`), `access.selection.message.user` (group `base.group_user/1/1/1`)
- **Functional file groups:** Wizards: `wizard/portal_share_views.xml`, `wizard/portal_share.py`, `wizard/whatsapp_send_message.py`, `wizard/__init__.py`, `wizard/whatsapp_send_message_views.xml`; Controllers: `controllers/__init__.py`, `controllers/whatsapp_mail_messaging.py`; Security: `security/ir.model.access.csv`; Views: `views/sale_order_views.xml`, `views/website_templates.xml`, `views/selection_message_views.xml`, `views/res_company_views.xml`, `views/res_config_settings_views.xml`, `views/website_views.xml`, `views/account_move_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `wk_wizard_messages` — Webkul Message Wizard

- **Manifest version:** `1.0.0`  
- **Summary:** To show messages/warnings in Odoo  
- **Category / license / author:** `Extra Tools` / `Other proprietary` / `Webkul Software Pvt. Ltd.`  
- **Dependencies:** None declared  
- **Source inventory:** 17 files; 4 Python, 1 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `WkWizardMessage` (`_name = wk.wizard.message`) — `wizard/wizard_message.py`; fields: `text:Html`; methods: `genrated_message()`
- **View architectures detected:** form: 1
- **ACL entries:** `Access Message Wizard` (group `base.group_user/1/1/1`)
- **Functional file groups:** Wizards: `wizard/wizard_message.xml`, `wizard/wizard_message.py`, `wizard/__init__.py`; Security: `security/ir.model.access.csv`
- **Tests present:** No test files detected in the addon archive.

### ODOO18 / `wm_purchase_global_discount` — Purchase Order Global Discount (Same as Odoo Sales Discount)

- **Manifest version:** `1.0.0`  
- **Summary:** Purchase Order Global Discount (Same as Odoo Sales Discount)  
- **Category / license / author:** `Purchase` / `OPL-1` / `Ibrahim Elmasry`  
- **Dependencies:** `purchase`  
- **Source inventory:** 22 files; 7 Python, 2 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `SaleOrderDiscount` (`_name = purchase.order.discount`) — `wizard/purchase_order_discount.py`; fields: `purchase_order_id:Many2one`, `company_id:Many2one`, `currency_id:Many2one`, `discount_amount:Monetary`, `discount_percentage:Float`, `discount_type:Selection`; methods: `check_discount_amount()`, `prepare_discount_product_values()`, `prepare_discount_line_values()`, `create_discount_lines()`, `action_discount_apply()`
  - `PurchaseOrder` extends `purchase.order` — `models/purchase_order.py`; methods: `action_open_discount_wizard()`
  - `Company` extends `res.company` — `models/res_company.py`; fields: `purchase_discount_product_id:Many2one`
- **View architectures detected:** form: 1, xpath: 1
- **ACL entries:** `access_purchase_order_discount` (group `purchase.group_purchase_user/1/1/1`)
- **Functional file groups:** Wizards: `wizard/purchase_order_discount_views.xml`, `wizard/__init__.py`, `wizard/purchase_order_discount.py`; Security: `security/ir.model.access.csv`; Views: `views/purchase_order_view.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `account_invoice_fixed_discount` — Account Fixed Discount

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Allows to apply fixed amount discounts in invoices.  
- **Category / license / author:** `Accounting & Finance` / `AGPL-3` / `ForgeFlow, Odoo Community Association (OCA)`  
- **Dependencies:** `account`  
- **Source inventory:** 25 files; 7 Python, 3 XML, 0 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestInvoiceFixedDiscount` — `tests/test_account_fixed_discount.py`; methods: `setUpClass()`, `test_01_discounts_fixed_single_unit()`, `test_02_discounts_fixed_multiple_units()`, `test_03_discount_fixed_no_tax()`, `test_03_discount_fixed_no_unit_prise()`, `test_04_base_line_set_to_none()` …
  - `AccountMoveLine` extends `account.move.line` — `models/account_move_line.py`; fields: `discount_fixed:Monetary`; methods: `_compute_totals()`, `_onchange_discount_fixed()`, `_onchange_discount()`, `_get_discount_from_fixed_discount()`
  - `AccountTax` extends `account.tax` — `models/account_tax.py`; methods: `_prepare_base_line_for_taxes_computation()`
- **View architectures detected:** xpath: 1
- **Functional file groups:** Security: `security/res_groups.xml`; Views: `views/account_move_view.xml`
- **Tests present:** `tests/test_account_fixed_discount.py`, `tests/__init__.py`

### ODOO19 / `advanced_accounting_reports` — Advanced Accounting Reports

- **Manifest version:** `1.20.0`  
- **Summary:** Advanced General Ledger, Trial Balance with Analytic Dimensions & Multi-Currency  
- **Category / license / author:** `Accounting` / `LGPL-3` / `Woledge`  
- **Dependencies:** `account`, `account_reports`, `base`, `web`  
- **Source inventory:** 46 files; 21 Python, 17 XML, 1 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestAdvancedAccounting` — `tests/test_advanced_accounting.py`; methods: `setUp()`, `test_feature_creation()`, `test_cost_center_creation()`, `test_patch_number_creation()`, `test_feature_uniqueness()`, `test_move_line_dimensions()`, `test_manual_exchange_rate()`, `test_manual_rate_constraint()`, `test_general_ledger_wizard()`, `test_trial_balance_wizard()`
  - `GeneralLedgerReport` (`_name = report.advanced_accounting_reports.report_general_ledger`) — `report/general_ledger_report.py`; methods: `_get_report_values()`
  - `TrialBalanceReport` (`_name = report.advanced_accounting_reports.report_trial_balance`) — `report/trial_balance_report.py`; methods: `_get_report_values()`
  - `TrialBalanceWizard` (`_name = trial.balance.wizard`) — `wizard/trial_balance_wizard.py`; fields: `date_from:Date`, `date_to:Date`, `journal_ids:Many2many`, `account_ids:Many2many`, `feature_ids:Many2many`, `cost_center_ids:Many2many`, `target_move:Selection`, `company_id:Many2one`, `show_secondary_currency:Boolean`, `opening_balance:Monetary`, `ending_balance:Monetary`, `currency_id:Many2one`; methods: `action_view_report()`, `action_export_excel()`, `action_export_pdf()` …
  - `GeneralLedgerWizard` (`_name = general.ledger.wizard`) — `wizard/general_ledger_wizard.py`; fields: `date_from:Date`, `date_to:Date`, `journal_ids:Many2many`, `account_ids:Many2many`, `partner_ids:Many2many`, `feature_ids:Many2many`, `cost_center_ids:Many2many`, `target_move:Selection`, `company_id:Many2one`, `show_secondary_currency:Boolean`, `opening_balance:Monetary`, `ending_balance:Monetary`, `currency_id:Many2one`; methods: `action_view_report()`, `action_export_excel()`, `action_export_pdf()` …
  - `AdvancedAccountingController` — `controllers/main.py`; methods: `get_general_ledger_data()`
  - `XlsxExportController` — `controllers/xlsx_export.py`; methods: `export_general_ledger_xlsx()`, `export_trial_balance_xlsx()` …
  - `AccountMoveLine` extends `account.move.line` — `models/account_move_line.py`; fields: `feature_ids:Many2many`, `cost_center_ids:Many2many`, `secondary_debit:Monetary`, `secondary_credit:Monetary`, `secondary_balance:Monetary`, `secondary_currency_id:Many2one`, `manual_rate:Float`, `patch_number_id:Many2one`, `secondary_currency_name:Char`; methods: `fields_get()` …
  - `AccountPatchNumber` (`_name = account.patch.number`) — `models/account_patch_number.py`; fields: `name:Char`, `description:Text`, `status:Selection`, `company_id:Many2one`, `active:Boolean`; methods: `name_get()` …
  - `AccountMove` extends `account.move` — `models/account_move.py`; fields: `secondary_currency_id:Many2one`, `manual_rate:Float`, `use_manual_rate:Boolean`, `secondary_debit_total:Monetary`, `secondary_credit_total:Monetary`, `secondary_balance_total:Monetary`, `patch_number_id:Many2one`; methods: `fields_get()`, `default_get()` …
  - `ResCompany` extends `res.company` — `models/res_company.py`; fields: `secondary_currency_id:Many2one`; methods: `_get_secondary_currency()`
  - `AccountFeature` (`_name = account.feature`) — `models/account_feature.py`; fields: `name:Char`, `code:Char`, `parent_id:Many2one`, `parent_path:Char`, `company_id:Many2one`, `active:Boolean`, `notes:Text`, `child_ids:One2many`, `debit:Monetary`, `credit:Monetary`, `balance:Monetary`, `currency_id:Many2one`, `secondary_debit:Monetary`, `secondary_credit:Monetary`, `secondary_balance:Monetary`, `secondary_currency_id:Many2one`, `avg_rate:Float`; methods: `fields_get()`, `name_get()` …
  - `AccountCostCenter` (`_name = account.cost.center`) — `models/account_cost_center.py`; fields: `name:Char`, `code:Char`, `parent_id:Many2one`, `parent_path:Char`, `company_id:Many2one`, `active:Boolean`, `child_ids:One2many`, `debit:Monetary`, `credit:Monetary`, `balance:Monetary`, `currency_id:Many2one`, `secondary_debit:Monetary`, `secondary_credit:Monetary`, `secondary_balance:Monetary`, `secondary_currency_id:Many2one`, `avg_rate:Float`; methods: `fields_get()`, `name_get()` …
- **HTTP routes:**
  - `/advanced_accounting/reports/general_ledger` → `get_general_ledger_data()` in `controllers/main.py`
  - `/advanced_accounting/export/general_ledger_xlsx` → `export_general_ledger_xlsx()` in `controllers/xlsx_export.py`
  - `/advanced_accounting/export/trial_balance_xlsx` → `export_trial_balance_xlsx()` in `controllers/xlsx_export.py`
- **Menu declarations:** `Advanced Dimensions`, `Features`, `Cost Centers`, `Patch Numbers`, `General Ledger (Advanced)`, `Trial Balance (Advanced)`
- **View architectures detected:** field: 2, form: 5, list: 5, search: 7, t: 2, xpath: 2
- **Record rules:** `Account Feature Multi-Company`, `Account Cost Center Multi-Company`, `Account Patch Number Multi-Company`
- **ACL entries:** `account.feature.readonly` (group `account.group_account_readonly/1/0/0`), `account.feature.user` (group `account.group_account_user/1/1/1`), `account.feature.manager` (group `account.group_account_manager/1/1/1`), `account.cost.center.readonly` (group `account.group_account_readonly/1/0/0`), `account.cost.center.user` (group `account.group_account_user/1/1/1`), `account.cost.center.manager` (group `account.group_account_manager/1/1/1`), `account.patch.number.readonly` (group `account.group_account_readonly/1/0/0`), `account.patch.number.user` (group `account.group_account_user/1/1/1`), `account.patch.number.manager` (group `account.group_account_manager/1/1/1`), `general.ledger.wizard.user` (group `account.group_account_user/1/1/1`), `general.ledger.wizard.manager` (group `account.group_account_manager/1/1/1`), `trial.balance.wizard.user` (group `account.group_account_user/1/1/1`), `trial.balance.wizard.manager` (group `account.group_account_manager/1/1/1`)
- **Functional file groups:** Wizards: `wizard/general_ledger_wizard_views.xml`, `wizard/trial_balance_wizard_views.xml`, `wizard/__init__.py`, `wizard/trial_balance_wizard.py`, `wizard/general_ledger_wizard.py`; Reports: `report/report_actions.xml`, `report/general_ledger_report.py`, `report/report_general_ledger.xml`, `report/report_trial_balance.xml`, `report/__init__.py`, `report/trial_balance_report.py`; Controllers: `controllers/main.py`, `controllers/__init__.py`, `controllers/xlsx_export.py`; Security: `security/ir.model.access.csv`, `security/security.xml`; Data: `data/sequence.xml`; Views: `views/account_patch_number_views.xml`, `views/menus.xml`, `views/account_cost_center_views.xml`, `views/account_move_line_views.xml`, `views/report_general_ledger_views.xml`, `views/report_trial_balance_views.xml`, `views/report_search_views.xml`, `views/account_feature_views.xml` …
- **Tests present:** `tests/__init__.py`, `tests/test_advanced_accounting.py`
- **Implemented development-batch changes:** Batch 01: sanitized export errors and disabled spreadsheet formula/link auto-conversion. Critical pre_init_hook review remains pending.

### ODOO19 / `ai_finance_suite` — AI Finance

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** AI-Powered Finance Suite: Virtual CFO, OCR Engine & Smart Reconciliation for Odoo 19  
- **Category / license / author:** `Accounting/Finance` / `LGPL-3` / `Woledge Team`  
- **Dependencies:** `base`, `mail`, `account`  
- **Source inventory:** 40 files; 14 Python, 13 XML, 3 JavaScript, 3 SCSS; 0 test files.  
- **Python classes / models:**
  - `VendorBillWizard` (`_name = af.vendor.bill.wizard`) — `wizards/vendor_bill_wizard.py`; fields: `document_type:Selection`, `bank_account_id:Many2one`, `reference_code:Char`, `statement_date_from:Date`, `statement_date_to:Date`, `state:Selection`, `invoice_file:Binary`, `filename:Char`, `vendor_id:Many2one`, `vendor_name_extracted:Char`, `invoice_number:Char`, `invoice_date:Date`, `due_date:Date`, `currency_id:Many2one`, `subtotal:Float`, `tax_amount:Float`, `total_amount:Float`, `line_ids:One2many` …; methods: `action_select_type()`, `action_back_to_type()`, `action_process_file()`, `action_create_bank_statement()`, `action_create_bill()`, `action_create_statement_from_review()`, `action_back_to_upload()`, `action_create_refund()` …
  - `VendorBillWizardLine` (`_name = af.vendor.bill.wizard.line`) — `wizards/vendor_bill_wizard.py`; fields: `wizard_id:Many2one`, `description:Char`, `quantity:Float`, `unit_price:Float`, `discount:Float`, `total:Float`; methods: `_compute_total()`
  - `VendorBillWizardColumn` (`_name = af.vendor.bill.wizard.column`) — `wizards/vendor_bill_wizard.py`; fields: `wizard_id:Many2one`, `column_name:Char`, `is_recommended:Boolean`, `display_label:Char`; methods: `_compute_display_label()`
  - `CFOQueryWizard` (`_name = af.cfo.query.wizard`) — `wizards/cfo_query_wizard.py`; fields: `cfo_agent_id:Many2one`, `question:Text`, `suggested_question:Selection`, `answer:Html`, `show_answer:Boolean`; methods: `action_ask()`, `action_new_question()` …
  - `AICredential` (`_name = af.credential`) — `models/ai_credential.py`; fields: `name:Char`, `provider:Selection`, `api_key:Char`, `api_base_url:Char`, `anonymize_data:Boolean`, `gemini_model:Selection`, `openai_model:Selection`, `groq_model:Selection`, `deepseek_model:Selection`, `claude_model:Selection`, `xai_model:Selection`, `mistral_model:Selection`, `cohere_model:Selection`, `custom_model_name:Char`, `model_version:Selection`, `last_tested_date:Datetime`, `status:Selection`; methods: `get_effective_model()`, `action_test_connection()` …
  - `AIFinanceConfig` extends `res.config.settings` — `models/ai_config.py`; fields: `ocr_credential_id:Many2one`, `virtual_cfo_credential_id:Many2one`; methods: `default_get()`, `get_config()`
  - `VendorStatement` (`_name = af.vendor.statement`) extends `mail.thread`, `mail.activity.mixin` — `models/vendor_statement.py`; fields: `name:Char`, `partner_id:Many2one`, `statement_date:Date`, `currency_id:Many2one`, `date_from:Date`, `date_to:Date`, `statement_total_due:Monetary`, `odoo_total_due:Monetary`, `difference_amount:Monetary`, `line_ids:One2many`, `state:Selection`, `ocr_raw_text:Text`, `statement_column_ids:One2many`, `selected_column_id:Many2one`, `extracted_columns:Char`, `match_key_column:Selection`, `summary_total_lines:Integer`, `summary_matched:Integer` …; methods: `create()`, `action_match_lines()`, `action_confirm_matches()`, `action_rematch()`, `action_print_report()` …
  - `VendorStatementLine` (`_name = af.vendor.statement.line`) — `models/vendor_statement.py`; fields: `statement_id:Many2one`, `date:Date`, `name:Char`, `voucher_number:Char`, `amount:Monetary`, `currency_id:Many2one`, `matched_move_line_id:Many2one`, `candidate_move_line_ids:Many2many`, `matched_partner_id:Many2one`, `odoo_amount_residual:Monetary`, `match_status:Selection`, `match_notes:Char`, `is_odoo_only:Boolean`
  - `VendorStatementColumn` (`_name = af.vendor.statement.column`) — `models/vendor_statement.py`; fields: `statement_id:Many2one`, `column_name:Char`, `is_recommended:Boolean`, `display_label:Char`; methods: `_compute_display_label()`
  - `AccountBankStatementFix` extends `account.bank.statement` — `models/account_bank_statement.py`; fields: `journal_has_invalid_statements:Boolean`; methods: `_compute_journal_has_invalid_statements()`
  - `VirtualCFOAgent` (`_name = af.virtual.cfo.agent`) extends `mail.thread` — `models/virtual_cfo_agent.py`; fields: `name:Char`, `user_id:Many2one`, `company_id:Many2one`, `conversation_ids:One2many`, `query_count:Integer`, `recommendation_count:Integer`; methods: `create()`, `ask_question()`, `action_new_conversation()`, `action_view_recommendations()`, `action_generate_insights()` …
  - `CFOConversation` (`_name = af.cfo.conversation`) — `models/virtual_cfo_agent.py`; fields: `cfo_agent_id:Many2one`, `question:Text`, `answer:Html`, `state:Selection`, `context_used:Text`, `ai_model:Char`, `processing_time:Float`, `error_message:Text`
  - `AIFinanceDashboard` (`_name = af.finance.dashboard`) — `models/ai_finance_dashboard.py`; fields: `name:Char`, `company_id:Many2one`, `currency_id:Many2one`, `date_from:Date`, `date_to:Date`, `total_sales:Monetary`, `total_purchases:Monetary`, `gross_profit:Monetary`, `profit_margin:Float`, `total_receivable:Monetary`, `total_payable:Monetary`, `invoices_to_collect:Integer`, `bills_to_pay:Integer`, `collection_rate:Float`, `payment_rate:Float`, `total_overdue_receivable:Monetary`, `total_overdue_payable:Monetary`, `total_bank_balance:Monetary` …; methods: `action_refresh()`, `action_open_receivables()`, `action_open_payables()`, `action_open_overdue()`, `action_open_bank_journals()`, `action_open_dashboard()`, `action_period_this_month()`, `action_period_last_month()`, `action_period_this_quarter()`, `action_period_this_year()`, `action_open_aging()`, `get_dashboard_data()` …
  - `BankStatement` (`_name = af.bank.statement`) extends `mail.thread`, `mail.activity.mixin` — `models/bank_statement.py`; fields: `name:Char`, `bank_account_id:Many2one`, `bank_name:Char`, `account_number:Char`, `date_from:Date`, `date_to:Date`, `opening_balance:Monetary`, `closing_balance:Monetary`, `odoo_balance:Monetary`, `difference:Monetary`, `currency_id:Many2one`, `line_ids:One2many`, `state:Selection`, `ocr_raw_text:Text`, `summary_total_lines:Integer`, `summary_matched:Integer`, `summary_discrepancy:Integer`, `summary_missing_odoo:Integer` …; methods: `create()`, `action_match_lines()`, `action_confirm_matches()`, `action_rematch()`, `action_print_report()` …
  - `BankStatementLine` (`_name = af.bank.statement.line`) — `models/bank_statement.py`; fields: `statement_id:Many2one`, `date:Date`, `description:Char`, `debit:Float`, `credit:Float`, `balance:Float`, `is_odoo_only:Boolean`, `matched_move_line_id:Many2one`, `candidate_move_line_ids:Many2many`, `matched_partner_id:Many2one`, `currency_id:Many2one`, `match_status:Selection`, `match_notes:Char`
  - `AIRefundTracking` (`_name = af.refund.tracking`) extends `mail.thread`, `mail.activity.mixin` — `models/ai_refund_tracking.py`; fields: `ticket_number:Char`, `name:Char`, `vendor_id:Many2one`, `currency_id:Many2one`, `refund_amount:Monetary`, `state:Selection`, `request_date:Date`, `expected_credit_date:Date`, `credit_received_date:Date`, `passenger_name:Char`, `flight_details:Char`, `refund_reason:Text`, `notes:Text`, `original_bill_id:Many2one`, `credit_note_id:Many2one`, `ocr_document:Binary`, `ocr_filename:Char`, `raw_ocr_data:Text` …; methods: `action_request_refund()`, `action_mark_approved()`, `action_receive_credit_note()`, `action_close()` …
- **Menu declarations:** `AI Finance`, `Dashboard`, `Analytics`, `OCR Engine`, `Virtual CFO (Chatbot)`, `Reconciliation`, `Partner Statements`, `Bank Statements`, `Configuration`, `AI Credentials`, `Settings`
- **View architectures detected:** form: 7, list: 3, xpath: 1
- **ACL entries:** `af.virtual.cfo.agent` (group `base.group_user/1/1/1`), `af.cfo.conversation` (group `base.group_user/1/1/1`), `af.vendor.bill.wizard` (group `base.group_user/1/1/1`), `af.cfo.query.wizard` (group `base.group_user/1/1/1`), `af.vendor.bill.wizard.line` (group `base.group_user/1/1/1`), `af.credential` (group `account.group_account_manager/1/1/1`), `af.credential` (group `base.group_system/1/1/1`), `af.refund.tracking` (group `base.group_user/1/1/1`), `af.vendor.statement` (group `base.group_user/1/1/1`), `af.vendor.statement.line` (group `base.group_user/1/1/1`), `af.bank.statement` (group `base.group_user/1/1/1`), `af.bank.statement.line` (group `base.group_user/1/1/1`), `af.vendor.bill.wizard.column` (group `base.group_user/1/1/1`), `af.vendor.statement.column` (group `base.group_user/1/1/1`), `af.finance.dashboard` (group `base.group_user/1/1/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`; Views: `views/menu.xml`, `views/virtual_cfo_views.xml`, `views/ai_credential_views.xml`, `views/bank_statement_views.xml`, `views/ai_finance_dashboard_views.xml`, `views/ai_config_views.xml`, `views/vendor_statement_views.xml`, `views/ai_finance_dashboard_action.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `archer_meta_lead_ads` — Meta Lead Ads

- **Manifest version:** `18.0.1.0.0`  
- **Summary:** Import Meta lead ads into CRM leads  
- **Category / license / author:** `Sales/CRM` / `LGPL-3` / `Archer Solutions`  
- **Dependencies:** `crm`, `mail`, `contacts`, `utm`  
- **Source inventory:** 25 files; 12 Python, 9 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ArcherMetaLeadAdsController` — `controllers/oauth.py`; methods: `meta_oauth_callback()`
  - `MetaSyncLog` (`_name = meta.sync.log`) — `models/meta_sync_log.py`; fields: `name:Char`, `company_id:Many2one`, `level:Selection`, `category:Char`, `message:Text`, `credential_id:Many2one`, `page_id:Many2one`, `form_id:Many2one`, `lead_id:Many2one`; methods: `log()` …
  - `MetaAppCredential` (`_name = meta.app.credential`) extends `mail.thread`, `mail.activity.mixin` — `models/meta_app_credential.py`; fields: `name:Char`, `company_id:Many2one`, `app_id:Char`, `app_secret:Char`, `user_access_token:Text`, `token_expiry_date:Datetime`, `state:Selection`, `redirect_uri:Char`, `page_ids:One2many`, `page_count:Integer`, `sync_issue_count:Integer`, `last_sync_date:Datetime`, `notes:Html`, `active:Boolean`; methods: `action_generate_token()`, `action_exchange_oauth_code()`, `action_test_connection()`, `action_fetch_pages()`, `action_view_pages()`, `action_view_sync_issues()` …
  - `ResConfigSettings` extends `res.config.settings` — `models/res_config_settings.py`; methods: `action_open_meta_lead_ads()`
  - `MetaLeadFieldMapping` (`_name = meta.lead.field.mapping`) — `models/meta_lead_field_mapping.py`; fields: `sequence:Integer`, `form_id:Many2one`, `company_id:Many2one`, `meta_field_key:Char`, `odoo_field_id:Many2one`, `odoo_field_name:Char`, `odoo_field_ttype:Selection`, `relation:Char`, `lookup_field:Char`, `transform:Selection`, `is_default:Boolean`, `active:Boolean`; methods: `_onchange_odoo_field_id()`
  - `MetaLeadForm` (`_name = meta.lead.form`) extends `mail.thread`, `mail.activity.mixin` — `models/meta_lead_form.py`; fields: `name:Char`, `company_id:Many2one`, `page_id:Many2one`, `form_id:Char`, `status:Char`, `locale:Char`, `created_time:Datetime`, `crm_team_id:Many2one`, `utm_source_id:Many2one`, `utm_medium_id:Many2one`, `fetch_frequency_minutes:Selection`, `mapping_ids:One2many`, `mapping_count:Integer`, `lead_count:Integer`, `last_fetch_date:Datetime`, `questions_json:Text`, `active:Boolean`; methods: `action_view_leads()`, `action_fetch_form_fields()`, `action_fetch_leads()` …
  - `CrmLead` extends `crm.lead` — `models/crm_lead.py`; fields: `x_meta_leadgen_id:Char`, `x_meta_platform:Selection`, `x_meta_page_id:Many2one`, `x_meta_form_id:Many2one`, `x_meta_campaign_name:Char`, `x_meta_ad_name:Char`, `x_meta_created_time:Datetime`
  - `MetaPage` (`_name = meta.page`) extends `mail.thread`, `mail.activity.mixin` — `models/meta_page.py`; fields: `name:Char`, `company_id:Many2one`, `credential_id:Many2one`, `page_id:Char`, `page_access_token:Text`, `category:Char`, `platform:Selection`, `instagram_account_id:Char`, `fan_count:Integer`, `is_active:Boolean`, `form_ids:One2many`, `form_count:Integer`, `lead_count:Integer`; methods: `action_view_forms()`, `action_view_leads()`, `action_fetch_forms()` …
- **HTTP routes:**
  - `/meta_lead_ads/oauth/callback` → `meta_oauth_callback()` in `controllers/oauth.py`
- **Menu declarations:** `Meta Lead Ads`, `Credentials`, `Pages`, `Forms`, `Sync Issues`
- **View architectures detected:** form: 4, list: 4, search: 4, xpath: 3
- **Record rules:** `Meta Credential multi company`, `Meta Page multi company`, `Meta Form multi company`, `Meta Field Mapping multi company`, `Meta Sync Log multi company`
- **ACL entries:** `meta.app.credential.user` (group `archer_meta_lead_ads.group_meta_lead_ads_user/1/0/0`), `meta.app.credential.manager` (group `archer_meta_lead_ads.group_meta_lead_ads_manager/1/1/1`), `meta.page.user` (group `archer_meta_lead_ads.group_meta_lead_ads_user/1/1/0`), `meta.page.manager` (group `archer_meta_lead_ads.group_meta_lead_ads_manager/1/1/1`), `meta.lead.form.user` (group `archer_meta_lead_ads.group_meta_lead_ads_user/1/1/0`), `meta.lead.form.manager` (group `archer_meta_lead_ads.group_meta_lead_ads_manager/1/1/1`), `meta.lead.field.mapping.user` (group `archer_meta_lead_ads.group_meta_lead_ads_user/1/1/1`), `meta.lead.field.mapping.manager` (group `archer_meta_lead_ads.group_meta_lead_ads_manager/1/1/1`), `meta.sync.log.user` (group `archer_meta_lead_ads.group_meta_lead_ads_user/1/0/0`), `meta.sync.log.manager` (group `archer_meta_lead_ads.group_meta_lead_ads_manager/1/0/0`)
- **Functional file groups:** Controllers: `controllers/__init__.py`, `controllers/oauth.py`; Security: `security/ir.model.access.csv`, `security/security.xml`; Data: `data/ir_cron_data.xml`; Views: `views/meta_app_credential_views.xml`, `views/meta_sync_log_views.xml`, `views/menus.xml`, `views/meta_page_views.xml`, `views/meta_lead_form_views.xml`, `views/crm_lead_views.xml`, `views/res_config_settings_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `auto_project_stages` — Project Task Visit Forms

- **Manifest version:** `1.0`  
- **Summary:** إضافة تبويبات Site Visit وCompany Visit في مهام المشروع مع حقول تفصيلية  
- **Category / license / author:** `Project` / `not declared` / `Elmasry`  
- **Dependencies:** `project`  
- **Source inventory:** 4 files; 4 Python, 0 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ProjectProject` extends `project.project` — `models/project_project.py`; methods: `create()`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `bi_employee_travel_managment` — HR Employee Travel Expense in Odoo 

- **Manifest version:** `19.0.0.0`  
- **Summary:** Apps for Hr Travel Expense Travel Expense reimbursement Employee Travel Expenses for Employee Travel Request for Employee Expenses Travel Expense voucher employee Travel expense Advance HR Travel Expense request HR Expenses of travel HR Expenses request  
- **Category / license / author:** `human resources` / `OPL-1` / `BROWSEINFO`  
- **Dependencies:** `base`, `hr`, `hr_expense`, `project`  
- **Source inventory:** 12 files; 4 Python, 5 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `travel_expence` (`_name = travel.expence`) — `models/travel_request.py`; fields: `product_id:Many2one`, `unit_price:Float`, `product_qty:Float`, `name:Char`, `currency_id:Many2one`
  - `My_travel_request` (`_name = travel.request`) — `models/travel_request.py`; fields: `name:Char`, `employee_id:Many2one`, `department_manager_id:Many2one`, `department_id:Many2one`, `job_id:Many2one`, `currency_id:Many2one`, `request_by:Many2one`, `confirm_by:Many2one`, `approve_by:Many2one`, `req_date:Date`, `confirm_date:Date`, `approve_date:Date`, `travel_purpose:Char`, `project_id:Many2one`, `account_analytic_id:Many2one`, `from_city:Char`, `from_state_id:Many2one`, `from_country_id:Many2one` …; methods: `onchange_employee()`, `check_dates()`, `create()`, `write()`, `action_expence_sheet()`, `action_confirm()`, `action_approve()`, `return_from_trip()`, `action_create_expence()`, `action_draft()`, `action_reject()` …
  - `my_travel_request` (`_name = travel.mode`) — `models/travel_request.py`; fields: `name:Char`
  - `HrExpense` extends `hr.expense` — `models/travel_request.py`; fields: `travel_id:Many2one`, `travel_expence_id:Many2one`
- **Menu declarations:** `Travel`, `Travel Request`, `Employee Travel Request`, `Travel Request To Approve`
- **View architectures detected:** form: 1, list: 1
- **ACL entries:** `access.travel.request` (group `base.group_user/1/1/1`), `access.travel.mode` (group `base.group_user/1/1/1`), `access_travel_expence` (group `base.group_user/1/1/1`)
- **Functional file groups:** Reports: `report/report_views.xml`, `report/employee_travel_report.xml`; Security: `security/ir.model.access.csv`, `security/groups.xml`; Data: `data/employee_travel_sequencer_data.xml`; Views: `views/travel_request_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `bi_so_product_quantity_limit` — Sale Order Product Quantity Limit

- **Manifest version:** `19.0.0.0`  
- **Summary:** sale product quantity limit sales product limit sales order product maximum quantity limit product minimum quantity restrict product quantity limit sales order minimum product quantity max product quantity limit min product quantity limit  
- **Category / license / author:** `Sales` / `OPL-1` / `BROWSEINFO`  
- **Dependencies:** `base`, `sale`, `sale_management`  
- **Source inventory:** 54 files; 5 Python, 1 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ProductTemplate` extends `product.template` — `models/product_template.py`; fields: `min_qty:Float`, `max_qty:Float`; methods: `qty_validate()`
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; methods: `create()`, `action_confirm()`
  - `SaleOrderLine` extends `sale.order.line` — `models/sale_order.py`; methods: `onchange_product_uom_qty()`
- **View architectures detected:** xpath: 1
- **Functional file groups:** Views: `views/product_template_view.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `cheque_tracking` — Cheque Tracking

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Track received and issued cheques with accounting lifecycle entries  
- **Category / license / author:** `Accounting/Payment` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `mail`, `account`  
- **Source inventory:** 36 files; 15 Python, 18 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ChequeReturnWizard` (`_name = cheque.return.wizard`) — `wizards/return_wizard.py`; fields: `cheque_id:Many2one`, `return_date:Date`, `return_reason_id:Many2one`, `bank_charges:Monetary`, `penalty_amount:Monetary`, `create_activity:Boolean`, `notes:Text`, `currency_id:Many2one`; methods: `action_return_cheque()`
  - `ChequeDepositWizard` (`_name = cheque.deposit.wizard`) — `wizards/deposit_wizard.py`; fields: `deposit_date:Date`, `bank_journal_id:Many2one`, `cheque_ids:Many2many`, `notes:Text`; methods: `action_create_deposit()`
  - `ChequePrintWizard` (`_name = cheque.print.wizard`) — `wizards/print_wizard.py`; fields: `cheque_ids:Many2many`, `template:Selection`; methods: `action_print()`
  - `ChequeReturnReason` (`_name = cheque.return.reason`) — `models/return_reason.py`; fields: `name:Char`, `code:Char`, `category:Selection`, `description:Text`, `active:Boolean`, `company_id:Many2one`
  - `ChequeCheque` (`_name = cheque.cheque`) extends `mail.thread`, `mail.activity.mixin` — `models/cheque.py`; fields: `name:Char`, `cheque_type:Selection`, `cheque_number:Char`, `cheque_date:Date`, `due_date:Date`, `amount:Monetary`, `currency_id:Many2one`, `company_currency_id:Many2one`, `amount_company_currency:Monetary`, `exchange_rate:Float`, `partner_id:Many2one`, `payee_name:Char`, `bank_id:Many2one`, `bank_branch_id:Many2one`, `bank_account_id:Many2one`, `deposit_account_id:Many2one`, `invoice_ids:Many2many`, `deposit_id:Many2one` …; methods: `create()`, `write()`, `action_submit()`, `action_approve()`, `action_deposit()`, `action_clear()`, `action_mark_cashed()`, `action_hand_over()`, `action_void()`, `action_cancel()`, `action_open_return_wizard()`, `action_print_cheque()` …
  - `AccountMove` extends `account.move` — `models/account_move.py`; fields: `cheque_id:Many2one`, `cheque_deposit_id:Many2one`, `cheque_return_id:Many2one`, `cheque_stage:Selection`
  - `ResCompany` extends `res.company` — `models/res_company.py`; fields: `cheque_received_account_id:Many2one`, `cheque_under_collection_account_id:Many2one`, `cheque_issued_account_id:Many2one`, `cheque_bank_charges_account_id:Many2one`, `cheque_penalty_income_account_id:Many2one`, `cheque_stale_months:Integer`, `cheque_pdc_reminder_days:Integer`, `cheque_max_redeposit_attempts:Integer`, `cheque_approval_threshold:Monetary`
  - `ChequeDeposit` (`_name = cheque.deposit`) extends `mail.thread`, `mail.activity.mixin` — `models/deposit.py`; fields: `name:Char`, `deposit_date:Date`, `bank_journal_id:Many2one`, `cheque_ids:One2many`, `total_amount:Monetary`, `currency_id:Many2one`, `journal_entry_id:Many2one`, `state:Selection`, `notes:Text`, `company_id:Many2one`; methods: `create()`, `action_confirm()`, `action_cancel()`, `action_print_deposit_slip()` …
  - `ChequeReturn` (`_name = cheque.return`) extends `mail.thread`, `mail.activity.mixin` — `models/cheque_return.py`; fields: `name:Char`, `cheque_id:Many2one`, `return_date:Date`, `return_reason_id:Many2one`, `bank_charges:Monetary`, `penalty_amount:Monetary`, `notes:Text`, `currency_id:Many2one`, `company_id:Many2one`, `move_ids:One2many`; methods: `create()`
  - `ResPartner` extends `res.partner` — `models/res_partner.py`; fields: `received_cheque_count:Integer`, `issued_cheque_count:Integer`, `bounced_cheque_count:Integer`, `total_cheque_received:Float`, `total_cheque_issued:Float`; methods: `action_view_received_cheques()`, `action_view_issued_cheques()` …
  - `ResConfigSettings` extends `res.config.settings` — `models/res_config_settings.py`; fields: `cheque_received_account_id:Many2one`, `cheque_under_collection_account_id:Many2one`, `cheque_issued_account_id:Many2one`, `cheque_bank_charges_account_id:Many2one`, `cheque_penalty_income_account_id:Many2one`, `cheque_stale_months:Integer`, `cheque_pdc_reminder_days:Integer`, `cheque_max_redeposit_attempts:Integer`, `cheque_approval_threshold:Monetary`
- **Menu declarations:** `Cheque Tracking`, `Operations`, `Received Cheques`, `Issued Cheques`, `All Cheques`, `Deposits`, `Returns`, `Reporting`, `Cheque Analysis`, `Configuration`, `Return Reasons`, `Settings`
- **View architectures detected:** calendar: 1, form: 7, graph: 1, kanban: 1, list: 4, pivot: 1, search: 2, xpath: 2
- **Record rules:** `Cheque multi-company`, `Cheque deposit multi-company`, `Cheque return multi-company`
- **ACL entries:** `cheque.cheque.user` (group `cheque_tracking.group_cheque_user/1/1/1`), `cheque.cheque.manager` (group `cheque_tracking.group_cheque_manager/1/1/1`), `cheque.deposit.user` (group `cheque_tracking.group_cheque_user/1/1/1`), `cheque.deposit.manager` (group `cheque_tracking.group_cheque_manager/1/1/1`), `cheque.return.user` (group `cheque_tracking.group_cheque_user/1/0/0`), `cheque.return.manager` (group `cheque_tracking.group_cheque_manager/1/1/1`), `cheque.return.reason.user` (group `cheque_tracking.group_cheque_user/1/0/0`), `cheque.return.reason.admin` (group `cheque_tracking.group_cheque_admin/1/1/1`), `cheque.deposit.wizard` (group `cheque_tracking.group_cheque_user/1/1/1`), `cheque.return.wizard` (group `cheque_tracking.group_cheque_manager/1/1/1`), `cheque.print.wizard` (group `cheque_tracking.group_cheque_user/1/1/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`, `security/cheque_security.xml`, `security/groups.xml`; Data: `data/return_reason_data.xml`, `data/sequence_data.xml`, `data/ir_cron_data.xml`; Views: `views/cheque_views.xml`, `views/return_views.xml`, `views/menus.xml`, `views/return_reason_views.xml`, `views/partner_views.xml`, `views/res_config_settings_views.xml`, `views/deposit_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `cheque_tracking_endorsement` — Cheque Tracking Endorsement

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Cheque endorsement workflow for cheque tracking  
- **Category / license / author:** `Accounting/Payment` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `cheque_tracking`  
- **Source inventory:** 19 files; 10 Python, 8 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ChequeEndorseWizard` (`_name = cheque.endorse.wizard`) — `wizards/endorse_wizard.py`; fields: `cheque_id:Many2one`, `current_beneficiary_id:Many2one`, `endorsee_partner_id:Many2one`, `endorsement_date:Date`, `reason:Text`, `create_vendor_bill:Boolean`; methods: `action_confirm()`
  - `ChequeCheque` extends `cheque.cheque` — `models/cheque.py`; fields: `is_endorsable:Boolean`, `is_crossed:Boolean`, `original_beneficiary_id:Many2one`, `current_endorsee_id:Many2one`, `endorsement_ids:One2many`, `endorsement_count:Integer`, `state:Selection`; methods: `create()`, `init()`, `write()`, `action_open_endorse_wizard()`, `action_endorse()`, `action_deposit()`, `action_cancel()`, `action_view_endorsements()` …
  - `AccountMove` extends `account.move` — `models/account_move.py`; fields: `cheque_endorsement_id:Many2one`, `cheque_stage:Selection`; methods: `action_view_cheque()`
  - `ChequeEndorsement` (`_name = cheque.endorsement`) extends `mail.thread`, `mail.activity.mixin` — `models/cheque_endorsement.py`; fields: `name:Char`, `cheque_id:Many2one`, `company_id:Many2one`, `currency_id:Many2one`, `amount:Monetary`, `endorser_id:Many2one`, `endorsee_id:Many2one`, `endorsement_date:Date`, `reason:Text`, `sequence:Integer`, `move_id:Many2one`, `vendor_bill_id:Many2one`, `state:Selection`, `user_id:Many2one`; methods: `create()`, `init()` …
  - `ResCompany` extends `res.company` — `models/res_company.py`; fields: `cheque_allow_post_dated_endorsement:Boolean`, `cheque_endorsement_reminder_days:Integer`, `cheque_endorsement_payable_account_id:Many2one`, `cheque_endorsement_bill_account_id:Many2one`
  - `ResConfigSettings` extends `res.config.settings` — `models/res_config_settings.py`; fields: `cheque_allow_post_dated_endorsement:Boolean`, `cheque_endorsement_reminder_days:Integer`, `cheque_endorsement_payable_account_id:Many2one`, `cheque_endorsement_bill_account_id:Many2one`
- **Menu declarations:** `Endorsements`
- **View architectures detected:** form: 2, list: 1, search: 1, xpath: 5
- **Record rules:** `Cheque endorsement multi-company`
- **ACL entries:** `cheque.endorsement.user` (group `cheque_tracking.group_cheque_user/1/0/0`), `cheque.endorsement.manager` (group `cheque_tracking_endorsement.group_cheque_endorse/1/1/1`), `cheque.endorsement.cheque.manager` (group `cheque_tracking.group_cheque_manager/1/1/1`), `cheque.endorsement.cheque.admin` (group `cheque_tracking.group_cheque_admin/1/1/1`), `cheque.endorse.wizard` (group `cheque_tracking_endorsement.group_cheque_endorse/1/1/1`), `cheque.endorse.wizard.manager` (group `cheque_tracking.group_cheque_manager/1/1/1`), `cheque.endorse.wizard.admin` (group `cheque_tracking.group_cheque_admin/1/1/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`, `security/groups.xml`, `security/endorsement_security.xml`; Views: `views/cheque_views.xml`, `views/menus.xml`, `views/endorsement_views.xml`, `views/res_config_settings_views.xml`, `views/account_move_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `connector_foodics` — Foodics Connector

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Bidirectional synchronization bridge between Odoo and Foodics POS  
- **Category / license / author:** `Sales/Point of Sale` / `LGPL-3` / `Woledge`  
- **Dependencies:** `account`, `contacts`, `mail`, `point_of_sale`, `product`, `sale_management`, `stock`  
- **Source inventory:** 38 files; 21 Python, 14 XML, 0 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestFoodicsModels` — `tests/test_foodics_models.py`; methods: `test_connection_generates_webhook_url()`, `test_sync_log_serializes_payloads()`
  - `FoodicsWebhookController` — `controllers/webhook_controller.py`; methods: `foodics_webhook_health()`, `foodics_webhook_http()` …
  - `FoodicsResyncWizard` (`_name = foodics.resync.wizard`) — `wizards/wizard_resync.py`; fields: `connection_id:Many2one`, `start_date:Datetime`, `sync_products:Boolean`, `sync_categories:Boolean`, `sync_customers:Boolean`, `sync_orders:Boolean`, `sync_inventory:Boolean`, `sync_taxes:Boolean`; methods: `action_resync()`
  - `FoodicsTestConnectionWizard` (`_name = foodics.test.connection.wizard`) — `wizards/wizard_test_connection.py`; fields: `connection_id:Many2one`, `result:Text`; methods: `action_test()`
  - `FoodicsWebhookEvent` (`_name = foodics.webhook.event`) — `models/foodics_webhook.py`; fields: `connection_id:Many2one`, `name:Char`, `event_type:Char`, `active:Boolean`
  - `FoodicsWebhookLog` (`_name = foodics.webhook.log`) — `models/foodics_webhook.py`; fields: `connection_id:Many2one`, `event_type:Char`, `event_id:Char`, `payload:Text`, `received_at:Datetime`, `processed:Boolean`, `processing_date:Datetime`, `status:Selection`, `error_message:Text`, `sync_log_id:Many2one`; methods: `create_from_request()`, `process()`
  - `ProductProduct` extends `product.product` — `models/product_product.py`; fields: `foodics_id:Char`, `foodics_sync_enabled:Boolean`, `foodics_last_sync_date:Datetime`; methods: `action_foodics_sync_now()`
  - `ProductTemplate` extends `product.template` — `models/product_product.py`; fields: `foodics_sync_enabled:Boolean`
  - `ProductCategory` extends `product.category` — `models/product_category.py`; fields: `foodics_id:Char`, `foodics_sync_enabled:Boolean`, `foodics_last_sync_date:Datetime`
  - `FoodicsMapping` (`_name = foodics.mapping`) — `models/foodics_mapping.py`; fields: `sequence:Integer`, `connection_id:Many2one`, `name:Char`, `odoo_model:Char`, `foodics_resource:Char`, `odoo_field:Char`, `foodics_field:Char`, `mapping_type:Selection`, `default_value:Char`, `transform_function:Char`, `active:Boolean`; methods: `_compute_name()`
  - `FoodicsBranchMapping` (`_name = foodics.branch.mapping`) — `models/foodics_mapping.py`; fields: `connection_id:Many2one`, `name:Char`, `foodics_branch_id:Char`, `warehouse_id:Many2one`, `location_id:Many2one`, `pos_config_id:Many2one`, `company_id:Many2one`, `active:Boolean`, `notes:Text`
  - `AccountTax` extends `account.tax` — `models/account_tax.py`; fields: `foodics_id:Char`, `foodics_sync_enabled:Boolean`, `foodics_last_sync_date:Datetime`
  - `FoodicsConnection` (`_name = foodics.connection`) extends `mail.thread`, `mail.activity.mixin` — `models/foodics_connection.py`; fields: `name:Char`, `sequence:Integer`, `business_id:Char`, `api_key:Char`, `api_secret:Char`, `token:Char`, `token_expires_at:Datetime`, `base_url:Char`, `test_mode:Boolean`, `active:Boolean`, `state:Selection`, `last_successful_call:Datetime`, `last_sync_date:Datetime`, `last_error:Text`, `webhook_secret:Char`, `webhook_url:Char`, `company_id:Many2one`, `sync_products:Boolean` …; methods: `action_generate_webhook_secret()`, `action_open_sync_logs()`, `action_open_failed_sync_logs()`, `action_test_connection()`, `cron_sync_products()`, `cron_sync_categories()`, `cron_sync_customers()`, `cron_sync_orders()`, `cron_sync_inventory()`, `cron_sync_taxes()` …
  - `ResPartner` extends `res.partner` — `models/res_partner.py`; fields: `foodics_id:Char`, `foodics_loyalty_points:Float`, `foodics_sync_enabled:Boolean`, `foodics_last_sync_date:Datetime`
  - `FoodicsBaseAdapter` (`_name = foodics.base.adapter`) — `models/foodics_adapters.py`; methods: `run()` …
  - `FoodicsProductAdapter` (`_name = foodics.product.adapter`) extends `foodics.base.adapter` — `models/foodics_adapters.py`; methods: `_to_foodics_payload()`
  - `FoodicsCategoryAdapter` (`_name = foodics.category.adapter`) extends `foodics.base.adapter` — `models/foodics_adapters.py`
  - `FoodicsCustomerAdapter` (`_name = foodics.customer.adapter`) extends `foodics.base.adapter` — `models/foodics_adapters.py`
  - `FoodicsOrderAdapter` (`_name = foodics.order.adapter`) extends `foodics.base.adapter` — `models/foodics_adapters.py`; methods: `_domain()`
  - `FoodicsInventoryAdapter` (`_name = foodics.inventory.adapter`) extends `foodics.base.adapter` — `models/foodics_adapters.py`; methods: `_domain()`
  - `FoodicsTaxAdapter` (`_name = foodics.tax.adapter`) extends `foodics.base.adapter` — `models/foodics_adapters.py`; methods: `_domain()`
  - `FoodicsApiClient` (`_name = foodics.api.client`) — `models/foodics_api.py`; methods: `call()` …
  - `FoodicsSyncLog` (`_name = foodics.sync.log`) extends `mail.thread`, `mail.activity.mixin` — `models/foodics_sync_log.py`; fields: `name:Char`, `connection_id:Many2one`, `company_id:Many2one`, `sync_type:Selection`, `direction:Selection`, `foodics_resource:Char`, `foodics_record_id:Char`, `odoo_model:Char`, `odoo_record_id:Integer`, `status:Selection`, `error_message:Text`, `retry_count:Integer`, `max_retries:Integer`, `next_retry_date:Datetime`, `execution_time:Float`, `request_payload:Text`, `response_data:Text`; methods: `create()`, `action_retry()`, `cron_retry_failed()`, `action_view_odoo_record()` …
- **HTTP routes:**
  - `/foodics/webhook/<string:secret>` → `foodics_webhook_health()` in `controllers/webhook_controller.py`
  - `/foodics/webhook/<string:secret>` → `foodics_webhook_http()` in `controllers/webhook_controller.py`
- **Menu declarations:** `Field Mappings`, `Dashboard`, `Customers`, `Monitoring`, `Sync Logs`, `Webhook Events`, `Webhook Logs`, `Synchronized Data`, `Products`, `Foodics Connector`, `Configuration`, `Connections`, `Reports`, `Stock Reconciliation`, `Full Resync`
- **View architectures detected:** form: 7, kanban: 1, list: 7, search: 2
- **ACL entries:** `foodics.connection admin` (group `connector_foodics.group_foodics_admin/1/1/1`), `foodics.connection operator` (group `connector_foodics.group_foodics_operator/1/0/0`), `foodics.mapping admin` (group `connector_foodics.group_foodics_admin/1/1/1`), `foodics.mapping operator` (group `connector_foodics.group_foodics_operator/1/0/0`), `foodics.branch.mapping admin` (group `connector_foodics.group_foodics_admin/1/1/1`), `foodics.branch.mapping operator` (group `connector_foodics.group_foodics_operator/1/0/0`), `foodics.sync.log admin` (group `connector_foodics.group_foodics_admin/1/1/1`), `foodics.sync.log operator` (group `connector_foodics.group_foodics_operator/1/1/0`), `foodics.webhook.event admin` (group `connector_foodics.group_foodics_admin/1/1/1`), `foodics.webhook.event operator` (group `connector_foodics.group_foodics_operator/1/0/0`), `foodics.webhook.log admin` (group `connector_foodics.group_foodics_admin/1/1/1`), `foodics.webhook.log operator` (group `connector_foodics.group_foodics_operator/1/1/0`), `foodics.test.connection.wizard` (group `connector_foodics.group_foodics_admin/1/1/1`), `foodics.resync.wizard` (group `connector_foodics.group_foodics_admin/1/1/1`)
- **Functional file groups:** Reports: `report/reconciliation_report.xml`; Controllers: `controllers/webhook_controller.py`, `controllers/__init__.py`; Security: `security/ir.model.access.csv`, `security/groups.xml`; Data: `data/foodics_webhook_events.xml`, `data/default_mappings.xml`, `data/cron_data.xml`; Views: `views/foodics_mapping_views.xml`, `views/dashboard_views.xml`, `views/partner_views.xml`, `views/foodics_sync_log_views.xml`, `views/foodics_webhook_views.xml`, `views/product_views.xml`, `views/foodics_connection_views.xml`
- **Tests present:** `tests/test_foodics_models.py`, `tests/__init__.py`
- **Implemented development-batch changes:** Batch 01: validates JSON object payloads and sanitizes internal errors returned from webhook endpoints; signature verification remains pending.

### ODOO19 / `crm_project_linker` — CRM Project Linker

- **Manifest version:** `1.0`  
- **Summary:** Create and link projects from CRM opportunities.  
- **Category / license / author:** `CRM` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `project`, `crm`, `sale_management`  
- **Source inventory:** 5 files; 4 Python, 1 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `CrmLead` extends `crm.lead` — `models/crm_lead.py`; fields: `project_id:Many2one`, `sale_order_id:Many2one`; methods: `action_open_project()`, `action_create_project()`
  - `Project` extends `project.project` — `models/crm_lead.py`; fields: `crm_lead_id:Many2one`, `sale_order_id:Many2one`, `sale_order_ids:One2many`; methods: `action_open_crm_lead()`, `action_create_quotation_from_project()`
  - `SaleOrder` extends `sale.order` — `models/crm_lead.py`; fields: `project_id:Many2one`
- **View architectures detected:** xpath: 4
- **Functional file groups:** Views: `views/crm_lead_view.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `customer_classification` — Customer Classification & Credit Control

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Classify customers into tiers (A-E) with inherited price lists, credit limits, and payment terms.  
- **Category / license / author:** `Sales/Sales` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `sale`, `account`  
- **Source inventory:** 16 files; 8 Python, 5 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `CustomerClassification` (`_name = customer.classification`) extends `mail.thread`, `mail.activity.mixin` — `models/customer_classification.py`; fields: `name:Char`, `description:Text`, `sequence:Integer`, `active:Boolean`, `pricelist_id:Many2one`, `credit_limit:Float`, `payment_term_id:Many2one`, `credit_policy:Selection`, `company_id:Many2one`, `partner_ids:One2many`, `partner_count:Integer`, `criteria_ids:One2many`, `has_active_criteria:Boolean`; methods: `action_apply_pricelist()` …
  - `AccountMove` extends `account.move` — `models/account_move.py`; fields: `partner_classification_id:Many2one`, `partner_effective_credit_limit:Float`, `partner_credit_policy:Selection`; methods: `action_post()` …
  - `ClassificationCriteria` (`_name = classification.criteria`) — `models/classification_criteria.py`; fields: `classification_id:Many2one`, `sequence:Integer`, `model_field:Selection`, `operator:Selection`, `value:Float`, `value_to:Float`, `active:Boolean`; methods: `_compute_display_name()`, `_check_between_values()`, `_evaluate()`
  - `ResPartner` extends `res.partner` — `models/res_partner.py`; fields: `classification_id:Many2one`, `override_pricelist:Boolean`, `override_credit_limit:Boolean`, `override_payment_term:Boolean`, `manual_pricelist_id:Many2one`, `classification_pricelist_id:Many2one`, `classification_credit_limit:Float`, `classification_payment_term_id:Many2one`, `credit_policy:Selection`, `effective_credit_limit:Float`, `effective_payment_term_id:Many2one`; methods: `_compute_product_pricelist()`, `_compute_effective_credit_limit()`, `_compute_effective_payment_term_id()`, `_onchange_classification_id()`, `_onchange_override_pricelist()`, `_onchange_override_credit_limit()`, `_onchange_override_payment_term()`
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; fields: `partner_classification_id:Many2one`, `partner_effective_credit_limit:Float`, `partner_credit_policy:Selection`; methods: `action_confirm()` …
- **Menu declarations:** `Customer Classification`, `Classifications`
- **View architectures detected:** form: 1, list: 1, search: 1, xpath: 4
- **ACL entries:** `customer.classification.manager` (group `sales_team.group_sale_manager/1/1/1`), `customer.classification.user` (group `sales_team.group_sale_salesman/1/0/0`), `classification.criteria.manager` (group `sales_team.group_sale_manager/1/1/1`), `classification.criteria.user` (group `sales_team.group_sale_salesman/1/0/0`)
- **Functional file groups:** Security: `security/ir.model.access.csv`; Data: `data/classification_cron.xml`, `data/default_data.xml`; Views: `views/res_partner_views.xml`, `views/sale_order_views.xml`, `views/customer_classification_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `deduction_management` — Deduction

- **Manifest version:** `19.0.2.0.0`  
- **Summary:** Manages employees' deductions  
- **Category / license / author:** `Hidden` / `Other proprietary` / `Abdullah Al-Habbal`  
- **Dependencies:** `base`, `hr_payroll`, `hr_work_entry_enterprise`  
- **Source inventory:** 9 files; 5 Python, 2 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `Deduction` (`_name = deduction.deduction`) extends `mail.thread`, `mail.activity.mixin` — `models/deduction.py`; fields: `employee_id:Many2one`, `vehicle_id:Many2one`, `date:Date`, `amount:Monetary`, `state:Selection`, `deduction_type:Selection`, `liter_value:Monetary`, `litres_no:Float`, `litres_total_cost:Monetary`, `company_id:Many2one`, `currency_id:Many2one`; methods: `employee_id_domain()`, `button_approve1()`, `button_approve2()`, `button_approve()`, `button_reject()`, `action_reset_to_draft()`, `get_admins()`, `write()`, `unlink()` …
  - `HrPayslip` extends `hr.payslip` — `models/hr_payslip.py`; methods: `action_payslip_paid()`, `action_payslip_unpaid()`, `action_payslip_cancel()`
- **Menu declarations:** `Deductions`
- **View architectures detected:** form: 1, list: 1, search: 1
- **Record rules:** `Deduction rule`
- **ACL entries:** `deduction.deduction.user` (group `deduction_management.group_deduction_management_user/1/0/0`), `deduction.deduction.approver` (group `deduction_management.group_deduction_management_approver/1/1/1`), `deduction.deduction.hr` (group `deduction_management.group_deduction_management_hr/1/1/1`), `deduction.deduction.manager` (group `deduction_management.group_deduction_management_manager/1/1/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`, `security/security.xml`; Views: `views/deduction_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `direct_print_auto` — Direct Print Auto

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Auto-print invoices, SOs, delivery slips and POs to the browser's print dialog when confirmed, plus a manual Direct Print button on each form.  
- **Category / license / author:** `Sales/Sales` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `web`, `sale_management`, `account`, `stock`, `purchase`  
- **Source inventory:** 42 files; 12 Python, 9 XML, 1 JavaScript, 0 SCSS; 3 test files.  
- **Python classes / models:**
  - `TestDirectPrintMixin` — `tests/test_direct_print_mixin.py`; methods: `setUp()`, `test_01_sale_order_report_ref()`, `test_02_account_move_report_ref()`, `test_03_stock_picking_report_ref()`, `test_04_purchase_order_report_ref()`, `test_10_so_auto_print_disabled_by_default()`, `test_11_so_auto_print_enabled()`, `test_12_invoice_auto_print_customer_only()`, `test_13_picking_auto_print_outgoing_only()`, `test_20_action_direct_print_returns_client_action()`
  - `TestAutoPrintFlow` — `tests/test_auto_print_flow.py`; methods: `setUp()`, `test_30_so_confirm_wraps_action_when_auto_print_on()`, `test_31_so_confirm_no_wrap_when_auto_print_off()`
  - `PurchaseOrder` (`_name = purchase.order`) extends `purchase.order`, `direct.print.mixin` — `models/purchase_order.py`; methods: `button_approve()` …
  - `AccountMove` (`_name = account.move`) extends `account.move`, `direct.print.mixin` — `models/account_move.py`; methods: `action_post()` …
  - `DirectPrintMixin` (`_name = direct.print.mixin`) — `models/direct_print_mixin.py`; methods: `action_direct_print()` …
  - `ResConfigSettings` extends `res.config.settings` — `models/res_config_settings.py`; fields: `direct_print_invoice_auto:Boolean`, `direct_print_so_auto:Boolean`, `direct_print_picking_auto:Boolean`, `direct_print_po_auto:Boolean`, `direct_print_open_dialog:Boolean`
  - `StockPicking` (`_name = stock.picking`) extends `stock.picking`, `direct.print.mixin` — `models/stock_picking.py`; methods: `button_validate()` …
  - `SaleOrder` (`_name = sale.order`) extends `sale.order`, `direct.print.mixin` — `models/sale_order.py`; methods: `action_confirm()` …
- **View architectures detected:** xpath: 5
- **ACL entries:** `res.config.settings.direct.print.user` (group `group_direct_print_manager/1/1/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`, `security/direct_print_groups.xml`; Views: `views/sale_order_views.xml`, `views/client_actions.xml`, `views/stock_picking_views.xml`, `views/purchase_order_views.xml`, `views/res_config_settings_views.xml`, `views/account_move_views.xml`, `views/direct_print_menus.xml`
- **Tests present:** `tests/test_direct_print_mixin.py`, `tests/__init__.py`, `tests/test_auto_print_flow.py`

### ODOO19 / `ebook_serial_delivery` — eBook Serial Delivery

- **Manifest version:** `19.0.1.1.0`  
- **Summary:** Deliver eBook licenses using standard Inventory Serial Numbers (stock.lot) — no custom "activation code" model.  
- **Category / license / author:** `Website/eCommerce` / `LGPL-3` / `Custom Development`  
- **Dependencies:** `website_sale`, `sale_stock`, `mail`  
- **Source inventory:** 17 files; 12 Python, 4 XML, 0 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestSerialMailTemplate` — `tests/test_serial_mail_template.py`; methods: `setUpClass()`, `test_default_template()`, `test_template_chosen_in_settings_is_sent()`, `test_serial_numbers_placeholder()`, `test_empty_setting_falls_back_to_default()` …
  - `ResCompany` extends `res.company` — `models/res_company.py`; fields: `ebook_serial_mail_template_id:Many2one`; methods: `_default_ebook_serial_mail_template()`, `_get_ebook_serial_mail_template()`
  - `ResConfigSettings` extends `res.config.settings` — `models/res_config_settings.py`; fields: `ebook_serial_mail_template_id:Many2one`; methods: `action_open_ebook_serial_mail_template()`
  - `StockPicking` extends `stock.picking` — `models/stock_picking.py`; fields: `ebook_email_sent:Boolean`; methods: `action_resend_ebook_email()` …
  - `StockPickingJawalySms` (`_name = ebook.jawaly.sms.helper`) — `models/ebook_activation_code.py`; methods: `send_serial_sms()`
  - `ProductTemplate` extends `product.template` — `models/product_template.py`; fields: `is_ebook_with_codes:Boolean`; methods: `_onchange_is_ebook_with_codes()`
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; fields: `ebook_serial_numbers_html:Html`; methods: `action_confirm()` …
  - `StockMove` extends `stock.move` — `models/stock_move.py`; methods: `_action_done()`
- **View architectures detected:** xpath: 3
- **Functional file groups:** Reports: `report/ebook_serial_report_templates.xml`; Data: `data/mail_template_data.xml`; Views: `views/res_config_settings_views.xml`, `views/product_template_views.xml`
- **Tests present:** `tests/test_serial_mail_template.py`, `tests/__init__.py`

### ODOO19 / `el_barcode_price_display` — Barcode Price Display

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Standalone barcode scanner price display page — no login needed  
- **Category / license / author:** `Inventory/Inventory` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `product`  
- **Source inventory:** 17 files; 6 Python, 2 XML, 1 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestBarcodePriceDisplay` — `tests/test_price_display.py`; methods: `setUpClass()`, `test_01_page_loads()`, `test_02_product_found()`, `test_03_product_not_found()`, `test_04_short_barcode_rejected()`, `test_05_placeholder_for_no_image()`, `test_06_placeholder_color_deterministic()`, `test_07_product_with_image()`, `test_08_empty_barcode()`, `test_09_no_barcode_param()`, `test_10_groups_exist()`
  - `BarcodePriceDisplay` — `controllers/main.py`; methods: `price_display_page()`, `price_display_search()`
- **HTTP routes:**
  - `/price-display` → `price_display_page()` in `controllers/main.py`
  - `/price-display/search` → `price_display_search()` in `controllers/main.py`
- **ACL entries:** `barcode.price.user` (group `group_barcode_price_user/1/0/0`)
- **Functional file groups:** Controllers: `controllers/main.py`, `controllers/__init__.py`; Security: `security/ir.model.access.csv`, `security/groups.xml`; Views: `views/templates.xml`
- **Tests present:** `tests/test_price_display.py`, `tests/__init__.py`

### ODOO19 / `el_button_access_control` — Button Access Control

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Control button visibility per user group — show/hide buttons in any view without editing XML  
- **Category / license / author:** `Tools/Security` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`  
- **Source inventory:** 18 files; 7 Python, 4 XML, 1 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestButtonAccessRule` — `tests/test_button_access.py`; methods: `setUpClass()`, `test_01_create_rule()`, `test_02_rule_requires_groups()`, `test_03_unique_constraint()`, `test_04_whitelist_injects_groups()`, `test_05_whitelist_multiple_groups()`, `test_06_blacklist_mode()`, `test_07_view_type_all()`, `test_08_view_type_list()`, `test_09_view_type_kanban()`, `test_10_archive_rule()`, `test_11_inactive_rule_not_applied()` …
  - `TestButtonAccessRuleIntegration` — `tests/test_button_access.py`; methods: `setUpClass()`, `test_20_fields_view_get_does_not_crash()`, `test_21_rule_creation_clears_cache()`, `test_22_rule_deletion()`
  - `Base` extends `base` — `models/base.py`; methods: `_get_view()`, `_el_apply_button_access_rules()`
  - `ElButtonAccessRule` (`_name = el.button.access.rule`) — `models/button_access_rule.py`; fields: `name:Char`, `sequence:Integer`, `active:Boolean`, `model_id:Many2one`, `model_name:Char`, `view_type:Selection`, `button_name:Selection`, `button_string:Char`, `mode:Selection`, `group_ids:Many2many`, `company_id:Many2one`; methods: `action_scan_buttons()`, `rpc_get_available_buttons()`, `create()`, `write()`, `unlink()`, `action_test_rule()` …
- **Menu declarations:** `Button Access Control`, `Rules`, `Configuration`, `User Groups`
- **View architectures detected:** form: 1, list: 1, search: 1
- **ACL entries:** `el.button.access.rule.user` (group `group_button_access_user/1/0/0`), `el.button.access.rule.manager` (group `group_button_access_manager/1/1/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`, `security/el_button_access_control_groups.xml`; Views: `views/menus.xml`, `views/button_access_rule_views.xml`
- **Tests present:** `tests/__init__.py`, `tests/test_button_access.py`

### ODOO19 / `el_cheque_tracking` — EL Cheque Tracking

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Track received and issued cheques with accounting lifecycle entries  
- **Category / license / author:** `Accounting/Payment` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `mail`, `account`  
- **Source inventory:** 67 files; 21 Python, 21 XML, 0 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestChequeLifecycle` — `tests/test_cheque_lifecycle.py`; methods: `setUpClass()`, `test_01_create_received_cheque_draft_state()`, `test_02_create_issued_cheque_draft_state()`, `test_03_unique_cheque_number_constraint()`, `test_04_positive_amount_constraint()`, `test_05_received_lifecycle_full_cycle()`, `test_06_issued_lifecycle_full_cycle()`, `test_07_returned_cheque_with_charges_and_penalty()`, `test_08_issued_cheque_return_reversal()`, `test_09_void_issued_cheque()`, `test_10_post_dated_cheque_cannot_deposit_before_due()`, `test_11_max_redeposit_attempts_exceeded()` …
  - `ChequeReturnWizard` (`_name = cheque.return.wizard`) — `wizard/return_wizard.py`; fields: `cheque_id:Many2one`, `return_date:Date`, `return_reason_id:Many2one`, `bank_charges:Monetary`, `penalty_amount:Monetary`, `currency_id:Many2one`, `notes:Text`; methods: `action_submit_return()` …
  - `ChequeDepositWizard` (`_name = cheque.deposit.wizard`) — `wizard/deposit_wizard.py`; fields: `deposit_date:Date`, `bank_journal_id:Many2one`, `cheque_ids:Many2many`, `company_id:Many2one`; methods: `default_get()`, `action_create_deposit()`
  - `ChequePrintWizard` (`_name = cheque.print.wizard`) — `wizard/print_wizard.py`; fields: `report_type:Selection`, `cheque_ids:Many2many`; methods: `default_get()`, `action_print()`
  - `ChequeReturnReason` (`_name = cheque.return.reason`) — `models/return_reason.py`; fields: `name:Char`, `code:Char`, `sequence:Integer`, `active:Boolean`, `default_penalty:Monetary`, `currency_id:Many2one`, `company_id:Many2one`
  - `AccountPaymentMethod` extends `account.payment.method` — `models/account_payment_method.py`; fields: `cheque_tracking_enabled:Boolean`
  - `ChequeCheque` (`_name = cheque.cheque`) extends `mail.thread`, `mail.activity.mixin` — `models/cheque.py`; fields: `name:Char`, `cheque_type:Selection`, `cheque_number:Char`, `cheque_date:Date`, `due_date:Date`, `payee_name:Char`, `amount:Monetary`, `currency_id:Many2one`, `company_currency_id:Many2one`, `amount_company_currency:Monetary`, `exchange_rate:Float`, `partner_id:Many2one`, `bank_id:Many2one`, `bank_branch_id:Many2one`, `bank_account_id:Many2one`, `deposit_account_id:Many2one`, `invoice_ids:Many2many`, `deposit_id:Many2one` …; methods: `create()`, `write()`, `unlink()`, `action_receive()`, `action_deposit()`, `action_clear()`, `action_approve()`, `action_hand_over()`, `action_cash()`, `action_return()`, `action_void()`, `action_cancel()` …
  - `AccountMove` extends `account.move` — `models/account_move.py`; fields: `cheque_id:Many2one`, `cheque_return_id:Many2one`, `cheque_stage:Selection`
  - `ResCompany` extends `res.company` — `models/res_company.py`; fields: `cheque_received_account_id:Many2one`, `cheque_under_collection_account_id:Many2one`, `cheque_issued_account_id:Many2one`, `cheque_penalty_income_account_id:Many2one`, `cheque_bank_charges_account_id:Many2one`, `cheque_stale_months:Integer`, `cheque_pdc_reminder_days:Integer`, `cheque_max_redeposits:Integer`, `cheque_approval_threshold:Monetary`
  - `ChequeDeposit` (`_name = cheque.deposit`) extends `mail.thread` — `models/deposit.py`; fields: `name:Char`, `deposit_date:Date`, `bank_journal_id:Many2one`, `cheque_ids:Many2many`, `total_amount:Monetary`, `currency_id:Many2one`, `state:Selection`, `notes:Text`, `company_id:Many2one`; methods: `create()`, `action_confirm()`, `action_cancel()`, `action_print_slip()` …
  - `ChequeReturn` (`_name = cheque.return`) — `models/cheque_return.py`; fields: `name:Char`, `cheque_id:Many2one`, `return_date:Date`, `return_reason_id:Many2one`, `bank_charges:Monetary`, `penalty_amount:Monetary`, `currency_id:Many2one`, `company_id:Many2one`, `notes:Text`, `move_ids:One2many`
  - `ResPartner` extends `res.partner` — `models/res_partner.py`; fields: `received_cheque_count:Integer`, `issued_cheque_count:Integer`, `bounced_cheque_count:Integer`, `total_cheque_received:Monetary`, `total_cheque_issued:Monetary`, `company_currency_id:Many2one`; methods: `action_view_received_cheques()`, `action_view_issued_cheques()` …
  - `ResConfigSettings` extends `res.config.settings` — `models/res_config_settings.py`; fields: `cheque_received_account_id:Many2one`, `cheque_under_collection_account_id:Many2one`, `cheque_issued_account_id:Many2one`, `cheque_penalty_income_account_id:Many2one`, `cheque_bank_charges_account_id:Many2one`, `cheque_stale_months:Integer`, `cheque_pdc_reminder_days:Integer`, `cheque_max_redeposits:Integer`, `cheque_approval_threshold:Monetary`, `company_currency_id:Many2one`
  - `AccountPayment` extends `account.payment` — `models/account_payment.py`; fields: `cheque_id:Many2one`; methods: `_check_cheque_consistency()`, `_onchange_cheque_id()`
  - `AccountPaymentRegister` extends `account.payment.register` — `models/account_payment_register.py`; fields: `cheque_id:Many2one`; methods: `_create_payment_vals_from_wizard()`
- **Menu declarations:** `Cheque Tracking`, `Received`, `Received Cheques`, `Deposits`, `Issued`, `Issued Cheques`, `Operations`, `All Cheques`, `Returns`, `Configuration`, `Return Reasons`
- **View architectures detected:** calendar: 1, form: 7, graph: 1, kanban: 1, list: 4, pivot: 1, search: 3, xpath: 4
- **Record rules:** `Cheque: multi-company`, `Cheque Deposit: multi-company`, `Cheque Return: multi-company`, `Cheque Return Reason: multi-company`, `Cheque Return Reason: user company`
- **ACL entries:** `cheque.cheque user` (group `group_cheque_user/1/1/1`), `cheque.cheque manager` (group `group_cheque_manager/1/1/1`), `cheque.deposit user` (group `group_cheque_user/1/1/1`), `cheque.deposit manager` (group `group_cheque_manager/1/1/1`), `cheque.return user` (group `group_cheque_user/1/0/0`), `cheque.return manager` (group `group_cheque_manager/1/1/1`), `cheque.return.reason user` (group `group_cheque_user/1/0/0`), `cheque.return.reason manager` (group `group_cheque_manager/1/1/1`), `cheque.deposit.wizard user` (group `group_cheque_user/1/1/1`), `cheque.return.wizard user` (group `group_cheque_user/1/1/1`), `cheque.print.wizard user` (group `group_cheque_user/1/1/1`)
- **Functional file groups:** Wizards: `wizard/return_wizard.py`, `wizard/deposit_wizard.py`, `wizard/__init__.py`, `wizard/print_wizard_views.xml`, `wizard/return_wizard_views.xml`, `wizard/deposit_wizard_views.xml`, `wizard/print_wizard.py`; Reports: `report/report_cheque_print.xml`, `report/__init__.py`, `report/report_deposit_slip.xml`, `report/report_cheque_register.xml`; Security: `security/ir.rule.xml`, `security/ir.model.access.csv`, `security/groups.xml`; Data: `data/return_reason_data.xml`, `data/sequence_data.xml`, `data/ir_cron_data.xml`, `data/account_payment_method_data.xml`; Views: `views/cheque_views.xml`, `views/return_views.xml`, `views/menus.xml`, `views/account_payment_register_views.xml`, `views/return_reason_views.xml`, `views/partner_views.xml`, `views/res_config_settings_views.xml`, `views/account_payment_views.xml` …
- **Tests present:** `tests/__init__.py`, `tests/test_cheque_lifecycle.py`

### ODOO19 / `el_commission_type` — Commission Types

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Manage sales commission types by team member role  
- **Category / license / author:** `Sales` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `mail`  
- **Source inventory:** 38 files; 6 Python, 5 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `SalesCommissionType` (`_name = sales.commission.type`) extends `mail.thread`, `mail.activity.mixin` — `models/commission_type.py`; fields: `team_member_type:Selection`, `commission_percentage:Float`, `company_id:Many2one`, `name:Char`; methods: `name_get()` …
  - `SalesCommission` (`_name = sales.commission`) extends `mail.thread`, `mail.activity.mixin` — `models/sales_commission.py`; fields: `name:Char`, `partner_id:Many2one`, `team_member_type:Selection`, `commission_percentage:Float`, `company_id:Many2one`; methods: `_compute_name()`
  - `ResPartner` extends `res.partner` — `models/res_partner.py`; fields: `sales_commission_type:Many2one`
- **Menu declarations:** `Commissions`, `Commissions`, `Commission Types`
- **View architectures detected:** form: 2, list: 2, search: 2, xpath: 1
- **ACL entries:** `sales.commission.type.all` (group `base.group_user/1/0/0`), `sales.commission.type.user` (group `group_commission_user/1/1/1`), `sales.commission.type.manager` (group `group_commission_manager/1/1/1`), `sales.commission.all` (group `base.group_user/1/0/0`), `sales.commission.user` (group `group_commission_user/1/1/1`), `sales.commission.manager` (group `group_commission_manager/1/1/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`, `security/security.xml`; Views: `views/res_partner_views.xml`, `views/menu.xml`, `views/commission_type_views.xml`, `views/sales_commission_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `el_construction_management` — Construction Management

- **Manifest version:** `19.0.1.24.0`  
- **Summary:** Construction Management | Job Costing | BOQ | Work Orders | RA Billing | Material Requisition | Subcontracting | Budget  
- **Category / license / author:** `Construction` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `mail`, `contacts`, `hr`, `stock`, `stock_account`, `purchase`, `account`, `project`, `web_gantt`  
- **Source inventory:** 111 files; 58 Python, 26 XML, 1 JavaScript, 0 SCSS; 10 test files.  
- **Python classes / models:**
  - `TestConstructionTask` — `tests/test_task.py`; methods: `setUpClass()`, `test_workflow_transitions_and_guards()`, `test_cancel_and_reset_workflow()`, `test_direct_state_write_is_blocked()`, `test_invalid_subproject_is_blocked()`, `test_progress_and_remaining_hours()`, `test_planned_hours_completion_uses_actual_logged_hours()`, `test_timer_only_in_progress()`, `test_timer_lifecycle()`, `test_running_timesheet_cannot_be_created_directly()`, `test_timesheet_cannot_be_added_to_closed_task()`, `test_completed_task_cannot_be_deleted()` …
  - `TestConstructionTaskGanttDependencies` — `tests/test_task.py`; methods: `setUpClass()`, `test_finish_to_start_dependency_is_allowed()`, `test_dependency_rejects_early_successor()`, `test_dependency_rejects_cross_project()`, `test_dependency_rejects_cycle()` …
  - `TestConstructionTaskAdvancedPlanning` — `tests/test_task.py`; methods: `setUpClass()`, `test_baseline_snapshot()`, `test_milestone_requires_single_day()`, `test_critical_path_and_slack()`, `test_project_schedule_action()`, `test_baseline_and_actual_fields_are_server_protected()`, `test_non_manager_cannot_set_actual_finish_through_done()` …
  - `TestBudgetCosting` — `tests/test_budget_costing.py`; methods: `test_same_product_lines_do_not_overwrite()`
  - `TestMaterialRequisition` — `tests/test_mreq.py`; methods: `test_purchase_order_requires_approval()`
  - `TestConstructionHardening` — `tests/test_hardening.py`; methods: `setUpClass()`, `test_forged_workflow_context_cannot_change_state()`, `test_subcontract_line_amount_is_contract_amount()`, `test_subcontract_lines_locked_after_confirmation()`, `test_ra_completion_percentage_affects_amount()`, `test_invalid_company_reference_is_rejected()`
  - `TestBilling` — `tests/test_billing.py`; methods: `test_progress_billing_requires_in_progress_for_invoice()`
  - `TestRound2Hardening` — `tests/test_round2_hardening.py`; methods: `setUpClass()`, `test_mreq_rejects_partial_vendor_assignment()`, `test_work_order_other_line_is_in_total()`, `test_ra_billing_numbers_increment_per_subcontract()`, `test_ra_billing_line_parent_is_required()`
  - `TestBudgetMethods` — `tests/test_budget_methods.py`; methods: `setUpClass()`, `test_project_total_budget()`, `test_lines_budget()`, `test_hybrid_budget_tracks_unallocated_balance()`, `test_hybrid_cannot_over_allocate()`, `test_lines_method_rejects_project_amount()`, `test_project_and_hybrid_require_project_amount()` …
  - `TestConstructionQualityCheck` — `tests/test_quality_check.py`; methods: `setUpClass()`, `test_workflow_pass_close()`, `test_start_requires_inspector_and_checkpoints()`, `test_result_requires_completed_checkpoints()`, `test_fail_requires_failed_point_action_and_recheck_date()`, `test_reinspection_can_pass()`, `test_direct_state_change_is_blocked()`, `test_closed_quality_check_is_read_only()`, `test_cancel_and_reset_are_manager_only()` …
  - `TestConstructionWorkflow` — `tests/test_workflow.py`; methods: `test_budget_direct_state_write_is_blocked()`
  - `ConstructionWorkType` (`_name = el_construction.work.type`) — `models/construction_configuration.py`; fields: `name:Char`, `code:Char`, `description:Text`, `sub_type_ids:One2many`, `active:Boolean`
  - `ConstructionWorkSubType` (`_name = el_construction.work.sub.type`) — `models/construction_configuration.py`; fields: `name:Char`, `code:Char`, `work_type_id:Many2one`, `description:Text`, `active:Boolean`
  - `ConstructionProject` (`_name = el_construction.project`) extends `mail.thread`, `mail.activity.mixin` — `models/construction_project.py`; fields: `name:Char`, `reference:Char`, `warehouse_id:Many2one`, `company_id:Many2one`, `street:Char`, `street2:Char`, `city:Char`, `state_id:Many2one`, `zip:Char`, `country_id:Many2one`, `date_start:Date`, `date_end:Date`, `longitude:Float`, `latitude:Float`, `phone:Char`, `mobile:Char`, `email:Char`, `active:Boolean` …; methods: `create()`, `write()`, `unlink()`, `action_archive()`, `action_unarchive()`, `action_start()`, `action_complete()`, `action_short_close()`, `action_reset_draft()`, `action_view_sub_projects()`, `action_view_budgets()`, `action_view_work_orders()` …
  - `ConstructionProjectImage` (`_name = el_construction.project.image`) — `models/construction_project.py`; fields: `project_id:Many2one`, `name:Char`, `image:Binary`
  - `ConstructionBoqLine` (`_name = el_construction.boq.line`) — `models/construction_boq_lines.py`; fields: `boq_id:Many2one`, `budget_line_ids:One2many`, `product_id:Many2one`, `description:Char`, `quantity:Float`, `uom_id:Many2one`, `unit_price:Float`, `amount:Float`; methods: `create()`, `write()`, `unlink()` …
  - `ConstructionSubcontract` (`_name = el_construction.subcontract`) extends `mail.thread`, `mail.activity.mixin` — `models/construction_subcontract.py`; fields: `name:Char`, `project_id:Many2one`, `sub_project_id:Many2one`, `partner_id:Many2one`, `company_id:Many2one`, `date:Date`, `date_start:Date`, `date_end:Date`, `work_description:Text`, `state:Selection`, `line_ids:One2many`, `consume_order_ids:One2many`, `consume_order_count:Integer`, `ra_billing_ids:One2many`, `ra_billing_count:Integer`, `contract_amount:Float`, `billed_amount:Float`, `remaining_amount:Float` …; methods: `create()`, `write()`, `action_confirm()`, `action_start()`, `action_complete()`, `action_cancel()`, `action_reset_draft()`, `action_view_consume_orders()`, `action_view_ra_billings()`, `action_create_bill()` …
  - `ConstructionSubcontractLine` (`_name = el_construction.subcontract.line`) — `models/construction_subcontract.py`; fields: `subcontract_id:Many2one`, `work_description:Char`, `description:Char`, `product_id:Many2one`, `quantity:Float`, `uom_id:Many2one`, `rate:Float`, `amount:Float`; methods: `create()`, `write()`, `unlink()` …
  - `ConstructionMaterialRequisitionLineInventory` extends `el_construction.material.requisition.line` — `models/construction_material_inventory_controls.py`; fields: `issue_line_ids:One2many`, `issued_qty:Float`, `consumed_qty:Float`, `returned_qty:Float`, `wastage_qty:Float`, `received_qty:Float`, `remaining_to_issue:Float`, `allowed_wastage_pct:Float`, `allowed_wastage_qty:Float`, `site_on_hand_qty:Float`; methods: `_compute_allowed_wastage_qty()`, `_compute_stock_quantities()`, `_compute_received_qty()`, `_compute_site_on_hand_qty()`
  - `ConstructionQualityCheckLine` (`_name = el_construction.quality.check.line`) — `models/construction_quality_check_lines.py`; fields: `quality_check_id:Many2one`, `sequence:Integer`, `name:Char`, `description:Text`, `standard:Char`, `result:Selection`, `remarks:Text`; methods: `create()`, `write()`, `unlink()` …
  - `ConstructionQualityCheckImage` (`_name = el_construction.quality.check.image`) — `models/construction_quality_check_lines.py`; fields: `quality_check_id:Many2one`, `name:Char`, `image:Binary`; methods: `create()`, `write()`, `unlink()` …
  - `ConstructionProgressBillingControls` extends `el_construction.progress.billing` — `models/construction_billing_controls.py`; fields: `commercial_status:Selection`, `retention_percent:Float`, `advance_recovery:Monetary`, `other_deductions:Monetary`, `net_commercial_amount:Monetary`, `retention_amount:Monetary`, `currency_id:Many2one`; methods: `_compute_commercial_amounts()`, `_check_commercial()`
  - `ConstructionRaBillingLineControls` extends `el_construction.ra.billing.line` — `models/construction_billing_controls.py`; fields: `previous_quantity:Float`, `current_quantity:Float`, `cumulative_quantity:Float`, `remaining_quantity:Float`; methods: `_compute_cumulative_controls()`, `_check_cumulative_quantity()`
  - `ConstructionRaCommercialControls` extends `el_construction.ra.billing` — `models/construction_billing_controls.py`; fields: `retention_percent:Float`, `retention_amount:Float`, `advance_recovery:Float`, `other_deductions:Float`, `net_certified_amount:Float`; methods: `_compute_ra_commercial()`, `_check_ra_commercial()`
  - `ConstructionConsumeOrder` (`_name = el_construction.consume.order`) extends `mail.thread` — `models/construction_consume_order.py`; fields: `name:Char`, `subcontract_id:Many2one`, `project_id:Many2one`, `sub_project_id:Many2one`, `company_id:Many2one`, `date:Date`, `state:Selection`, `line_ids:One2many`, `notes:Text`; methods: `create()`, `write()`, `action_confirm()`, `action_done()`, `action_cancel()` …
  - `ConstructionConsumeOrderLine` (`_name = el_construction.consume.order.line`) — `models/construction_consume_order.py`; fields: `consume_order_id:Many2one`, `product_id:Many2one`, `description:Char`, `quantity:Float`, `uom_id:Many2one`; methods: `_onchange_product_id()`
  - `ConstructionCostEntry` (`_name = el_construction.cost.entry`) — `models/construction_cost.py`; fields: `name:Char`, `project_id:Many2one`, `sub_project_id:Many2one`, `company_id:Many2one`, `currency_id:Many2one`, `date:Date`, `cost_type:Selection`, `cost_category:Selection`, `amount:Monetary`, `analytic_account_id:Many2one`, `source_model:Char`, `source_res_id:Integer`, `source_ref:Char`, `notes:Text`; methods: `create_from_source()` …
  - `ConstructionMaterialIssue` (`_name = el_construction.material.issue`) extends `mail.thread`, `mail.activity.mixin` — `models/construction_material_issue.py`; fields: `name:Char`, `issue_type:Selection`, `state:Selection`, `project_id:Many2one`, `sub_project_id:Many2one`, `work_order_id:Many2one`, `task_id:Many2one`, `material_requisition_id:Many2one`, `warehouse_id:Many2one`, `source_location_id:Many2one`, `destination_location_id:Many2one`, `picking_id:Many2one`, `scrap_id:Many2one`, `company_id:Many2one`, `date:Date`, `notes:Text`, `actual_cost:Monetary`, `company_currency_id:Many2one` …; methods: `create()`, `write()`, `action_confirm()`, `action_done()`, `action_cancel()`, `action_create_reversal()`, `action_create_consumption()`, `action_create_return()`, `action_create_wastage()`, `action_view_stock_document()` …
  - `ConstructionMaterialIssueLine` (`_name = el_construction.material.issue.line`) — `models/construction_material_issue.py`; fields: `issue_id:Many2one`, `material_requisition_line_id:Many2one`, `stock_move_id:Many2one`, `scrap_id:Many2one`, `product_id:Many2one`, `description:Char`, `quantity:Float`, `uom_id:Many2one`, `available_qty:Float`; methods: `write()`, `create()` …
  - `ConstructionPhase` (`_name = el_construction.phase`) extends `mail.thread`, `mail.activity.mixin` — `models/construction_phase.py`; fields: `name:Char`, `title:Char`, `project_id:Many2one`, `sub_project_id:Many2one`, `company_id:Many2one`, `sequence:Integer`, `parent_id:Many2one`, `child_ids:One2many`, `date_start:Date`, `date_end:Date`, `material_cost:Float`, `equipment_cost:Float`, `labour_cost:Float`, `overhead_cost:Float`, `total_cost:Float`, `state:Selection`, `work_order_ids:One2many`, `work_order_count:Integer` …; methods: `create()`, `write()`, `action_start()`, `action_complete()`, `action_hold()`, `action_reset_draft()`, `action_view_work_orders()` …
  - `ConstructionPhaseEntry` (`_name = el_construction.phase.entry`) — `models/construction_phase.py`; fields: `phase_id:Many2one`, `date:Date`, `description:Text`, `entry_type:Selection`, `product_id:Many2one`, `quantity:Float`, `unit_price:Float`, `amount:Float`; methods: `_check_values()`, `_compute_amount()`
  - `ConstructionRateAnalysis` (`_name = el_construction.rate.analysis`) extends `mail.thread`, `mail.activity.mixin` — `models/construction_rate_analysis.py`; fields: `name:Char`, `title:Char`, `project_id:Many2one`, `company_id:Many2one`, `sub_project_id:Many2one`, `date:Date`, `work_type_id:Many2one`, `work_sub_type_id:Many2one`, `uom_id:Many2one`, `per_unit:Char`, `material_line_ids:One2many`, `equipment_line_ids:One2many`, `labour_line_ids:One2many`, `overhead_line_ids:One2many`, `other_line_ids:One2many`, `material_total:Float`, `equipment_total:Float`, `labour_total:Float` …; methods: `create()` …
  - `ConstructionRateAnalysisLine` (`_name = el_construction.rate.analysis.line`) — `models/construction_rate_analysis.py`; fields: `rate_analysis_id:Many2one`, `line_type:Selection`, `product_id:Many2one`, `description:Char`, `quantity:Float`, `uom_id:Many2one`, `unit_price:Float`, `amount:Float`; methods: `_check_values()`, `_compute_amount()`, `_onchange_product_id()`
  - `ConstructionSubProjectDocument` (`_name = el_construction.sub.project.document`) — `models/construction_sub_project_documents.py`; fields: `sub_project_id:Many2one`, `name:Char`, `document:Binary`, `document_name:Char`, `doc_type:Selection`, `notes:Text`
  - `ConstructionVariationOrder` (`_name = el_construction.variation.order`) extends `mail.thread`, `mail.activity.mixin` — `models/construction_variation.py`; fields: `name:Char`, `project_id:Many2one`, `sub_project_id:Many2one`, `company_id:Many2one`, `currency_id:Many2one`, `date:Date`, `reason:Text`, `description:Text`, `state:Selection`, `line_ids:One2many`, `amount:Monetary`, `approved_by:Many2one`, `approved_on:Datetime`, `approval_line_ids:One2many`; methods: `create()`, `write()`, `action_submit()`, `action_approve()`, `action_reject()`, `action_cancel()` …
  - `ConstructionVariationApproval` (`_name = el_construction.variation.approval`) — `models/construction_variation.py`; fields: `variation_id:Many2one`, `matrix_id:Many2one`, `user_id:Many2one`, `approved_on:Datetime`; methods: `create()`, `write()`, `unlink()` …
  - `ConstructionVariationOrderLine` (`_name = el_construction.variation.order.line`) — `models/construction_variation.py`; fields: `variation_id:Many2one`, `boq_line_id:Many2one`, `product_id:Many2one`, `description:Char`, `quantity:Float`, `unit_price:Float`, `amount:Float`; methods: `write()`, `create()`, `unlink()` …
  - `ConstructionBudgetLine` (`_name = el_construction.budget.line`) — `models/construction_budget_lines.py`; fields: `budget_id:Many2one`, `project_id:Many2one`, `sub_project_id:Many2one`, `company_id:Many2one`, `boq_line_id:Many2one`, `work_type_id:Many2one`, `work_sub_type_id:Many2one`, `product_id:Many2one`, `description:Char`, `quantity:Float`, `uom_id:Many2one`, `unit_price:Float`, `planned_amount:Float`, `actual_amount:Float`, `variance:Float`, `progress:Float`; methods: `create()`, `write()`, `unlink()`, `action_recompute_actual()` …
  - `ConstructionRaBilling` (`_name = el_construction.ra.billing`) extends `mail.thread` — `models/construction_ra_billing.py`; fields: `name:Char`, `subcontract_id:Many2one`, `project_id:Many2one`, `sub_project_id:Many2one`, `company_id:Many2one`, `partner_id:Many2one`, `date:Date`, `billing_no:Integer`, `state:Selection`, `line_ids:One2many`, `total_amount:Float`, `previous_amount:Float`, `current_amount:Float`, `cumulative_amount:Float`, `remaining_contract:Float`, `notes:Text`; methods: `create()`, `write()`, `action_submit()`, `action_approve()`, `action_reject()`, `action_reset_draft()` …
  - `ConstructionRaBillingLine` (`_name = el_construction.ra.billing.line`) — `models/construction_ra_billing.py`; fields: `ra_billing_id:Many2one`, `description:Char`, `budget_line_id:Many2one`, `quantity:Float`, `uom_id:Many2one`, `rate:Float`, `amount:Float`, `completion_percentage:Float`; methods: `create()`, `write()`, `unlink()` …
  - `ConstructionExtraExpense` (`_name = el_construction.extra.expense`) extends `mail.thread` — `models/construction_extra_expense.py`; fields: `name:Char`, `project_id:Many2one`, `sub_project_id:Many2one`, `company_id:Many2one`, `date:Date`, `description:Text`, `expense_type:Selection`, `product_id:Many2one`, `budget_line_id:Many2one`, `quantity:Float`, `unit_price:Float`, `amount:Float`, `state:Selection`, `approved_by:Many2one`, `source_move_line_id:Many2one`, `notes:Text`; methods: `create()`, `write()`, `action_confirm()`, `action_approve()`, `action_cancel()`, `action_reset_draft()` …
  - `ConstructionWorkOrder` (`_name = el_construction.work.order`) extends `mail.thread`, `mail.activity.mixin` — `models/construction_work_order.py`; fields: `name:Char`, `project_id:Many2one`, `sub_project_id:Many2one`, `phase_id:Many2one`, `company_id:Many2one`, `date:Date`, `date_start:Date`, `date_end:Date`, `responsible_id:Many2one`, `description:Text`, `state:Selection`, `material_line_ids:One2many`, `equipment_line_ids:One2many`, `labour_line_ids:One2many`, `overhead_line_ids:One2many`, `other_line_ids:One2many`, `material_total:Float`, `equipment_total:Float` …; methods: `create()`, `write()`, `action_confirm()`, `action_start()`, `action_done()`, `action_cancel()`, `action_reset_draft()` …
  - `ConstructionWorkOrderLine` (`_name = el_construction.work.order.line`) — `models/construction_work_order.py`; fields: `work_order_id:Many2one`, `line_type:Selection`, `product_id:Many2one`, `budget_line_id:Many2one`, `description:Char`, `quantity:Float`, `uom_id:Many2one`, `unit_price:Float`, `amount:Float`; methods: `create()`, `write()`, `unlink()` …
  - `PurchaseOrder` extends `purchase.order` — `models/integrations/purchase.py`; fields: `material_requisition_id:Many2one`
  - `PurchaseOrderLine` extends `purchase.order.line` — `models/integrations/purchase.py`; fields: `material_requisition_line_id:Many2one`
  - `ConstructionStockMove` extends `stock.move` — `models/integrations/stock.py`; fields: `construction_material_issue_id:Many2one`, `material_requisition_line_id:Many2one`; methods: `_create_construction_actual_cost_entry()`
  - `ConstructionStockPicking` extends `stock.picking` — `models/integrations/stock.py`; fields: `construction_material_issue_id:Many2one`, `material_requisition_id:Many2one`; methods: `_action_done()`
  - `ConstructionStockScrap` extends `stock.scrap` — `models/integrations/stock.py`; fields: `construction_material_issue_id:Many2one`; methods: `action_validate()`
  - `AccountMove` extends `account.move` — `models/integrations/account.py`; fields: `construction_subcontract_id:Many2one`, `construction_progress_billing_id:Many2one`; methods: `action_post()` …
  - `ConstructionWorkflowMixin` — `models/workflow_mixin.py`; methods: `create()`, `write()` …
  - `ConstructionQualityPoint` (`_name = el_construction.quality.point`) — `models/construction_quality_point.py`; fields: `name:Char`, `sequence:Integer`, `project_id:Many2one`, `company_id:Many2one`, `check_type:Selection`, `description:Text`, `standard:Char`, `active:Boolean`
  - `ConstructionQualityCheckQualityPointExtension` extends `el_construction.quality.check` — `models/construction_quality_point.py`; methods: `action_load_project_quality_points()`
  - `ConstructionBOQRevision` (`_name = el_construction.boq.revision`) — `models/construction_revisions.py`; fields: `name:Char`, `boq_id:Many2one`, `project_id:Many2one`, `company_id:Many2one`, `revision_no:Integer`, `state:Selection`, `reason:Text`, `line_ids:One2many`, `approved_by:Many2one`, `approved_on:Datetime`; methods: `write()`, `action_approve()`, `action_cancel()`
  - `ConstructionBOQRevisionLine` (`_name = el_construction.boq.revision.line`) — `models/construction_revisions.py`; fields: `revision_id:Many2one`, `source_line_id:Many2one`, `description:Char`, `quantity:Float`, `unit_price:Float`, `amount:Float`; methods: `create()`, `write()`, `unlink()` …
  - `ConstructionBudgetRevision` (`_name = el_construction.budget.revision`) — `models/construction_revisions.py`; fields: `name:Char`, `budget_id:Many2one`, `project_id:Many2one`, `company_id:Many2one`, `revision_no:Integer`, `state:Selection`, `reason:Text`, `total_amount:Monetary`, `currency_id:Many2one`, `line_ids:One2many`; methods: `write()`, `action_approve()`, `action_cancel()` …
  - `ConstructionBudgetRevisionLine` (`_name = el_construction.budget.revision.line`) — `models/construction_revisions.py`; fields: `revision_id:Many2one`, `source_line_id:Many2one`, `description:Char`, `quantity:Float`, `unit_price:Float`, `amount:Monetary`, `currency_id:Many2one`; methods: `create()`, `write()`, `unlink()` …
  - `ConstructionTaskBaselineRevision` (`_name = el_construction.task.baseline.revision`) — `models/construction_revisions.py`; fields: `name:Char`, `project_id:Many2one`, `company_id:Many2one`, `revision_no:Integer`, `state:Selection`, `reason:Text`, `line_ids:One2many`; methods: `write()`, `action_approve()`, `action_cancel()`
  - `ConstructionTaskBaselineRevisionLine` (`_name = el_construction.task.baseline.revision.line`) — `models/construction_revisions.py`; fields: `revision_id:Many2one`, `task_id:Many2one`, `baseline_start:Date`, `baseline_end:Date`, `baseline_hours:Float`; methods: `create()`, `write()`, `unlink()` …
  - `ConstructionBOQRevisionActions` extends `el_construction.boq` — `models/construction_revisions.py`; methods: `action_create_revision()`
  - `ConstructionBudgetRevisionActions` extends `el_construction.budget` — `models/construction_revisions.py`; methods: `action_create_revision()`
  - `ConstructionProgressBillingLine` (`_name = el_construction.progress.billing.line`) — `models/construction_progress_billing_lines.py`; fields: `billing_id:Many2one`, `line_type:Selection`, `product_id:Many2one`, `description:Char`, `quantity:Float`, `uom_id:Many2one`, `unit_price:Float`, `tax_ids:Many2many`, `tax_amount:Float`, `total_amount:Float`; methods: `create()`, `write()`, `unlink()` …
  - `ConstructionBudget` (`_name = el_construction.budget`) extends `mail.thread`, `mail.activity.mixin` — `models/construction_budget.py`; fields: `name:Char`, `project_id:Many2one`, `sub_project_id:Many2one`, `company_id:Many2one`, `date:Date`, `notes:Text`, `budget_method:Selection`, `project_budget_amount:Float`, `state:Selection`, `line_ids:One2many`, `total_planned:Float`, `allocated_amount:Float`, `unallocated_amount:Float`, `allocation_percentage:Float`, `total_actual:Float`, `total_variance:Float`; methods: `create()`, `write()`, `action_confirm()`, `action_approve()`, `action_done()`, `action_cancel()`, `action_reset_draft()`, `action_recompute_actual()` …
  - `ConstructionMaterialRequisition` (`_name = el_construction.material.requisition`) extends `mail.thread`, `mail.activity.mixin` — `models/construction_material_requisition.py`; fields: `name:Char`, `project_id:Many2one`, `sub_project_id:Many2one`, `work_order_id:Many2one`, `company_id:Many2one`, `date:Date`, `required_date:Date`, `requested_by:Many2one`, `approved_by:Many2one`, `department_id:Many2one`, `warehouse_id:Many2one`, `state:Selection`, `line_ids:One2many`, `notes:Text`, `rejection_reason:Text`, `purchase_order_count:Integer`, `purchase_order_ids:Many2many`, `purchase_order_link_ids:One2many` …; methods: `create()`, `write()`, `action_submit_approval()`, `action_approve()`, `action_in_progress()`, `action_ready()`, `action_withdrawal()`, `action_done()`, `action_reject()`, `action_cancel()`, `action_reset_draft()`, `action_create_purchase_order()` …
  - `ConstructionMaterialRequisitionLine` (`_name = el_construction.material.requisition.line`) — `models/construction_material_requisition.py`; fields: `requisition_id:Many2one`, `purchase_order_line_ids:One2many`, `stock_move_ids:One2many`, `product_id:Many2one`, `description:Char`, `quantity:Float`, `uom_id:Many2one`, `unit_price:Float`, `amount:Float`, `vendor_id:Many2one`, `vendor_domain_ids:Many2many`, `notes:Char`; methods: `write()`, `unlink()`, `create()` …
  - `ConstructionProgressBilling` (`_name = el_construction.progress.billing`) extends `mail.thread`, `mail.activity.mixin` — `models/construction_progress_billing.py`; fields: `name:Char`, `reference:Char`, `project_id:Many2one`, `sub_project_id:Many2one`, `company_id:Many2one`, `date:Date`, `partner_id:Many2one`, `invoice_type:Selection`, `phase_id:Many2one`, `work_order_id:Many2one`, `include_material:Boolean`, `include_equipment:Boolean`, `include_labour:Boolean`, `include_overhead:Boolean`, `include_other:Boolean`, `state:Selection`, `material_line_ids:One2many`, `equipment_line_ids:One2many` …; methods: `create()`, `write()`, `action_load_work_order_lines()`, `action_start()`, `action_complete()`, `action_reset_draft()`, `action_create_invoice()`, `action_view_invoices()` …
  - `ConstructionReportWizard` (`_name = el_construction.report.wizard`) — `models/construction_report_wizard.py`; fields: `report_type:Selection`, `output_format:Selection`, `project_id:Many2one`, `date_from:Date`, `date_to:Date`, `include_archived:Boolean`; methods: `default_get()`, `action_print()` …
  - `ConstructionReportMenuWizard` (`_name = el_construction.report.menu.wizard`) — `models/construction_report_wizard.py`; fields: `report_type:Selection`, `output_format:Selection`, `project_id:Many2one`, `date_from:Date`, `date_to:Date`; methods: `action_print()`
  - `ConstructionQualityCheck` (`_name = el_construction.quality.check`) extends `mail.thread`, `mail.activity.mixin` — `models/construction_quality_check.py`; fields: `name:Char`, `project_id:Many2one`, `sub_project_id:Many2one`, `phase_id:Many2one`, `work_order_id:Many2one`, `company_id:Many2one`, `date:Date`, `inspector_id:Many2one`, `inspection_method:Selection`, `check_type:Selection`, `state:Selection`, `check_line_ids:One2many`, `result_notes:Text`, `corrective_action:Text`, `recheck_date:Date`, `closed_date:Date`, `closed_by_id:Many2one`, `document:Binary` …; methods: `create()`, `write()`, `unlink()`, `action_start()`, `action_pass()`, `action_fail()`, `action_conditional()`, `action_recheck()`, `action_close()`, `action_cancel()`, `action_reset_draft()` …
  - `ConstructionMaterialRequisitionControls` extends `el_construction.material.requisition` — `models/construction_material_controls.py`; fields: `procurement_stage:Selection`, `committed_amount:Monetary`, `received_amount:Monetary`, `currency_id:Many2one`, `site_location_id:Many2one`, `stock_operation_ids:One2many`, `stock_operation_count:Integer`; methods: `action_submit_approval()`, `action_approve()`, `action_create_purchase_order()`, `action_create_internal_transfer()`, `action_done()`, `action_create_material_issue()`, `action_view_stock_operations()`, `action_create_consumption()`, `action_create_return()`, `action_create_wastage()` …
  - `ConstructionBoq` (`_name = el_construction.boq`) extends `mail.thread`, `mail.activity.mixin` — `models/construction_boq.py`; fields: `name:Char`, `state:Selection`, `project_id:Many2one`, `sub_project_id:Many2one`, `company_id:Many2one`, `work_type_id:Many2one`, `work_sub_type_id:Many2one`, `length:Float`, `width:Float`, `height:Float`, `nos:Float`, `quantity:Float`, `uom_id:Many2one`, `description:Text`, `line_ids:One2many`, `total_amount:Float`; methods: `create()`, `write()`, `action_approve()`, `action_lock()`, `action_cancel()`, `action_reset_draft()`, `action_create_budget()` …
  - `ConstructionProjectControls` extends `el_construction.project` — `models/construction_project_controls.py`; fields: `site_location_id:Many2one`, `consumption_location_id:Many2one`, `material_issue_ids:One2many`, `material_issue_count:Integer`, `enforce_closure_gates:Boolean`, `closure_gate_summary:Text`, `variation_order_ids:One2many`, `cost_entry_ids:One2many`, `approved_variation_amount:Monetary`, `committed_cost:Monetary`, `actual_cost:Monetary`, `forecast_cost:Monetary`, `currency_id:Many2one`, `analytic_account_id:Many2one`; methods: `action_initialize_stock_locations()`, `action_view_material_issues()`, `write()`, `action_complete()`, `action_rebuild_cost_snapshot()`, `dashboard_snapshot()`, `action_create_baseline_revision()` …
  - `ConstructionSubProject` (`_name = el_construction.sub.project`) extends `mail.thread`, `mail.activity.mixin` — `models/construction_sub_project.py`; fields: `name:Char`, `reference:Char`, `project_id:Many2one`, `warehouse_id:Many2one`, `company_id:Many2one`, `date_start:Date`, `date_end:Date`, `state:Selection`, `partner_id:Many2one`, `boq_ids:One2many`, `engineer_ids:Many2many`, `document_ids:One2many`, `handover_checklist_complete:Boolean`, `client_acceptance:Boolean`, `handover_notes:Text`, `handover_date:Date`, `handover_by:Many2one`, `insurance_company:Char` …; methods: `create()`, `write()`, `action_planning()`, `action_procurement()`, `action_construction()`, `action_handover()`, `action_view_tasks()`, `action_view_phases()`, `action_view_work_orders()`, `action_view_mreq()`, `action_view_boq()`, `action_view_billings()` …
  - `ConstructionNCR` (`_name = el_construction.ncr`) extends `mail.thread`, `mail.activity.mixin` — `models/construction_quality_controls.py`; fields: `name:Char`, `project_id:Many2one`, `sub_project_id:Many2one`, `quality_check_id:Many2one`, `company_id:Many2one`, `date:Date`, `description:Text`, `severity:Selection`, `state:Selection`, `capa_ids:One2many`, `root_cause:Text`, `verified_by:Many2one`, `closed_by:Many2one`; methods: `create()`, `action_open()`, `action_start_capa()`, `action_verify()`, `action_close()`, `action_cancel()`
  - `ConstructionCAPA` (`_name = el_construction.capa`) — `models/construction_quality_controls.py`; fields: `ncr_id:Many2one`, `project_id:Many2one`, `company_id:Many2one`, `name:Char`, `action_type:Selection`, `owner_id:Many2one`, `deadline:Date`, `state:Selection`, `completion_notes:Text`; methods: `write()`, `action_done()`, `action_cancel()`
  - `ConstructionTask` (`_name = el_construction.task`) extends `mail.thread`, `mail.activity.mixin` — `models/construction_task.py`; fields: `name:Char`, `reference:Char`, `project_id:Many2one`, `sub_project_id:Many2one`, `phase_id:Many2one`, `work_order_id:Many2one`, `company_id:Many2one`, `sequence:Integer`, `description:Html`, `assigned_to:Many2one`, `department_id:Many2one`, `date_start:Date`, `date_end:Date`, `date_deadline:Date`, `priority:Selection`, `state:Selection`, `progress:Float`, `planned_hours:Float` …; methods: `action_set_baseline()`, `create()`, `write()`, `unlink()`, `action_start()`, `action_done()`, `action_cancel()`, `action_reset_draft()`, `action_timer_start()`, `action_timer_stop()` …
  - `ConstructionTimesheet` (`_name = el_construction.timesheet`) — `models/construction_task.py`; fields: `task_id:Many2one`, `project_id:Many2one`, `company_id:Many2one`, `employee_id:Many2one`, `date:Date`, `hours:Float`, `description:Char`, `is_internal:Boolean`, `state:Selection`; methods: `create()`, `write()`, `unlink()` …
  - `ConstructionApprovalMatrix` (`_name = el_construction.approval.matrix`) — `models/construction_approval.py`; fields: `name:Char`, `active:Boolean`, `sequence:Integer`, `model_name:Selection`, `company_id:Many2one`, `amount_from:Monetary`, `amount_to:Monetary`, `currency_id:Many2one`, `approver_ids:Many2many`, `required_approvals:Integer`; methods: `get_approval_matrix()` …
  - `ConstructionTaskControls` extends `el_construction.task` — `models/construction_task_controls.py`; fields: `progress_mode:Selection`, `planned_quantity:Float`, `completed_quantity:Float`, `quantity_uom_id:Many2one`, `physical_progress:Float`; methods: `_compute_physical_progress()`, `_compute_progress()`
  - `ConstructionPermit` (`_name = el_construction.permit`) — `models/construction_permit.py`; fields: `project_id:Many2one`, `company_id:Many2one`, `name:Char`, `is_required_for_execution:Boolean`, `permit_type:Selection`, `issue_date:Date`, `expiry_date:Date`, `issuing_authority:Char`, `document:Binary`, `document_name:Char`, `state:Selection`, `notes:Text`; methods: `write()`, `action_approve()`, `action_reject()`, `action_expire()`, `action_reset_pending()` …
- **Menu declarations:** `Construction`, `Dashboard`, `Projects`, `Projects`, `Sub Projects`, `Planning & Execution`, `Phases / WBS`, `Tasks`, `Schedule`, `Work Orders`, `Commercial & Cost`, `Bill of Quantities`, `Budgets`, `Rate Analysis`, `Progress Billing`, `Contracts`, `Subcontracting`, `Consume Orders`, `RA Billings`, `Extra Expenses` …
- **View architectures detected:** form: 23, gantt: 1, kanban: 1, list: 26, search: 14, xpath: 4
- **Record rules:** `Construction Project Company`, `Construction Sub Project Company`, `Construction BOQ Company`, `Construction Budget Company`, `Construction Work Order Company`, `Construction Material Requisition Company`, `Construction Subcontract Company`, `Construction Progress Billing Company`, `Construction Phase Company`, `Construction Quality Check Company`, `Construction Task Company`, `Construction Extra Expense Company`, `Construction Quality Point Company`, `Construction RA Billing Company`, `Construction Approval Matrix Company`, `Construction Variation Approval Company`, `Construction BOQ Revision Company`, `Construction BOQ Revision Line Company`, `Construction Budget Revision Company`, `Construction Budget Revision Line Company` …
- **ACL entries:** `construction.project.user` (group `group_construction_user/1/1/1`), `construction.project.manager` (group `group_construction_manager/1/1/1`), `construction.project.image.user` (group `group_construction_user/1/1/1`), `construction.project.image.manager` (group `group_construction_manager/1/1/1`), `construction.permit.user` (group `group_construction_user/1/1/1`), `construction.permit.manager` (group `group_construction_manager/1/1/1`), `construction.sub.project.user` (group `group_construction_user/1/1/1`), `construction.sub.project.manager` (group `group_construction_manager/1/1/1`), `construction.sub.project.document.user` (group `group_construction_user/1/1/1`), `construction.sub.project.document.manager` (group `group_construction_manager/1/1/1`), `construction.boq.user` (group `group_construction_user/1/1/1`), `construction.boq.manager` (group `group_construction_manager/1/1/1`), `construction.boq.line.user` (group `group_construction_user/1/1/1`), `construction.boq.line.manager` (group `group_construction_manager/1/1/1`), `construction.rate.analysis.user` (group `group_construction_user/1/1/1`), `construction.rate.analysis.manager` (group `group_construction_manager/1/1/1`), `construction.rate.analysis.line.user` (group `group_construction_user/1/1/1`), `construction.rate.analysis.line.manager` (group `group_construction_manager/1/1/1`), `construction.budget.user` (group `group_construction_user/1/1/1`), `construction.budget.manager` (group `group_construction_manager/1/1/1`) …
- **Functional file groups:** Security: `security/ir.model.access.csv`, `security/construction_security.xml`; Data: `data/sequence_data.xml`, `data/configuration_data.xml`; Views: `views/construction_report_menu_actions.xml`, `views/construction_subcontract_views.xml`, `views/construction_quality_check_views.xml`, `views/construction_work_order_views.xml`, `views/construction_boq_views.xml`, `views/construction_extra_expense_views.xml`, `views/construction_phase_views.xml`, `views/construction_budget_views.xml` …
- **Tests present:** `tests/test_task.py`, `tests/test_budget_costing.py`, `tests/test_mreq.py`, `tests/test_hardening.py`, `tests/test_billing.py`, `tests/__init__.py`, `tests/test_round2_hardening.py`, `tests/test_budget_methods.py`, `tests/test_quality_check.py`, `tests/test_workflow.py`

### ODOO19 / `el_construction_tender` — Construction Tendering

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Client Tenders (Bid Costing & Submission) + Subcontractor/Vendor RFQ & Bid Comparison  
- **Category / license / author:** `Construction` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `mail`, `contacts`, `el_construction_management`  
- **Source inventory:** 18 files; 7 Python, 8 XML, 1 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ConstructionTenderRfqCompareWizard` (`_name = el_construction.tender.rfq.compare.wizard`) — `wizard/tender_compare_wizard.py`; fields: `rfq_id:Many2one`, `vendor_ids:One2many`, `comparison_html:Html`; methods: `_compute_comparison_html()`
  - `ConstructionTenderRfq` (`_name = el_construction.tender.rfq`) extends `mail.thread`, `mail.activity.mixin` — `models/tender_rfq.py`; fields: `name:Char`, `company_id:Many2one`, `project_id:Many2one`, `sub_project_id:Many2one`, `tender_opportunity_id:Many2one`, `work_type_id:Many2one`, `scope_description:Text`, `submission_deadline:Datetime`, `state:Selection`, `line_ids:One2many`, `vendor_ids:One2many`, `winner_vendor_id:Many2one`, `subcontract_id:Many2one`, `lowest_amount:Float`, `vendor_count:Integer`; methods: `create()`, `write()`, `action_send()`, `action_start_bidding()`, `action_go_comparison()`, `action_reset_draft()`, `action_cancel()`, `action_open_compare_wizard()`, `action_award_vendor()`, `action_create_subcontract()` …
  - `ConstructionTenderRfqLine` (`_name = el_construction.tender.rfq.line`) — `models/tender_rfq.py`; fields: `rfq_id:Many2one`, `boq_line_id:Many2one`, `product_id:Many2one`, `description:Char`, `quantity:Float`, `uom_id:Many2one`, `awarded_unit_price:Float`; methods: `_check_quantity()`, `_onchange_boq_line_id()`, `_onchange_product_id()`
  - `ConstructionTenderRfqVendor` (`_name = el_construction.tender.rfq.vendor`) — `models/tender_rfq.py`; fields: `rfq_id:Many2one`, `partner_id:Many2one`, `state:Selection`, `submission_date:Date`, `bid_line_ids:One2many`, `total_amount:Float`, `notes:Text`; methods: `create()`, `action_mark_submitted()`, `action_mark_declined()`, `action_award()` …
  - `ConstructionTenderRfqBidLine` (`_name = el_construction.tender.rfq.bid.line`) — `models/tender_rfq.py`; fields: `rfq_vendor_id:Many2one`, `rfq_line_id:Many2one`, `unit_price:Float`, `amount:Float`, `is_lowest:Boolean`, `remarks:Char`; methods: `_compute_amount()`, `_compute_is_lowest()`, `_check_price()`, `_check_same_rfq()`
  - `ConstructionTenderOpportunity` (`_name = el_construction.tender.opportunity`) extends `mail.thread`, `mail.activity.mixin` — `models/tender_opportunity.py`; fields: `name:Char`, `title:Char`, `client_id:Many2one`, `tender_type:Selection`, `reference_no:Char`, `company_id:Many2one`, `user_id:Many2one`, `submission_deadline:Datetime`, `site_visit_date:Datetime`, `bid_bond_required:Boolean`, `bid_bond_amount:Float`, `bid_bond_expiry:Date`, `state:Selection`, `line_ids:One2many`, `rfq_ids:One2many`, `rfq_count:Integer`, `total_cost:Float`, `total_price:Float` …; methods: `create()`, `write()`, `action_set_qualification()`, `action_start_estimating()`, `action_send_review()`, `action_submit()`, `action_reset_draft()`, `action_mark_lost()`, `action_cancel()`, `action_mark_won()`, `action_create_project()`, `dashboard_snapshot()` …
  - `ConstructionTenderLine` (`_name = el_construction.tender.line`) — `models/tender_opportunity.py`; fields: `tender_id:Many2one`, `work_type_id:Many2one`, `work_sub_type_id:Many2one`, `product_id:Many2one`, `description:Char`, `quantity:Float`, `uom_id:Many2one`, `cost_source_rfq_line_id:Many2one`, `cost_unit_manual:Float`, `cost_unit:Float`, `overhead_percent:Float`, `profit_percent:Float`, `unit_price:Float`, `cost_amount:Float`, `amount:Float`, `boq_line_id:Many2one`; methods: `_compute_cost_unit()`, `_compute_price()`, `_compute_amounts()`, `_check_quantity()`, `_onchange_work_type_id()`, `_onchange_product_id()`
- **Menu declarations:** `Tendering`, `Tenders`, `Subcontractor / Vendor RFQs`
- **View architectures detected:** form: 4, list: 2
- **Record rules:** `Tender Opportunity Company`, `Tender Line Company`, `Tender RFQ Company`, `Tender RFQ Line Company`, `Tender RFQ Vendor Company`, `Tender RFQ Bid Line Company`
- **ACL entries:** `construction.tender.opportunity.user` (group `el_construction_management.group_construction_user/1/1/1`), `construction.tender.opportunity.manager` (group `el_construction_management.group_construction_manager/1/1/1`), `construction.tender.line.user` (group `el_construction_management.group_construction_user/1/1/1`), `construction.tender.line.manager` (group `el_construction_management.group_construction_manager/1/1/1`), `construction.tender.rfq.user` (group `el_construction_management.group_construction_user/1/1/1`), `construction.tender.rfq.manager` (group `el_construction_management.group_construction_manager/1/1/1`), `construction.tender.rfq.line.user` (group `el_construction_management.group_construction_user/1/1/1`), `construction.tender.rfq.line.manager` (group `el_construction_management.group_construction_manager/1/1/1`), `construction.tender.rfq.vendor.user` (group `el_construction_management.group_construction_user/1/1/1`), `construction.tender.rfq.vendor.manager` (group `el_construction_management.group_construction_manager/1/1/1`), `construction.tender.rfq.bid.line.user` (group `el_construction_management.group_construction_user/1/1/1`), `construction.tender.rfq.bid.line.manager` (group `el_construction_management.group_construction_manager/1/1/1`), `construction.tender.rfq.compare.wizard` (group `el_construction_management.group_construction_user/1/1/1`)
- **Functional file groups:** Wizards: `wizard/tender_compare_wizard_views.xml`, `wizard/__init__.py`, `wizard/tender_compare_wizard.py`; Security: `security/ir.model.access.csv`, `security/construction_tender_security.xml`; Data: `data/sequence_data.xml`; Views: `views/tender_opportunity_views.xml`, `views/tender_rfq_views.xml`, `views/menu_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `el_ebook_store` — E-Book Store

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Sell e-books with unique access codes — online reader + download  
- **Category / license / author:** `Website/eCommerce` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `sale`, `sale_management`, `website_sale`, `payment`, `portal`, `mail`  
- **Source inventory:** 31 files; 14 Python, 9 XML, 0 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestEbookStore` — `tests/test_ebook_store.py`; methods: `setUpClass()`, `test_01_product_ebook_fields()`, `test_02_generate_random_codes()`, `test_03_generate_manual_codes()`, `test_04_code_uniqueness()`, `test_05_assign_and_expire()`, `test_06_expired_code_cannot_be_reused()`, `test_07_code_stats()`, `test_08_library_accessible_after_purchase()`, `test_09_library_permanent_access()`, `test_10_access_log_created()`, `test_11_reset_code()` …
  - `GenerateCodesWizard` (`_name = generate.codes.wizard`) — `wizard/generate_codes_wizard.py`; fields: `product_tmpl_id:Many2one`, `generation_mode:Selection`, `code_count:Integer`, `manual_codes:Text`, `max_access:Integer`; methods: `action_generate()`
  - `EbookPortal` — `controllers/portal.py`; methods: `my_library()`, `read_ebook()`, `download_ebook()`
  - `EbookLibrary` (`_name = ebook.library`) extends `mail.thread`, `mail.activity.mixin` — `models/ebook_library.py`; fields: `partner_id:Many2one`, `product_tmpl_id:Many2one`, `code_id:Many2one`, `order_id:Many2one`, `state:Selection`, `purchase_date:Datetime`, `last_access:Datetime`, `access_count:Integer`
  - `ProductTemplate` extends `product.template` — `models/product_template.py`; fields: `is_ebook:Boolean`, `ebook_file:Binary`, `ebook_filename:Char`, `ebook_sample:Binary`, `ebook_sample_filename:Char`, `ebook_access_type:Selection`, `ebook_author:Char`, `ebook_pages:Integer`, `ebook_isbn:Char`, `ebook_total_codes:Integer`, `ebook_codes_used:Integer`, `ebook_codes_available:Integer`; methods: `_compute_code_stats()`
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; methods: `action_confirm()`
  - `EbookAccessLog` (`_name = ebook.access.log`) — `models/ebook_access_log.py`; fields: `library_id:Many2one`, `partner_id:Many2one`, `product_tmpl_id:Many2one`, `access_date:Datetime`, `ip_address:Char`, `user_agent:Char`
  - `EbookCode` (`_name = ebook.code`) extends `mail.thread`, `mail.activity.mixin` — `models/ebook_code.py`; fields: `name:Char`, `product_tmpl_id:Many2one`, `partner_id:Many2one`, `order_id:Many2one`, `state:Selection`, `generated_by:Selection`, `access_count:Integer`, `max_access:Integer`, `create_date:Datetime`, `used_date:Datetime`, `expiry_date:Datetime`; methods: `generate_codes()`, `action_assign()`, `action_use()`, `action_assign_and_expire()`, `action_reset()`, `action_expire()` …
- **HTTP routes:**
  - `/my/library` → `my_library()` in `controllers/portal.py`
  - `/my/ebook/<int:library_id>/read` → `read_ebook()` in `controllers/portal.py`
  - `/my/ebook/<int:library_id>/download` → `download_ebook()` in `controllers/portal.py`
- **Menu declarations:** `E-Book Store`, `Access Codes`, `Customer Libraries`, `Access Logs`
- **View architectures detected:** form: 3, list: 3, search: 1, xpath: 1
- **ACL entries:** `ebook.code.user` (group `group_ebook_user/1/0/0`), `ebook.code.manager` (group `group_ebook_manager/1/1/1`), `ebook.library.user` (group `group_ebook_user/1/0/0`), `ebook.library.manager` (group `group_ebook_manager/1/1/1`), `ebook.access.log.user` (group `group_ebook_user/1/0/0`), `ebook.access.log.manager` (group `group_ebook_manager/1/1/1`), `generate.codes.wizard` (group `group_ebook_manager/1/1/1`)
- **Functional file groups:** Wizards: `wizard/__init__.py`, `wizard/generate_codes_wizard.py`, `wizard/generate_codes_wizard_views.xml`; Controllers: `controllers/portal.py`, `controllers/__init__.py`; Security: `security/ir.model.access.csv`, `security/security_groups.xml`; Data: `data/email_templates.xml`; Views: `views/ebook_code_views.xml`, `views/ebook_library_views.xml`, `views/product_template_views.xml`, `views/ebook_dashboard_views.xml`, `views/ebook_menus.xml`, `views/portal_ebook_views.xml`
- **Tests present:** `tests/__init__.py`, `tests/test_ebook_store.py`

### ODOO19 / `el_hospital` — Hospital Management System

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Complete hospital management: patients, appointments, EMR, wards, lab, pharmacy, billing  
- **Category / license / author:** `Services/Hospital` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `mail`, `hr`, `stock`, `account`, `sale_management`, `web`  
- **Source inventory:** 69 files; 27 Python, 23 XML, 1 JavaScript, 0 SCSS; 6 test files.  
- **Python classes / models:**
  - `TestHospitalAdmission` — `tests/test_hospital_admission.py`; methods: `setUpClass()`, `test_01_create_admission()`, `test_02_admit_sets_bed_occupied()`, `test_03_discharge_frees_bed()`, `test_04_days_count()`, `test_05_cannot_admit_without_bed()`, `test_06_cancel_frees_bed()`, `test_07_bed_maintenance()`, `test_08_ward_stats()`
  - `TestHospitalPatient` — `tests/test_hospital_patient.py`; methods: `setUpClass()`, `test_01_create_patient()`, `test_02_patient_code_sequence()`, `test_03_age_computation()`, `test_04_unique_partner()`, `test_05_allergy_creation()`, `test_06_chronic_disease_creation()`, `test_07_smart_button_appointments()`, `test_08_display_name_with_ref()`
  - `TestHospitalBilling` — `tests/test_hospital_billing.py`; methods: `setUpClass()`, `test_01_create_billing()`, `test_02_line_subtotal()`, `test_03_billing_total()`, `test_04_cannot_invoice_empty()`, `test_05_create_invoice()`, `test_06_cannot_invoice_twice()`
  - `TestHospitalAppointment` — `tests/test_hospital_appointment.py`; methods: `setUpClass()`, `test_01_create_appointment()`, `test_02_state_draft_to_confirmed()`, `test_03_state_confirmed_to_done()`, `test_04_done_creates_medical_record()`, `test_05_cancel_appointment()`, `test_06_cannot_cancel_done()`, `test_07_reset_to_draft()`
  - `TestHospitalLab` — `tests/test_hospital_lab.py`; methods: `setUpClass()`, `test_01_create_lab_test()`, `test_02_lab_state_requested_to_in_progress()`, `test_03_lab_complete_requires_result()`, `test_04_lab_complete_with_result()`, `test_05_lab_cancel()`, `test_06_create_radiology()`, `test_07_radiology_complete()`, `test_08_cannot_cancel_completed()`
  - `HospitalController` — `controllers/controllers.py`; methods: `get_dashboard_data()`
  - `HospitalPrescriptionLine` (`_name = hospital.prescription.line`) — `models/hospital_prescription.py`; fields: `prescription_id:Many2one`, `medicament_id:Many2one`, `dosage:Char`, `frequency:Char`, `duration:Char`, `quantity:Float`, `instructions:Text`, `company_id:Many2one`
  - `HospitalPrescription` (`_name = hospital.prescription`) extends `mail.thread`, `mail.activity.mixin` — `models/hospital_prescription.py`; fields: `name:Char`, `patient_id:Many2one`, `physician_id:Many2one`, `medical_record_id:Many2one`, `prescription_date:Datetime`, `line_ids:One2many`, `state:Selection`, `notes:Text`, `company_id:Many2one`; methods: `create()`, `action_done()`, `action_draft()`, `action_print()`
  - `HospitalDashboard` (`_name = hospital.dashboard`) — `models/hospital_dashboard.py`; fields: `total_patients:Integer`, `total_physicians:Integer`, `total_appointments_today:Integer`, `total_active_admissions:Integer`, `total_beds:Integer`, `occupied_beds:Integer`, `available_beds:Integer`, `bed_occupancy_rate:Float`, `pending_lab_tests:Integer`, `pending_radiology:Integer`, `monthly_revenue:Monetary`, `currency_id:Many2one`; methods: `get_dashboard_data()` …
  - `HospitalAdmission` (`_name = hospital.admission`) extends `mail.thread`, `mail.activity.mixin` — `models/hospital_admission.py`; fields: `name:Char`, `patient_id:Many2one`, `physician_id:Many2one`, `department_id:Many2one`, `ward_id:Many2one`, `bed_id:Many2one`, `admission_date:Datetime`, `discharge_date:Datetime`, `state:Selection`, `reason:Text`, `discharge_notes:Text`, `days_count:Integer`, `company_id:Many2one`; methods: `create()`, `action_admit()`, `action_discharge()`, `action_cancel()`, `action_draft()` …
  - `HospitalMedicament` (`_name = hospital.medicament`) extends `mail.thread`, `mail.activity.mixin` — `models/hospital_medicament.py`; fields: `name:Char`, `product_id:Many2one`, `product_tmpl_id:Many2one`, `generic_name:Char`, `form:Selection`, `strength:Char`, `is_prescription_required:Boolean`, `stock_qty:Float`, `active:Boolean`, `company_id:Many2one`; methods: `_compute_name()`, `_compute_display_name()`, `_compute_stock_qty()`
  - `HospitalPhysician` (`_name = hospital.physician`) extends `mail.thread`, `mail.activity.mixin` — `models/hospital_physician.py`; fields: `name:Char`, `partner_id:Many2one`, `employee_id:Many2one`, `user_id:Many2one`, `specialization:Char`, `department_id:Many2one`, `medical_license:Char`, `phone:Char`, `email:Char`, `image_1920:Image`, `active:Boolean`, `company_id:Many2one`; methods: `action_open_patients()` …
  - `HospitalLabTest` (`_name = hospital.lab.test`) extends `mail.thread`, `mail.activity.mixin` — `models/hospital_lab_test.py`; fields: `name:Char`, `patient_id:Many2one`, `physician_id:Many2one`, `medical_record_id:Many2one`, `test_type:Selection`, `test_name:Char`, `request_date:Datetime`, `result_date:Datetime`, `state:Selection`, `result:Text`, `notes:Text`, `company_id:Many2one`; methods: `create()`, `action_start()`, `action_complete()`, `action_cancel()`
  - `HospitalPatientAllergy` (`_name = hospital.patient.allergy`) — `models/hospital_patient.py`; fields: `patient_id:Many2one`, `name:Char`, `severity:Selection`, `notes:Text`
  - `HospitalPatientDisease` (`_name = hospital.patient.disease`) — `models/hospital_patient.py`; fields: `patient_id:Many2one`, `name:Char`, `diagnosed_date:Date`, `notes:Text`
  - `HospitalPatient` (`_name = hospital.patient`) extends `mail.thread`, `mail.activity.mixin` — `models/hospital_patient.py`; fields: `name:Char`, `ref:Char`, `partner_id:Many2one`, `birth_date:Date`, `age:Integer`, `gender:Selection`, `blood_type:Selection`, `phone:Char`, `email:Char`, `address:Char`, `image_1920:Image`, `physician_id:Many2one`, `department_id:Many2one`, `allergy_ids:One2many`, `chronic_disease_ids:One2many`, `appointment_count:Integer`, `admission_count:Integer`, `active:Boolean` …; methods: `create()`, `action_open_appointments()`, `action_open_admissions()` …
  - `HospitalDepartment` (`_name = hospital.department`) extends `mail.thread`, `mail.activity.mixin` — `models/hospital_department.py`; fields: `name:Char`, `code:Char`, `display_name:Char`, `head_physician_id:Many2one`, `bed_capacity:Integer`, `notes:Text`, `company_id:Many2one`, `active:Boolean`; methods: `_compute_display_name()`
  - `HospitalWard` (`_name = hospital.ward`) — `models/hospital_ward.py`; fields: `name:Char`, `code:Char`, `display_name:Char`, `department_id:Many2one`, `ward_type:Selection`, `floor:Char`, `bed_capacity:Integer`, `bed_count:Integer`, `occupied_count:Integer`, `available_count:Integer`, `notes:Text`, `company_id:Many2one`, `active:Boolean`; methods: `action_open_beds()` …
  - `HospitalMedicalRecord` (`_name = hospital.medical.record`) extends `mail.thread`, `mail.activity.mixin` — `models/hospital_medical_record.py`; fields: `name:Char`, `patient_id:Many2one`, `physician_id:Many2one`, `appointment_id:Many2one`, `record_date:Datetime`, `chief_complaint:Text`, `diagnosis:Text`, `treatment:Text`, `notes:Text`, `prescription_ids:One2many`, `lab_test_ids:One2many`, `radiology_order_ids:One2many`, `prescription_count:Integer`, `lab_test_count:Integer`, `radiology_count:Integer`, `company_id:Many2one`; methods: `create()`, `action_create_prescription()`, `action_open_lab_tests()`, `action_open_radiology()` …
  - `HospitalInvoiceBillingLine` (`_name = hospital.invoice.billing.line`) — `models/hospital_billing.py`; fields: `billing_id:Many2one`, `name:Char`, `service_type:Selection`, `quantity:Float`, `price_unit:Monetary`, `price_subtotal:Monetary`, `currency_id:Many2one`; methods: `_compute_subtotal()`
  - `HospitalInvoiceBilling` (`_name = hospital.invoice.billing`) extends `mail.thread`, `mail.activity.mixin` — `models/hospital_billing.py`; fields: `name:Char`, `patient_id:Many2one`, `partner_id:Many2one`, `physician_id:Many2one`, `move_id:Many2one`, `billing_date:Date`, `line_ids:One2many`, `amount_total:Monetary`, `state:Selection`, `currency_id:Many2one`, `company_id:Many2one`, `notes:Text`; methods: `create()`, `action_create_invoice()`, `action_view_invoice()`, `action_print()` …
  - `HospitalBed` (`_name = hospital.bed`) extends `mail.thread`, `mail.activity.mixin` — `models/hospital_bed.py`; fields: `name:Char`, `ward_id:Many2one`, `bed_number:Char`, `state:Selection`, `admission_id:Many2one`, `patient_id:Many2one`, `notes:Text`, `company_id:Many2one`; methods: `action_set_maintenance()`, `action_set_available()` …
  - `HospitalRadiologyOrder` (`_name = hospital.radiology.order`) extends `mail.thread`, `mail.activity.mixin` — `models/hospital_radiology.py`; fields: `name:Char`, `patient_id:Many2one`, `physician_id:Many2one`, `medical_record_id:Many2one`, `modality:Selection`, `study_name:Char`, `request_date:Datetime`, `result_date:Datetime`, `state:Selection`, `result:Text`, `image_ids:Many2many`, `notes:Text`, `company_id:Many2one`; methods: `create()`, `action_start()`, `action_complete()`, `action_cancel()`
  - `HospitalAppointment` (`_name = hospital.appointment`) extends `mail.thread`, `mail.activity.mixin` — `models/hospital_appointment.py`; fields: `name:Char`, `patient_id:Many2one`, `physician_id:Many2one`, `department_id:Many2one`, `appointment_date:Datetime`, `duration:Float`, `state:Selection`, `type:Selection`, `notes:Text`, `medical_record_id:Many2one`, `is_today:Boolean`, `company_id:Many2one`; methods: `create()`, `action_confirm()`, `action_done()`, `action_cancel()`, `action_draft()`, `action_create_medical_record()` …
- **HTTP routes:**
  - `/hospital/dashboard/data` → `get_dashboard_data()` in `controllers/controllers.py`
- **Menu declarations:** `Hospital`, `Dashboard`, `Patients`, `Patients`, `Appointments`, `Today's Appointments`, `Medical Records`, `Physicians`, `Inpatient`, `Admissions`, `Active Admissions`, `Wards`, `Beds`, `Laboratory`, `Lab Tests`, `Radiology`, `Pharmacy`, `Medicaments`, `Prescriptions`, `Billing` …
- **View architectures detected:** calendar: 1, form: 13, kanban: 1, list: 13, search: 7
- **Record rules:** `Hospital: Multi-Company`
- **ACL entries:** `hospital.department.user` (group `group_hospital_user/1/0/0`), `hospital.department.admin` (group `group_hospital_admin/1/1/1`), `hospital.physician.user` (group `group_hospital_user/1/0/0`), `hospital.physician.doctor` (group `group_hospital_doctor/1/1/1`), `hospital.physician.admin` (group `group_hospital_admin/1/1/1`), `hospital.patient.user` (group `group_hospital_user/1/0/0`), `hospital.patient.reception` (group `group_hospital_reception/1/1/1`), `hospital.patient.doctor` (group `group_hospital_doctor/1/1/1`), `hospital.patient.admin` (group `group_hospital_admin/1/1/1`), `hospital.patient.allergy.user` (group `group_hospital_user/1/0/0`), `hospital.patient.allergy.doctor` (group `group_hospital_doctor/1/1/1`), `hospital.patient.allergy.admin` (group `group_hospital_admin/1/1/1`), `hospital.patient.disease.user` (group `group_hospital_user/1/0/0`), `hospital.patient.disease.doctor` (group `group_hospital_doctor/1/1/1`), `hospital.patient.disease.admin` (group `group_hospital_admin/1/1/1`), `hospital.appointment.user` (group `group_hospital_user/1/0/0`), `hospital.appointment.reception` (group `group_hospital_reception/1/1/1`), `hospital.appointment.doctor` (group `group_hospital_doctor/1/1/1`), `hospital.appointment.admin` (group `group_hospital_admin/1/1/1`), `hospital.medical.record.user` (group `group_hospital_user/1/0/0`) …
- **Functional file groups:** Controllers: `controllers/controllers.py`, `controllers/__init__.py`; Security: `security/ir.model.access.csv`, `security/el_hospital_groups.xml`; Data: `data/hospital_sequences.xml`, `data/hospital_mail_templates.xml`, `data/hospital_data.xml`; Views: `views/hospital_medical_record_views.xml`, `views/hospital_appointment_views.xml`, `views/hospital_lab_test_views.xml`, `views/hospital_prescription_views.xml`, `views/hospital_menus.xml`, `views/hospital_ward_views.xml`, `views/hospital_admission_views.xml`, `views/hospital_patient_views.xml` …
- **Tests present:** `tests/test_hospital_admission.py`, `tests/test_hospital_patient.py`, `tests/__init__.py`, `tests/test_hospital_billing.py`, `tests/test_hospital_appointment.py`, `tests/test_hospital_lab.py`
- **Implemented development-batch changes:** Batch 01: sanitized dashboard API error responses.

### ODOO19 / `el_hr_attendance_sheet` — HR Attendance Sheet And Policies

- **Manifest version:** `19.0.1.1.0`  
- **Summary:** Calculate overtime, lateness, absence from attendance and feed payslip  
- **Category / license / author:** `Human Resources/Attendance` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `hr_attendance`, `hr`, `hr_payroll`, `hr_holidays`, `mail`, `calendar`  
- **Source inventory:** 63 files; 21 Python, 19 XML, 0 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestHrAttendanceSheet` — `tests/test_hr_attendance_sheet.py`; methods: `setUpClass()`, `test_01_overtime_rule_creation()`, `test_02_lateness_step_lookup()`, `test_03_absence_step_lookup()`, `test_04_policy_get_overtime_rule()`, `test_05_sheet_sequence()`, `test_06_state_machine_transitions()`, `test_07_public_holiday_state_machine()`, `test_08_overtime_calculation()`, `test_09_lateness_tier_lookup_by_occurrence()`, `test_10_absence_tier_escalation()`, `test_11_absence_fixed_days_penalty()` …
  - `HrAttendanceSheetReport` (`_name = report.el_hr_attendance_sheet.report_hr_attendance_sheet`) — `report/hr_attendance_sheet_report.py`; methods: `_get_report_values()`
  - `HrAttendanceChangeDataWizard` (`_name = hr.attendance.change.data.wizard`) — `wizard/hr_attendance_change_data_wizard.py`; fields: `sheet_line_id:Many2one`, `new_overtime_hours:Float`, `new_late_in_minutes:Float`, `new_difference_hours:Float`, `reason:Text`; methods: `action_apply()`
  - `HrAttendanceSheetBatchWizard` (`_name = hr.attendance.sheet.batch.wizard`) — `wizard/hr_attendance_sheet_batch_wizard.py`; fields: `department_id:Many2one`, `date_from:Date`, `date_to:Date`, `employee_ids:Many2many`, `company_id:Many2one`; methods: `action_create_batch()` …
  - `HrAttendanceCreatePayslipWizard` (`_name = hr.attendance.create.payslip.wizard`) — `wizard/hr_attendance_create_payslip_wizard.py`; fields: `sheet_id:Many2one`, `employee_id:Many2one`, `date_from:Date`, `date_to:Date`, `struct_id:Many2one`, `contract_id:Many2one`; methods: `action_create_payslip()`
  - `HrAttendancePublicHoliday` (`_name = hr.attendance.public.holiday`) extends `mail.thread`, `mail.activity.mixin` — `models/hr_attendance_public_holiday.py`; fields: `name:Char`, `date_from:Date`, `date_to:Date`, `active:Boolean`, `state:Selection`, `line_ids:One2many`, `company_id:Many2one`; methods: `write()`, `action_activate()`, `action_cancel()`, `action_draft()`, `is_employee_on_holiday()` …
  - `HrAttendancePublicHolidayLine` (`_name = hr.attendance.public.holiday.line`) — `models/hr_attendance_public_holiday.py`; fields: `holiday_id:Many2one`, `employee_id:Many2one`, `department_id:Many2one`, `employee_tag_ids:Many2many`, `company_id:Many2one`; methods: `matches_employee()`
  - `HrPayrollStructure` extends `hr.payroll.structure` — `models/hr_payroll_structure.py`; methods: `create()`, `action_clean_inherited_rules()`, `action_propagate_attendance_rules()` …
  - `HrAttendancePolicy` (`_name = hr.attendance.policy`) extends `mail.thread` — `models/hr_attendance_policy.py`; fields: `name:Char`, `active:Boolean`, `company_id:Many2one`, `overtime_working_id:Many2one`, `overtime_weekend_id:Many2one`, `overtime_holiday_id:Many2one`, `lateness_id:Many2one`, `absence_id:Many2one`, `contract_ids:One2many`; methods: `get_overtime_rule()`
  - `HrAttendanceSheet` (`_name = hr.attendance.sheet`) extends `mail.thread`, `mail.activity.mixin` — `models/hr_attendance_sheet.py`; fields: `name:Char`, `employee_id:Many2one`, `date_from:Date`, `date_to:Date`, `contract_id:Many2one`, `policy_id:Many2one`, `state:Selection`, `company_id:Many2one`, `currency_id:Many2one`, `line_ids:One2many`, `total_overtime:Float`, `total_overtime_working:Float`, `total_overtime_weekend:Float`, `total_overtime_holiday:Float`, `total_late_in:Float`, `total_absence:Float`, `total_late_penalty_hours:Float`, `total_absence_penalty_days:Float` …; methods: `create()`, `write()`, `action_compute()`, `action_approve()`, `action_done()`, `action_cancel()`, `action_draft()`, `action_create_payslip()`, `action_print_report()`, `action_open_payslip()` …
  - `HrAttendanceSheetLine` (`_name = hr.attendance.sheet.line`) — `models/hr_attendance_sheet.py`; fields: `sheet_id:Many2one`, `date:Date`, `day_type:Selection`, `planned_hours:Float`, `worked_hours:Float`, `overtime_hours:Float`, `late_in_minutes:Float`, `is_absent:Boolean`, `is_leave:Boolean`, `leave_id:Many2one`, `difference_hours:Float`, `absence_occurrence:Integer`, `late_occurrence:Integer`, `late_penalty:Float`, `absence_penalty_days:Float`, `note:Text`, `attendance_ids:Many2many`, `changed_manually:Boolean`; methods: `create()`, `write()`, `unlink()`, `action_open_change_wizard()` …
  - `HrPayslip` extends `hr.payslip` — `models/hr_payslip.py`; fields: `attendance_sheet_id:Many2one`, `no_attendance_sheet:Boolean`, `overtime_hours:Float`, `overtime_working_hours:Float`, `overtime_weekend_hours:Float`, `overtime_holiday_hours:Float`, `late_in_hours:Float`, `absence_days:Float`, `difference_hours:Float`, `late_penalty_hours:Float`, `absence_penalty_days:Float`, `number_late_occurrences:Integer`, `number_absence_occurrences:Integer`; methods: `action_link_attendance_sheet()`, `action_open_attendance_sheet()`, `create()` …
  - `HrContract` extends `hr.version` — `models/hr_contract.py`; fields: `attendance_policy_id:Many2one`
  - `HrEmployee` extends `hr.employee` — `models/hr_contract.py`; fields: `attendance_policy_id:Many2one`
  - `HrAttendanceSheetBatch` (`_name = hr.attendance.sheet.batch`) extends `mail.thread` — `models/hr_attendance_sheet_batch.py`; fields: `name:Char`, `department_id:Many2one`, `date_from:Date`, `date_to:Date`, `state:Selection`, `company_id:Many2one`, `line_ids:One2many`; methods: `create()`, `write()`, `action_generate_sheets()`, `action_confirm()`, `action_done()`, `action_cancel()`, `action_draft()` …
  - `HrAttendanceSheetBatchLine` (`_name = hr.attendance.sheet.batch.line`) — `models/hr_attendance_sheet_batch.py`; fields: `batch_id:Many2one`, `employee_id:Many2one`, `sheet_id:Many2one`, `error_message:Text`, `company_id:Many2one`
  - `HrAttendanceRuleOvertime` (`_name = hr.attendance.rule.overtime`) — `models/hr_attendance_rule.py`; fields: `name:Char`, `type:Selection`, `apply_after_minutes:Float`, `rate:Float`, `active:Boolean`, `company_id:Many2one`
  - `HrAttendanceRuleLateness` (`_name = hr.attendance.rule.lateness`) — `models/hr_attendance_rule.py`; fields: `name:Char`, `active:Boolean`, `unit:Selection`, `tier_ids:One2many`, `company_id:Many2one`; methods: `get_tier()`, `get_step()`, `get_step_for_minutes()`, `get_step_for_hours()`
  - `HrAttendanceRuleLatenessTier` (`_name = hr.attendance.rule.lateness.tier`) — `models/hr_attendance_rule.py`; fields: `name:Char`, `lateness_id:Many2one`, `sequence:Integer`, `occurrence_from:Integer`, `occurrence_to:Integer`, `step_ids:One2many`, `step_count:Integer`, `unit:Selection`, `company_id:Many2one`; methods: `get_step_for_minutes()`, `get_step_for_hours()`, `action_open_rule()`, `action_open_tier()` …
  - `HrAttendanceRuleLatenessStep` (`_name = hr.attendance.rule.lateness.step`) — `models/hr_attendance_rule.py`; fields: `tier_id:Many2one`, `from_minutes:Float`, `to_minutes:Float`, `from_hours:Float`, `to_hours:Float`, `penalty_type:Selection`, `rate:Float`, `penalty_hours:Float`, `initial_rate:Float`, `amount:Float`, `lateness_id:Many2one`, `company_id:Many2one`; methods: `_compute_hour_range()`, `_inverse_hour_range()`, `_check_ranges()`
  - `HrAttendanceRuleAbsence` (`_name = hr.attendance.rule.absence`) — `models/hr_attendance_rule.py`; fields: `name:Char`, `active:Boolean`, `tier_ids:One2many`, `company_id:Many2one`; methods: `get_tier()`, `get_step_for_days()`
  - `HrAttendanceRuleAbsenceTier` (`_name = hr.attendance.rule.absence.tier`) — `models/hr_attendance_rule.py`; fields: `name:Char`, `absence_id:Many2one`, `sequence:Integer`, `occurrence_from:Integer`, `occurrence_to:Integer`, `step_ids:One2many`, `step_count:Integer`, `company_id:Many2one`; methods: `get_step_for_days()`, `action_open_rule()`, `action_open_tier()` …
  - `HrAttendanceRuleAbsenceStep` (`_name = hr.attendance.rule.absence.step`) — `models/hr_attendance_rule.py`; fields: `tier_id:Many2one`, `from_days:Integer`, `to_days:Integer`, `penalty_type:Selection`, `rate:Float`, `deduction_days:Float`, `absence_id:Many2one`, `company_id:Many2one`; methods: `compute_deduction_days()` …
- **Menu declarations:** `Attendance Sheets`, `Attendance Sheets`, `Batches`, `Configuration`, `Public Holidays`, `Rules`, `Overtime Rules`, `Lateness Rules`, `Absence Rules`, `Attendance Policies`
- **View architectures detected:** form: 12, graph: 1, kanban: 1, list: 9, pivot: 1, search: 7, xpath: 3
- **Record rules:** `Attendance Sheet: multi-company`, `Attendance Policy: multi-company`, `Public Holiday: multi-company`, `Attendance Sheet Batch: multi-company`, `Overtime Rule: multi-company`, `Attendance Sheet: see own`, `Attendance Sheet Line: multi-company`, `Attendance Sheet Batch Line: multi-company`, `Attendance Sheet Line: see own`, `Attendance Sheet: officer access within company`, `Attendance Sheet Line: officer access within company`, `Attendance Sheet Batch Line: officer access within company`, `Public Holiday Line: multi-company`, `Lateness Rule: multi-company`, `Lateness Tier: multi-company`, `Lateness Step: multi-company`, `Absence Rule: multi-company`, `Absence Tier: multi-company`, `Absence Step: multi-company`
- **ACL entries:** `hr.attendance.public.holiday.user` (group `group_hr_attendance_sheet_user/1/0/0`), `hr.attendance.public.holiday.officer` (group `group_hr_attendance_sheet_officer/1/1/1`), `hr.attendance.public.holiday.manager` (group `group_hr_attendance_sheet_manager/1/1/1`), `hr.attendance.public.holiday.line.user` (group `group_hr_attendance_sheet_user/1/0/0`), `hr.attendance.public.holiday.line.officer` (group `group_hr_attendance_sheet_officer/1/1/1`), `hr.attendance.public.holiday.line.manager` (group `group_hr_attendance_sheet_manager/1/1/1`), `hr.attendance.rule.overtime.user` (group `group_hr_attendance_sheet_user/1/0/0`), `hr.attendance.rule.overtime.manager` (group `group_hr_attendance_sheet_manager/1/1/1`), `hr.attendance.rule.lateness.user` (group `group_hr_attendance_sheet_user/1/0/0`), `hr.attendance.rule.lateness.manager` (group `group_hr_attendance_sheet_manager/1/1/1`), `hr.attendance.rule.lateness.step.user` (group `group_hr_attendance_sheet_user/1/0/0`), `hr.attendance.rule.lateness.step.manager` (group `group_hr_attendance_sheet_manager/1/1/1`), `hr.attendance.rule.lateness.tier.user` (group `group_hr_attendance_sheet_user/1/0/0`), `hr.attendance.rule.lateness.tier.manager` (group `group_hr_attendance_sheet_manager/1/1/1`), `hr.attendance.rule.absence.user` (group `group_hr_attendance_sheet_user/1/0/0`), `hr.attendance.rule.absence.manager` (group `group_hr_attendance_sheet_manager/1/1/1`), `hr.attendance.rule.absence.step.user` (group `group_hr_attendance_sheet_user/1/0/0`), `hr.attendance.rule.absence.step.manager` (group `group_hr_attendance_sheet_manager/1/1/1`), `hr.attendance.rule.absence.tier.user` (group `group_hr_attendance_sheet_user/1/0/0`), `hr.attendance.rule.absence.tier.manager` (group `group_hr_attendance_sheet_manager/1/1/1`) …
- **Functional file groups:** Wizards: `wizard/hr_attendance_sheet_batch_wizard_views.xml`, `wizard/__init__.py`, `wizard/hr_attendance_change_data_wizard_views.xml`, `wizard/hr_attendance_change_data_wizard.py`, `wizard/hr_attendance_sheet_batch_wizard.py`, `wizard/hr_attendance_create_payslip_wizard_views.xml`, `wizard/hr_attendance_create_payslip_wizard.py`; Reports: `report/hr_attendance_sheet_report.xml`, `report/hr_attendance_sheet_report.py`, `report/hr_attendance_sheet_report_templates.xml`, `report/__init__.py`; Security: `security/ir.model.access.csv`, `security/hr_attendance_sheet_groups.xml`, `security/hr_attendance_sheet_rules.xml`; Data: `data/hr_payroll_structure_data.xml`, `data/ir_sequence_data.xml`, `data/hr_structure_attendance_rules_action.xml`, `data/hr_salary_rule_data.xml`; Views: `views/hr_attendance_policy_views.xml`, `views/hr_attendance_sheet_batch_views.xml`, `views/hr_attendance_public_holiday_views.xml`, `views/hr_attendance_rule_views.xml`, `views/hr_payslip_views.xml`, `views/hr_contract_views.xml`, `views/hr_attendance_sheet_views.xml`, `views/hr_attendance_sheet_menus.xml`
- **Tests present:** `tests/__init__.py`, `tests/test_hr_attendance_sheet.py`

### ODOO19 / `el_inter_company_transfer` — Inter Company Transfer

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Automate inter-company stock, sale, purchase, and accounting documents  
- **Category / license / author:** `Warehouse / Inventory` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `mail`, `stock`, `sale_management`, `sale_stock`, `purchase`, `purchase_stock`, `account`  
- **Source inventory:** 23 files; 11 Python, 11 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `InterCompanyConfig` (`_name = inter.company.config`) — `models/inter_company_config.py`; fields: `source_company_id:Many2one`, `dest_company_id:Many2one`, `display_name:Char`, `apply_on:Selection`, `link_document:Boolean`, `auto_validate_picking:Boolean`, `auto_create_invoice:Boolean`, `auto_validate_invoice:Boolean`, `active:Boolean`; methods: `_compute_display_name()`, `_check_company_warehouses()`, `_find_for_sale()`, `_find_for_purchase()`, `_company_from_partner()`
  - `PurchaseOrder` extends `purchase.order` — `models/purchase_order.py`; fields: `inter_company_transfer_id:Many2one`, `inter_company_sale_order_id:Many2one`; methods: `button_confirm()`, `action_view_inter_company_transfer()`, `action_view_inter_company_sale_order()` …
  - `AccountMove` extends `account.move` — `models/account_move.py`; fields: `inter_company_transfer_id:Many2one`; methods: `action_view_inter_company_transfer()`
  - `ResCompany` extends `res.company` — `models/res_company.py`; fields: `inter_company_warehouse_id:Many2one`
  - `StockPicking` extends `stock.picking` — `models/stock_picking.py`; fields: `inter_company_transfer_id:Many2one`; methods: `action_view_inter_company_transfer()`
  - `ReturnInterCompanyTransfer` (`_name = return.inter.company.transfer`) extends `mail.thread`, `mail.activity.mixin` — `models/return_inter_company_transfer.py`; fields: `name:Char`, `source_ict_id:Many2one`, `source_company_id:Many2one`, `dest_company_id:Many2one`, `from_warehouse_id:Many2one`, `to_warehouse_id:Many2one`, `state:Selection`, `sale_order_id:Many2one`, `purchase_order_id:Many2one`, `delivery_picking_id:Many2one`, `receipt_picking_id:Many2one`, `customer_invoice_id:Many2one`, `vendor_bill_id:Many2one`, `partner_id:Many2one`, `date:Date`, `return_line_ids:One2many`, `company_id:Many2one`; methods: `create()`, `action_process()`, `action_cancel()`, `action_view_sale_order()`, `action_view_purchase_order()`, `action_view_customer_invoice()`, `action_view_vendor_bill()` …
  - `ReturnInterCompanyTransferLine` (`_name = return.inter.company.transfer.line`) — `models/return_inter_company_transfer.py`; fields: `transfer_id:Many2one`, `product_id:Many2one`, `quantity:Float`, `uom_id:Many2one`, `price_unit:Float`, `company_id:Many2one`; methods: `_onchange_product_id()`
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; fields: `inter_company_transfer_id:Many2one`, `inter_company_purchase_order_id:Many2one`; methods: `action_confirm()`, `action_view_inter_company_transfer()`, `action_view_inter_company_purchase_order()` …
  - `StockInterCompanyTransfer` (`_name = stock.inter.company.transfer`) extends `mail.thread`, `mail.activity.mixin` — `models/stock_inter_company_transfer.py`; fields: `name:Char`, `source_company_id:Many2one`, `dest_company_id:Many2one`, `from_warehouse_id:Many2one`, `to_warehouse_id:Many2one`, `state:Selection`, `sale_order_id:Many2one`, `purchase_order_id:Many2one`, `delivery_picking_id:Many2one`, `receipt_picking_id:Many2one`, `customer_invoice_id:Many2one`, `vendor_bill_id:Many2one`, `partner_id:Many2one`, `date:Date`, `config_id:Many2one`, `transfer_line_ids:One2many`, `company_id:Many2one`; methods: `create()`, `action_process()`, `action_cancel()`, `action_reverse()`, `create_from_sale_order()`, `create_from_purchase_order()`, `action_view_sale_order()`, `action_view_purchase_order()`, `action_view_delivery_picking()`, `action_view_receipt_picking()`, `action_view_customer_invoice()`, `action_view_vendor_bill()` …
  - `StockInterCompanyTransferLine` (`_name = stock.inter.company.transfer.line`) — `models/stock_inter_company_transfer.py`; fields: `transfer_id:Many2one`, `product_id:Many2one`, `quantity:Float`, `uom_id:Many2one`, `price_unit:Float`, `company_id:Many2one`; methods: `_onchange_product_id()`
- **Menu declarations:** `InterCompany Transaction`, `InterCompany Transaction`, `Return InterCompany Transaction`, `Inventory Breakdown`, `InterCompany Rules`
- **View architectures detected:** form: 3, list: 3, xpath: 5
- **Record rules:** `Inter-company transfers: allowed companies`, `Inter-company transfer lines: allowed companies`, `Return inter-company transfers: allowed companies`, `Return inter-company transfer lines: allowed companies`, `Inter-company configs: allowed companies`
- **ACL entries:** `stock.inter.company.transfer` (group `/1/1/1`), `stock.inter.company.transfer.line` (group `/1/1/1`), `return.inter.company.transfer` (group `/1/1/1`), `return.inter.company.transfer.line` (group `/1/1/1`), `inter.company.config` (group `/1/1/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`, `security/security_groups.xml`; Data: `data/inter_company_sequence.xml`; Views: `views/return_inter_company_transfer_views.xml`, `views/sale_order_views.xml`, `views/stock_inter_company_transfer_views.xml`, `views/inter_company_menus.xml`, `views/stock_picking_views.xml`, `views/purchase_order_views.xml`, `views/res_company_views.xml`, `views/inter_company_config_views.xml` …
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `el_nmo_classification` — El-Nmo - Customer Classification

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Customer classification tiers (A-E) with auto-classification criteria.  
- **Category / license / author:** `Sales/Sales` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `mail`, `sale`, `account`, `el_nmo_sale_payment_gateway`  
- **Source inventory:** 15 files; 8 Python, 6 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `CustomerClassification` (`_name = customer.classification`) extends `mail.thread`, `mail.activity.mixin` — `models/customer_classification.py`; fields: `name:Char`, `description:Text`, `sequence:Integer`, `active:Boolean`, `pricelist_id:Many2one`, `credit_limit:Float`, `payment_term_id:Many2one`, `credit_policy:Selection`, `company_id:Many2one`, `partner_ids:One2many`, `partner_count:Integer`, `criteria_ids:One2many`, `has_active_criteria:Boolean`; methods: `action_apply_pricelist()` …
  - `AccountMove` extends `account.move` — `models/account_move.py`; fields: `partner_classification_id:Many2one`, `partner_effective_credit_limit:Float`, `partner_credit_policy:Selection`; methods: `action_post()` …
  - `ClassificationCriteria` (`_name = classification.criteria`) — `models/classification_criteria.py`; fields: `classification_id:Many2one`, `sequence:Integer`, `model_field:Selection`, `operator:Selection`, `value:Float`, `value_to:Float`, `active:Boolean`; methods: `_compute_display_name()`, `_check_between_values()`, `_evaluate()`
  - `ResPartner` extends `res.partner` — `models/res_partner.py`; fields: `classification_id:Many2one`, `override_pricelist:Boolean`, `override_credit_limit:Boolean`, `override_payment_term:Boolean`, `manual_pricelist_id:Many2one`, `classification_pricelist_id:Many2one`, `classification_credit_limit:Float`, `classification_payment_term_id:Many2one`, `credit_policy:Selection`, `effective_credit_limit:Float`, `effective_payment_term_id:Many2one`, `payment_type:Selection`, `payment_gateway_id:Many2one`, `remaining_credit:Float`; methods: `_compute_product_pricelist()`, `_compute_effective_credit_limit()`, `_compute_remaining_credit()`, `_compute_effective_payment_term_id()`, `_onchange_classification_id()`, `_onchange_override_pricelist()`, `_onchange_override_credit_limit()`, `_onchange_override_payment_term()`
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; fields: `partner_payment_type:Selection`, `partner_classification_id:Many2one`, `partner_effective_credit_limit:Float`, `partner_credit_policy:Selection`, `partner_outstanding:Monetary`, `partner_remaining_credit:Float`, `payment_gateway_id:Many2one`; methods: `action_confirm()` …
- **Menu declarations:** `Customer Classification`, `Classifications`
- **View architectures detected:** form: 1, list: 1, search: 1, xpath: 4
- **ACL entries:** `customer.classification.manager` (group `sales_team.group_sale_manager/1/1/1`), `customer.classification.user` (group `sales_team.group_sale_salesman/1/0/0`), `classification.criteria.manager` (group `sales_team.group_sale_manager/1/1/1`), `classification.criteria.user` (group `sales_team.group_sale_salesman/1/0/0`)
- **Functional file groups:** Security: `security/ir.model.access.csv`, `security/security.xml`; Data: `data/classification_cron.xml`, `data/default_data.xml`; Views: `views/res_partner_views.xml`, `views/sale_order_views.xml`, `views/customer_classification_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `el_nmo_credit_approval` — El-Nmo - Credit Limit Approval Workflow

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Approval workflow for sale orders exceeding customer credit limits.  
- **Category / license / author:** `Sales/Sales` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `mail`, `sale`, `el_nmo_classification`  
- **Source inventory:** 28 files; 10 Python, 7 XML, 0 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestCreditApproval` — `tests/test_credit_approval.py`; methods: `setUpClass()`, `test_01_rejection_reason_creation()`, `test_02_approval_request_creation()`, `test_03_approval_request_approve()`, `test_04_approval_request_reject_without_reason()`, `test_05_approval_request_reject_with_reason()`, `test_06_approval_request_resubmit()`, `test_07_credit_policy_warning_allows_confirm()`, `test_08_cash_customer_not_blocked()`
  - `CreditApprovalWizard` (`_name = credit.approval.wizard`) — `wizard/credit_approval_wizard.py`; fields: `sale_order_id:Many2one`, `request_id:Many2one`, `request_state:Selection`, `customer_id:Many2one`, `credit_limit:Float`, `credit_used:Float`, `order_amount:Monetary`, `exceeded_by:Float`, `currency_id:Many2one`, `rejection_reason_id:Many2one`, `rejection_notes:Text`; methods: `default_get()`, `action_approve()`, `action_reject()`
  - `CreditRejectionReason` (`_name = credit.rejection.reason`) — `models/credit_rejection_reason.py`; fields: `name:Char`, `description:Text`, `sequence:Integer`, `active:Boolean`, `company_id:Many2one`
  - `CreditApprovalRequest` (`_name = credit.approval.request`) extends `mail.thread`, `mail.activity.mixin` — `models/credit_approval_request.py`; fields: `name:Char`, `sale_order_id:Many2one`, `partner_id:Many2one`, `requested_by:Many2one`, `supervisor_id:Many2one`, `state:Selection`, `credit_limit:Float`, `credit_used:Float`, `order_amount:Monetary`, `exceeded_by:Float`, `currency_id:Many2one`, `rejection_reason_id:Many2one`, `rejection_notes:Text`, `approval_date:Datetime`, `company_id:Many2one`; methods: `create()`, `action_submit()`, `action_approve()`, `action_reject()`, `action_cancel()`, `action_resubmit()` …
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; fields: `credit_approval_id:Many2one`, `credit_approval_state:Selection`, `is_credit_blocked:Boolean`; methods: `action_confirm()` …
- **Menu declarations:** `Credit Approval`, `Approval Requests`, `Rejection Reasons`
- **View architectures detected:** form: 3, list: 2, search: 2, xpath: 3
- **ACL entries:** `credit.rejection.reason.manager` (group `el_nmo_credit_approval.group_credit_approval_manager/1/1/1`), `credit.rejection.reason.supervisor` (group `el_nmo_credit_approval.group_credit_approval_supervisor/1/0/0`), `credit.rejection.reason.salesperson` (group `el_nmo_credit_approval.group_credit_approval_salesperson/1/0/0`), `credit.approval.request.manager` (group `el_nmo_credit_approval.group_credit_approval_manager/1/1/1`), `credit.approval.request.supervisor` (group `el_nmo_credit_approval.group_credit_approval_supervisor/1/1/0`), `credit.approval.request.salesperson` (group `el_nmo_credit_approval.group_credit_approval_salesperson/1/0/1`), `credit.approval.wizard.manager` (group `el_nmo_credit_approval.group_credit_approval_manager/1/1/1`), `credit.approval.wizard.supervisor` (group `el_nmo_credit_approval.group_credit_approval_supervisor/1/1/1`), `credit.approval.wizard.salesperson` (group `el_nmo_credit_approval.group_credit_approval_salesperson/1/0/1`)
- **Functional file groups:** Wizards: `wizard/credit_approval_wizard.py`, `wizard/credit_approval_wizard_views.xml`, `wizard/__init__.py`; Security: `security/ir.model.access.csv`, `security/groups.xml`; Data: `data/default_rejection_reasons.xml`; Views: `views/credit_approval_request_views.xml`, `views/menu.xml`, `views/sale_order_views.xml`, `views/credit_rejection_reason_views.xml`
- **Tests present:** `tests/test_credit_approval.py`, `tests/__init__.py`

### ODOO19 / `el_nmo_sale_payment_gateway` — Sale Payment Gateway

- **Manifest version:** `19.0.1.2.0`  
- **Summary:** Payment Gateway on Sales/Invoice/Delivery + auto-sync Receivable & Payable accounts from gateway to partner  
- **Category / license / author:** `Sales` / `LGPL-3` / `Zelal Alhayek`  
- **Dependencies:** `sale_management`, `account`, `stock`, `delivery`  
- **Source inventory:** 15 files; 8 Python, 5 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `SalePaymentGateway` (`_name = sale.payment.gateway`) — `models/sale_payment_gateway.py`; fields: `name:Char`, `active:Boolean`, `property_account_receivable_id:Many2one`, `property_account_payable_id:Many2one`; methods: `write()`
  - `AccountMove` extends `account.move` — `models/account_move.py`; fields: `payment_gateway_id:Many2one`, `carrier_id:Many2one`
  - `ResPartner` extends `res.partner` — `models/res_partner.py`; fields: `payment_gateway_id:Many2one`; methods: `create()`, `write()` …
  - `StockPicking` extends `stock.picking` — `models/stock_picking.py`; fields: `payment_gateway_id:Many2one`; methods: `write()`
  - `StockMove` extends `stock.move` — `models/stock_picking.py`; fields: `payment_gateway_id:Many2one`; methods: `_get_new_picking_values()`
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; fields: `payment_gateway_id:Many2one`; methods: `write()` …
- **Menu declarations:** `Payment Gateways`
- **View architectures detected:** form: 1, list: 1, xpath: 4
- **ACL entries:** `payment.gateway.user` (group `base.group_user/1/1/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`; Views: `views/res_partner_views.xml`, `views/sale_order_views.xml`, `views/payment_gateway_views.xml`, `views/stock_picking_views.xml`, `views/account_move_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `el_payroll_wps` — Payroll WPS Export

- **Manifest version:** `19.0.1.2.0`  
- **Summary:** Adds an 'Others' field to payslips and the bank salary file export (WPS)  
- **Category / license / author:** `Human Resources/Payroll` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `hr_payroll`  
- **Source inventory:** 44 files; 9 Python, 2 XML, 0 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestWpsExport` — `tests/test_wps_export.py`; methods: `setUpClass()`, `test_others_field_is_the_other_allowances()`, `test_bank_file_has_the_template_layout_and_correct_amounts()`, `test_missing_bank_account_or_id_blocks_the_export()`, `test_payslips_of_an_employee_in_the_month_are_added_together()`, `test_draft_payslips_and_other_months_are_not_exported()`, `test_csv_bank_file_has_the_bank_columns_and_correct_amounts()`, `test_csv_export_is_blocked_like_the_excel_one()` …
  - `WpsExportWizard` (`_name = wps.export.wizard`) — `wizard/wps_export_wizard.py`; fields: `month:Date`, `bank_code:Char`, `payslip_count:Integer`, `employee_count:Integer`, `total_net:Float`, `issues:Html`, `has_blocking_issue:Boolean`, `state:Selection`, `file_data:Binary`, `file_name:Char`; methods: `action_export()`, `action_export_csv()` …
  - `HrPayslip` extends `hr.payslip` — `models/hr_payslip.py`; fields: `x_others:Float`; methods: `compute_sheet()` …
- **Menu declarations:** `WPS Export`
- **View architectures detected:** field: 1, form: 1
- **ACL entries:** `wps.export.wizard.user` (group `hr_payroll.group_hr_payroll_user/1/1/1`), `wps.export.wizard.admin` (group `base.group_system/1/1/1`)
- **Functional file groups:** Wizards: `wizard/wps_export_wizard_views.xml`, `wizard/__init__.py`, `wizard/wps_export_wizard.py`; Security: `security/ir.model.access.csv`; Views: `views/hr_payslip_views.xml`
- **Tests present:** `tests/test_wps_export.py`, `tests/__init__.py`

### ODOO19 / `el_pdf_print_preview` — PDF Print Preview

- **Manifest version:** `19.0.1.1.0`  
- **Summary:** Preview PDF reports in-browser before printing — no download needed  
- **Category / license / author:** `Extra Tools/Usability` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `web`  
- **Source inventory:** 410 files; 10 Python, 4 XML, 7 JavaScript, 1 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestPdfPreview` — `tests/test_pdf_preview.py`; methods: `setUp()`, `test_01_preview_print_field_exists()`, `test_02_preview_print_default_true()`, `test_03_automatic_printing_default_false()`, `test_04_toggle_preview_print()`, `test_05_readable_fields()`, `test_06_writeable_fields()`, `test_07_preview_reload_action()`, `test_08_session_info_has_preview_fields()`, `test_09_report_override_exists()`, `test_10_controller_exists()`, `test_11_error_catcher_template()` …
  - `PrintPreviewController` — `controllers/main.py`; methods: `get_report_name()`
  - `IrHttp` extends `ir.http` — `models/ir_http.py`; methods: `session_info()`
  - `ResUsers` extends `res.users` — `models/res_users.py`; fields: `preview_print:Boolean`, `automatic_printing:Boolean`; methods: `action_preview_reload()`, `SELF_READABLE_FIELDS()`, `SELF_WRITEABLE_FIELDS()`
  - `IrActionsReport` extends `ir.actions.report` — `models/ir_actions_report.py`; methods: `_render_qweb_pdf()`
- **HTTP routes:**
  - `/pdf_print_preview/get_report_name` → `get_report_name()` in `controllers/main.py`
- **View architectures detected:** xpath: 1
- **Functional file groups:** Reports: `report/ir_actions_report_templates.xml`, `report/ir_actions_report.xml`; Controllers: `controllers/main.py`, `controllers/__init__.py`; Security: `security/ir.model.access.csv`; Views: `views/res_users_views.xml`
- **Tests present:** `tests/__init__.py`, `tests/test_pdf_preview.py`

### ODOO19 / `el_pos_customer_payment_method` — POS Customer Payment Method

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Restrict POS payment methods per customer, with POS-level defaults for customers without a specific list.  
- **Category / license / author:** `Sales/Point of Sale` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `point_of_sale`  
- **Source inventory:** 13 files; 8 Python, 2 XML, 1 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestElPosPaymentMethodFilter` — `tests/test_payment_filter.py`; methods: `setUpClass()`, `test_01_partner_field_stored()`, `test_02_pos_data_fields_include_allowed_methods()`, `test_03_child_partner_resolves_to_commercial_partner()`, `test_04_partner_data_read_returns_method_ids()`, `test_05_pos_config_defaults_field_loaded()`, `test_06_settings_related_field_roundtrip()`
  - `ResPartner` extends `res.partner` — `models/res_partner.py`; fields: `el_allowed_pos_payment_method_ids:Many2many`; methods: `_load_pos_data_fields()`
  - `ResConfigSettings` extends `res.config.settings` — `models/res_config_settings.py`; fields: `pos_el_default_payment_method_ids:Many2many`
  - `PosConfig` extends `pos.config` — `models/pos_config.py`; fields: `el_pos_default_payment_method_ids:Many2many`
- **View architectures detected:** xpath: 2
- **Functional file groups:** Views: `views/res_partner_views.xml`, `views/res_config_settings_views.xml`
- **Tests present:** `tests/__init__.py`, `tests/test_payment_filter.py`

### ODOO19 / `el_prevent_negative_stock` — Prevent Negative Stock

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Prevent negative stock — block stock moves AND sales orders when stock is insufficient  
- **Category / license / author:** `Inventory/Security` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `stock`, `mail`, `sale_management`, `nmo_sale_order_approval_workflow`, `nmo_stock_user_restriction`  
- **Source inventory:** 31 files; 8 Python, 5 XML, 0 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestPreventNegativeStock` — `tests/test_negative_stock.py`; methods: `setUpClass()`, `test_01_sufficient_stock()`, `test_02_insufficient_stock_rejected()`, `test_03_zero_stock_rejected()`, `test_04_exact_quantity()`, `test_05_multiple_products_mixed()` …
  - `TestPreventNegativeStockSale` — `tests/test_negative_stock.py`; methods: `setUpClass()`, `test_10_sale_with_sufficient_stock()`, `test_11_sale_with_insufficient_stock_blocked()`, `test_12_sale_with_zero_stock_blocked()`, `test_13_sale_exact_quantity_allowed()`, `test_14_sale_blocked_with_clear_message()` …
  - `ElStockAlert` (`_name = el.stock.alert`) extends `mail.thread`, `mail.activity.mixin` — `models/el_stock_alert.py`; fields: `name:Char`, `product_id:Many2one`, `location_id:Many2one`, `requested_qty:Float`, `available_qty:Float`, `move_id:Many2one`, `user_id:Many2one`, `state:Selection`, `company_id:Many2one`; methods: `create()`
  - `SaleOrder` extends `sale.order` — `models/sale_order.py`; methods: `action_confirm()`
  - `StockMove` extends `stock.move` — `models/stock_move.py`; methods: `_action_assign()`
- **Menu declarations:** `Negative Stock Alerts`, `All Alerts`
- **View architectures detected:** form: 1, list: 1, search: 1
- **ACL entries:** `el.stock.alert.user` (group `group_alert_user/1/0/0`), `el.stock.alert.manager` (group `group_alert_manager/1/1/1`), `el.stock.alert.system` (group `base.group_system/1/1/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`, `security/el_prevent_negative_stock_groups.xml`; Data: `data/mail_template.xml`, `data/sequence.xml`; Views: `views/menus.xml`, `views/el_stock_alert_views.xml`
- **Tests present:** `tests/test_negative_stock.py`, `tests/__init__.py`

### ODOO19 / `ie_stock_movement_report` — Stock Movement Report

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** PDF report of inventory movements with opening/closing balance and running value.  
- **Category / license / author:** `Inventory/Reporting` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `stock`, `stock_account`, `web`  
- **Source inventory:** 33 files; 10 Python, 4 XML, 0 JavaScript, 0 SCSS; 3 test files.  
- **Python classes / models:**
  - `TestStockMovementReportWizard` — `tests/test_stock_movement_report.py`; methods: `setUp()`, `test_01_wizard_creates_with_required_dates()`, `test_02_wizard_rejects_invalid_dates()`, `test_03_optional_fields_default_falsy()`, `test_04_action_print_pdf_returns_dict()`
  - `TestStockMovementReportModel` — `tests/test_stock_movement_report.py`; methods: `setUp()`, `test_05_empty_period_returns_empty_payload()`, `test_06_invalid_date_range_raises_usererror()`, `test_07_build_base_domain_no_filters()`, `test_08_build_base_domain_with_warehouse()`, `test_09_build_base_domain_with_location()`, `test_10_build_base_domain_with_product()`, `test_11_build_base_domain_with_category()`, `test_12_prefetch_product_data_returns_expected_keys()`, `test_13_prefetch_names_returns_id_to_name_dict()`, `test_14_empty_payload_structure()`
  - `TestStockMovementReportPermissions` — `tests/test_permissions.py`; methods: `setUp()`, `test_01_manager_can_create()`, `test_02_manager_can_write()`, `test_03_manager_can_unlink()`, `test_04_user_cannot_unlink()`
  - `StockMovementReportHandler` (`_name = report.ie_stock_movement_report.report_stock_movement_document`) — `reports/stock_movement_report.py`; methods: `_get_report_values()`, `_dict_to_obj()`
  - `StockMovementReport` (`_name = stock.movement.report`) — `models/stock_movement_report.py`; methods: `get_report_data()` …
  - `StockMovementReportWizard` (`_name = stock.movement.report.wizard`) — `models/stock_movement_report.py`; fields: `date_from:Date`, `date_to:Date`, `warehouse_id:Many2one`, `location_id:Many2one`, `product_id:Many2one`, `categ_id:Many2one`; methods: `action_print_pdf()` …
- **Menu declarations:** `Stock Movement Report`
- **View architectures detected:** form: 1
- **ACL entries:** `stock.movement.report.wizard.user` (group `group_stock_movement_report_user/1/1/1`), `stock.movement.report.wizard.manager` (group `group_stock_movement_report_manager/1/1/1`)
- **Functional file groups:** Wizards: `wizard/__init__.py`, `wizard/stock_movement_report_wizard_views.xml`; Security: `security/ir.model.access.csv`, `security/ir.module.privilege.xml`; Views: `views/stock_movement_report_menu.xml`
- **Tests present:** `tests/test_stock_movement_report.py`, `tests/__init__.py`, `tests/test_permissions.py`

### ODOO19 / `inventory_report_generator` — Inventory All In One Report Generator

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Dynamic Inventory Report Generator for Odoo 17  
- **Category / license / author:** `Productivity` / `AGPL-3` / `Cybrosys Techno Solutions`  
- **Dependencies:** `stock`  
- **Source inventory:** 17 files; 8 Python, 3 XML, 1 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `InventoryPDFReport` (`_name = report.inventory_report_generator.inventory_pdf_report`) — `report/inventory_pdf_report.py`; methods: `_get_report_values()`
  - `InventoryReportGenerator` — `controllers/inventory_report_generator.py`; methods: `get_report_xlsx()`
  - `DynamicInventoryReport` (`_name = dynamic.inventory.report`) — `models/dynamic_inventory_report.py`; fields: `purchase_report:Char`, `date_from:Datetime`, `date_to:Datetime`, `report_type:Selection`; methods: `inventory_report()`, `get_filter()`, `get_filter_data()`, `create()`, `write()`, `get_inventory_xlsx_report()` …
- **HTTP routes:**
  - `/inventory_dynamic_xlsx_reports` → `get_report_xlsx()` in `controllers/inventory_report_generator.py`
- **Menu declarations:** `All In One Inventory Report`
- **ACL entries:** `access.dynamic.inventory.report.user` (group `base.group_user/1/1/1`)
- **Functional file groups:** Reports: `report/inventory_pdf_report.py`, `report/__init__.py`, `report/inventory_pdf_report_templates.xml`; Controllers: `controllers/__init__.py`, `controllers/inventory_report_generator.py`; Security: `security/ir.model.access.csv`; Views: `views/inventory_report_views.xml`
- **Tests present:** No test files detected in the addon archive.
- **Implemented development-batch changes:** Batch 01: SQL company scoping, parameterized date filters, reduced duplicate computation, spreadsheet formula-injection mitigation, constrained XLSX endpoint, sanitized client errors.

### ODOO19 / `invoice_stock_move` — Stock Picking From Invoice

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Stock Picking From Customer/Supplier Invoice  
- **Category / license / author:** `Accounting` / `AGPL-3` / `Cybrosys Techno Solutions`  
- **Dependencies:** `account`, `stock`, `payment`  
- **Source inventory:** 113 files; 5 Python, 1 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `AccountMoveLine` extends `account.move.line` — `models/account_move_line.py`; methods: `_create_stock_moves()`
  - `AccountMove` extends `account.move` — `models/account_move.py`; fields: `picking_count:Integer`, `invoice_picking_id:Many2one`, `picking_type_id:Many2one`; methods: `action_stock_move()`, `action_view_picking()` …
- **View architectures detected:** xpath: 1
- **Functional file groups:** Views: `views/account_move_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `invoice_tracking` — Invoice Tracking

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Brief description of the module  
- **Category / license / author:** `accounting` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `mail`, `account`, `purchase`  
- **Source inventory:** 24 files; 13 Python, 9 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `PublicImage` — `controller/main.py`; methods: `get_partner_image()`
  - `CheckTracking` (`_name = check.tracking`) extends `mail.thread`, `mail.activity.mixin` — `models/check_tracking.py`; fields: `name:Char`, `company_id:Many2one`, `check_type:Selection`, `partner_id:Many2one`, `amount:Monetary`, `currency_id:Many2one`, `secondary_amount:Monetary`, `secondary_currency_id:Many2one`, `date_issue:Date`, `date_due:Date`, `bank_id:Many2one`, `journal_id:Many2one`, `attachment_ids:Many2many`, `receivable_account_id:Many2one`, `payable_account_id:Many2one`, `bank_account_id:Many2one`, `move_ids:One2many`, `move_count:Integer` …; methods: `action_confirm()`, `action_deposit()`, `action_clear()`, `action_bounce()`, `action_issue()`, `action_cash()`, `action_view_entries()` …
  - `AccountMove` extends `account.move` — `models/account_move.py`; fields: `code_id:Many2one`, `check_tracking_id:Many2one`, `check_stage:Selection`; methods: `change_partner()`
  - `Well` (`_name = oil.well`) — `models/well.py`; fields: `name:Char`
  - `ResCompany` extends `res.company` — `models/res_company.py`; fields: `cheque_received_account_id:Many2one`, `cheque_under_collection_account_id:Many2one`, `cheque_issued_account_id:Many2one`
  - `PartnerCode` (`_name = partner.code`) — `models/res_partner.py`; fields: `name:Char`
  - `ResPartner` extends `res.partner` — `models/res_partner.py`; fields: `code_id:Many2one`
  - `ResConfigSettings` extends `res.config.settings` — `models/res_config_settings.py`; fields: `cheque_received_account_id:Many2one`, `cheque_under_collection_account_id:Many2one`, `cheque_issued_account_id:Many2one`
  - `PurchaseOrder` extends `purchase.order` — `models/purshase_order.py`; fields: `tracking_count:Integer`; methods: `action_create_invoice_tracking()`, `action_view_invoice_tracking()` …
  - `InvoiceTracking` (`_name = invoice.tracking`) extends `mail.thread`, `mail.activity.mixin` — `models/invoice_tracking.py`; fields: `name:Char`, `bill_reference:Char`, `code_id:Many2one`, `partner_id:Many2one`, `purchase_id:Many2one`, `vendor_bill_id:Many2one`, `purchase_reference:Char`, `received_date:Date`, `bill_date:Date`, `del_to_administration:Date`, `rec_from_administration:Date`, `purchase_line_ids:One2many`, `currency_id:Many2one`, `egp_currency_id:Many2one`, `usd_currency_id:Many2one`, `total_invoice_amount:Monetary`, `approved_egp_amount:Monetary`, `approved_usd_amount:Monetary` …; methods: `create()`, `write()`, `action_receive()`, `action_del_to_administration()`, `action_rec_from_administration()`, `action_cancel()`, `action_reset_to_draft()`, `action_create_bill_from_invoice_tracking()`, `action_view_purchase_order()`, `action_view_vendor_bill()`, `change_partner()`, `unlink()` …
- **HTTP routes:**
  - `/public/partner/image/<int:partner_id>` → `get_partner_image()` in `controller/main.py`
- **Menu declarations:** `Invoice Tracking`, `Vendor Code`, `Well Number`, `Checks`
- **View architectures detected:** form: 4, list: 4, xpath: 6
- **ACL entries:** `access.invoice.tracking.user` (group `base.group_user/1/1/1`), `access.partner.code` (group `base.group_user/1/1/1`), `access_oil_well` (group `base.group_user/1/1/1`), `access_check_tracking` (group `base.group_user/1/1/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`; Data: `data/invoice_tracking_sequence.xml`; Views: `views/res_partner_views.xml`, `views/well_view.xml`, `views/menu_item.xml`, `views/purchase_order_views.xml`, `views/check_tracking_views.xml`, `views/invoice_tracking_views.xml`, `views/res_config_settings_views.xml`, `views/account_move_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `loan_management` — Loans Management

- **Manifest version:** `19.0.2.0.0`  
- **Summary:** Manages employees' loans  
- **Category / license / author:** `Hidden` / `Other proprietary` / `Abdullah Al-Habbal`  
- **Dependencies:** `base`, `hr_payroll`  
- **Source inventory:** 15 files; 8 Python, 4 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `Loan` (`_name = loan`) extends `mail.thread` — `models/loan.py`; fields: `employee_id:Many2one`, `date:Date`, `amount:Monetary`, `reason:Text`, `loan_lines:One2many`, `installments_count:Char`, `company_id:Many2one`, `state:Selection`, `currency_id:Many2one`; methods: `compute_installments()`, `employee_id_domain()`, `button_approve()`, `button_reject()`, `button_draft()`, `get_admins()`, `write()`, `unlink()`
  - `LoanLine` (`_name = loan.line`) — `models/loan_line.py`; fields: `loan_id:Many2one`, `employee_id:Many2one`, `payment_date:Date`, `amount:Monetary`, `state:Selection`, `loan_state:Selection`, `company_id:Many2one`, `currency_id:Many2one`, `note:Html`; methods: `write()`
  - `HrPayslip` extends `hr.payslip` — `models/hr_payslip.py`; fields: `loan_total:Float`, `loan_before:Float`, `loan_after:Float`; methods: `action_payslip_paid()`, `action_payslip_unpaid()`, `action_payslip_cancel()`
- **Menu declarations:** `Loans Management`, `Installments`, `Payment Schedule`
- **View architectures detected:** form: 1, list: 2, search: 1, xpath: 1
- **Record rules:** `Loan rule`, `Loans: Only see loans of own company`
- **ACL entries:** `loan.user` (group `loan_management.group_loan_user/1/0/0`), `loan.line.user` (group `loan_management.group_loan_user/1/0/0`), `loan.manager` (group `loan_management.group_loan_manager/1/1/1`), `loan.line.manager` (group `loan_management.group_loan_manager/1/1/1`)
- **Functional file groups:** Reports: `report/hr_payslip_report.xml`; Controllers: `controllers/controllers.py`, `controllers/__init__.py`; Security: `security/ir.model.access.csv`, `security/security.xml`; Views: `views/loan_views.xml`, `views/hr_payslip_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `meno` — meno

- **Manifest version:** `18.0`  
- **Summary:** Crack odoo v19  
- **Category / license / author:** `not declared` / `not declared` / `meno`  
- **Dependencies:** `base`, `base_setup`  
- **Source inventory:** 10 files; 6 Python, 3 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ir_module_module` extends `ir.module.module` — `models/models.py`; methods: `crack()`, `cracks()`, `button_immediate_upgrade()`
  - `IrConfigParameter` extends `ir.config_parameter` — `models/models.py`; methods: `cracks()`
- **ACL entries:** `crack.crack` (group `/1/0/0`)
- **Functional file groups:** Controllers: `controllers/controllers.py`, `controllers/__init__.py`; Security: `security/ir.model.access.csv`; Data: `data/cracks_test.xml`; Views: `views/views.xml`, `views/templates.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `mrp_lock_lines` — MRP Lock Lines

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Lock all component lines in Manufacturing Order except the last one  
- **Category / license / author:** `Manufacturing/Manufacturing` / `LGPL-3` / `Masry`  
- **Dependencies:** `mrp`, `stock`  
- **Source inventory:** 6 files; 4 Python, 1 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `StockMoveLine` extends `stock.move.line` — `models/stock_move_line.py`; fields: `is_last_line:Boolean`; methods: `_compute_is_last_line()`
  - `StockMove` extends `stock.move` — `models/stock_move_line.py`; fields: `is_last_line:Boolean`; methods: `_compute_is_last_line()`
- **View architectures detected:** xpath: 1
- **Functional file groups:** Views: `views/mrp_production_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `partner_balance_confirmation` — Balance Confirmation

- **Manifest version:** `19.0.3.6.0`  
- **Summary:** Customer Balance Confirmation (Imdad / Namo templates)  
- **Category / license / author:** `Accounting` / `LGPL-3` / `Z.ai`  
- **Dependencies:** `base`, `mail`, `account`  
- **Source inventory:** 26 files; 7 Python, 5 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `BalanceConfirmationWizard` (`_name = balance.confirmation.wizard`) — `wizard/balance_confirmation_wizard.py`; fields: `partner_id:Many2one`, `confirmation_date:Date`, `template_type:Selection`, `notes:Text`, `printed_by:Many2one`, `balance:Monetary`, `balance_text:Char`, `currency_id:Many2one`; methods: `action_print_pdf()`, `action_print_word()`, `action_send_email()` …
  - `ResPartner` extends `res.partner` — `models/res_partner.py`; methods: `action_open_balance_confirmation()` …
- **View architectures detected:** form: 1, xpath: 1
- **ACL entries:** `balance.confirmation.wizard` (group `base.group_user/1/1/1`)
- **Functional file groups:** Wizards: `wizard/balance_confirmation_wizard.py`, `wizard/balance_confirmation_wizard_views.xml`, `wizard/__init__.py`; Security: `security/ir.model.access.csv`; Data: `data/mail_template.xml`, `data/template_namo.docx`, `data/template_amdad.docx`; Views: `views/res_partner_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `partner_request` — Partner Request

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Approval workflow for creating new customers via sales requests.  
- **Category / license / author:** `Sales/Sales` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `sale`, `sales_team`, `customer_classification`  
- **Source inventory:** 11 files; 4 Python, 4 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `PartnerRequest` (`_name = partner.request`) extends `mail.thread`, `mail.activity.mixin` — `models/partner_request.py`; fields: `name:Char`, `customer_code:Char`, `classification_id:Many2one`, `contact_person:Char`, `partner_id:Many2one`, `sequence:Char`, `country_id:Many2one`, `state_id:Many2one`, `city:Char`, `area:Char`, `street:Char`, `zip:Char`, `pobox:Char`, `phone:Char`, `email:Char`, `vat:Char`, `sales_supervisor_id:Many2one`, `salesperson_id:Many2one` …; methods: `create()`, `action_submit()`, `action_create_partner()`, `action_send_back()`, `action_reject()`, `action_open_partner()` …
  - `ResPartner` extends `res.partner` — `models/partner_request.py`; methods: `create()`
- **Menu declarations:** `Partner Requests`
- **View architectures detected:** form: 1, list: 1, search: 1
- **ACL entries:** `partner.request.manager` (group `partner_request.group_partner_request_manager/1/1/1`), `partner.request.user` (group `partner_request.group_partner_request_user/1/1/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`, `security/partner_request_security.xml`; Data: `data/partner_request_data.xml`; Views: `views/partner_request_menus.xml`, `views/partner_request_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `payment_alrajhi_arb` — Al Rajhi Bank (ARB) Payment Gateway

- **Manifest version:** `19.0.1.4.12`  
- **Summary:** Official-style ARB integration: token API, encrypted trandata, bank-hosted redirect, KSA Card/Mada checkout (Odoo 19).  
- **Category / license / author:** `Accounting/Payment Providers` / `LGPL-3` / `Sirelkhatim Gamal`  
- **Dependencies:** `payment`  
- **Source inventory:** 38 files; 10 Python, 3 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ARBClient` — `services/arb_client.py`; methods: `encrypt_trandata()`, `decrypt_trandata()`, `get_customer_ip_header()`, `frame_payment_page_url()`, `prepare_redirect_form_values()`, `create_payment_token()`, `inquire_transaction()` …
  - `AlRajhiARBController` — `controllers/alrajhi_arb.py`; methods: `alrajhi_arb_return()`, `alrajhi_arb_status()` …
  - `PaymentProvider` extends `payment.provider` — `models/payment_provider.py`; fields: `code:Selection`, `arb_tranportal_id:Char`, `arb_tranportal_password:Char`, `arb_resource_key:Char`, `arb_endpoint_url_test:Char`, `arb_endpoint_url_prod:Char`; methods: `action_test_alrajhi_connection()` …
  - `PaymentTransaction` extends `payment.transaction` — `models/payment_transaction.py`; fields: `arb_track_id:Char`, `arb_return_token:Char`; methods: `_get_specific_processing_values()`, `_get_specific_rendering_values()`, `_search_by_reference()`, `_extract_amount_data()`, `_apply_updates()`, `_get_base_url()`
- **HTTP routes:**
  - `/payment/alrajhi_arb/return` → `alrajhi_arb_return()` in `controllers/alrajhi_arb.py`
  - `/payment/alrajhi_arb/status/<int:tx_id>` → `alrajhi_arb_status()` in `controllers/alrajhi_arb.py`
- **View architectures detected:** group: 1
- **Functional file groups:** Controllers: `controllers/alrajhi_arb.py`, `controllers/__init__.py`; Data: `data/payment_provider_data.xml`; Views: `views/payment_provider_views.xml`, `views/arb_redirect_form_templates.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `payment_applepay` — Hyperpay Payment Acquirer - Applepay

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Payment Acquirer: Applepay  
- **Category / license / author:** `Accounting/Payment Providers` / `Other proprietary` / `Technaureus Info Solutions Pvt. Ltd.`  
- **Dependencies:** `payment`, `website`  
- **Source inventory:** 30 files; 8 Python, 5 XML, 1 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ApplepayController` — `controllers/main.py`; methods: `applepay_return()`, `payment_applepay_card()`
  - `PaymentProvider` extends `payment.provider` — `models/payment_provider.py`; fields: `code:Selection`, `applepay_entity_id:Char`, `applepay_authorization_bearer:Char`; methods: `applepay_form_generate_values()` …
  - `PaymentTransaction` extends `payment.transaction` — `models/payment_transaction.py`; fields: `applepay_checkout_id:Char`; methods: `_get_specific_rendering_values()`, `_extract_reference()`, `_extract_amount_data()`, `_apply_updates()`
- **HTTP routes:**
  - `/payment/applepay/return` → `applepay_return()` in `controllers/main.py`
  - `/shop/applepay/payment/` → `payment_applepay_card()` in `controllers/main.py`
- **View architectures detected:** group: 1
- **Functional file groups:** Controllers: `controllers/main.py`, `controllers/__init__.py`; Data: `data/payment_method_data.xml`, `data/payment_provider_data.xml`; Views: `views/payment_provider_views.xml`, `views/payment_popup_template.xml`, `views/payment_applepay_templates.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `payment_hyperpay` — Hyperpay Payment Acquirer

- **Manifest version:** `19.0.1.0.1`  
- **Summary:** Website Hyper Pay Payment Acquirer  
- **Category / license / author:** `Accounting/Payment Providers` / `Other proprietary` / `Webkul Software Pvt. Ltd.`  
- **Dependencies:** `account`, `payment`, `website_sale`  
- **Source inventory:** 47 files; 9 Python, 4 XML, 1 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `HyperPayController` — `controllers/main.py`; methods: `create_hyperpay_checkout()`, `hyperpay_shopper_result()`
  - `PaymentProvider` extends `payment.provider` — `models/payment_provider.py`; fields: `code:Selection`, `hyperpay_authorization:Char`, `hyperpay_merchant_id:Char`, `hyperpay_data_brands:Char`; methods: `_get_default_payment_method_codes()`, `_hyperpay_get_api_domain()`, `_get_hyperpay_data_brands()`
  - `PaymentTransaction` extends `payment.transaction` — `models/payment_transaction.py`; fields: `hyperpay_checkout_id:Char`; methods: `_get_specific_rendering_values()`, `_extract_reference()`, `_extract_amount_data()`, `_apply_updates()`
- **HTTP routes:**
  - `/payment/hyperpay/checkout/create` → `create_hyperpay_checkout()` in `controllers/main.py`
  - `/payment/hyperpay/result` → `hyperpay_shopper_result()` in `controllers/main.py`
- **View architectures detected:** group: 1
- **Functional file groups:** Controllers: `controllers/main.py`, `controllers/__init__.py`; Data: `data/payment_method_data.xml`, `data/payment_provider_data.xml`; Views: `views/payment_provider_views.xml`, `views/payment_hyperpay_templates.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `pos_daily_sequence` — POS Daily Sequence

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Automatically reset POS order numbering every day  
- **Category / license / author:** `Point of Sale` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `point_of_sale`, `mail`, `stock`, `account`  
- **Source inventory:** 12 files; 6 Python, 3 XML, 1 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `PosSession` extends `pos.session` — `models/pos_session.py`; fields: `daily_sequence_id:Many2one`
  - `PosConfig` extends `pos.config` — `models/pos_config.py`; fields: `daily_sequence_id:Many2one`, `use_daily_sequence:Boolean`, `daily_sequence_prefix:Char`, `daily_sequence_reset_period:Selection`, `daily_sequence_padding:Integer`; methods: `write()`, `create()` …
  - `PosOrder` extends `pos.order` — `models/pos_order.py`; fields: `daily_order_number:Char`; methods: `read_pos_data()`, `action_pos_order_paid()` …
- **View architectures detected:** field: 3, xpath: 1
- **ACL entries:** `POS Config Daily Sequence User` (group ` /1/0/0`)
- **Functional file groups:** Security: `security/ir.model.access.csv`; Data: `data/ir_sequence_data.xml`; Views: `views/pos_config_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `pos_get_weight_button` — POS Get Weight Button

- **Manifest version:** `1.0`  
- **Summary:** Adds a Get Weight button to POS control buttons  
- **Category / license / author:** `Sales/Point of Sale` / `LGPL-3` / `not declared`  
- **Dependencies:** `point_of_sale`  
- **Source inventory:** 4 files; 2 Python, 1 XML, 1 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:** No model/class declarations detected by the static extractor; inspect source files for dynamic definitions.
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `rm_hr_attendance_sheet` — HR Attendance Sheet and Policies

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Attendance sheets, policies, overtime, lateness, absence, and payroll links  
- **Category / license / author:** `Human Resources/Attendances` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `hr_attendance`, `hr_holidays`, `hr_payroll`, `mail`  
- **Source inventory:** 30 files; 15 Python, 13 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `RmAttendanceSheetBatchWizard` (`_name = rm.attendance.sheet.batch.wizard`) — `wizards/rm_attendance_sheet_batch.py`; fields: `date_from:Date`, `date_to:Date`, `department_id:Many2one`, `employee_ids:Many2many`, `employee_category_ids:Many2many`, `calculate_now:Boolean`, `summary:Text`; methods: `action_create_sheets()`
  - `RmAttendanceSheetChangeWizard` (`_name = rm.attendance.sheet.change.wizard`) — `wizards/rm_attendance_sheet_change.py`; fields: `sheet_id:Many2one`, `line_id:Many2one`, `overtime_hours:Float`, `late_in_minutes:Float`, `difference_hours:Float`, `is_absent:Boolean`, `reason:Text`; methods: `action_apply()`, `default_get()`
  - `RmAttendancePolicy` (`_name = rm.attendance.policy`) — `models/rm_attendance_policy.py`; fields: `name:Char`, `effective_date:Date`, `overtime_rule_ids:One2many`, `lateness_rule_ids:One2many`, `absence_rule_ids:One2many`, `version_ids:One2many`, `active:Boolean`, `company_id:Many2one`
  - `HrSalaryRule` extends `hr.salary.rule` — `models/hr_salary_rule.py`; methods: `_rm_configure_attendance_basic_rule()`
  - `RmLatenessRule` (`_name = rm.lateness.rule`) — `models/rm_lateness_rule.py`; fields: `name:Char`, `step_ids:One2many`, `active:Boolean`, `policy_id:Many2one`, `company_id:Many2one`; methods: `get_penalty()`
  - `RmLatenessStep` (`_name = rm.lateness.step`) — `models/rm_lateness_rule.py`; fields: `rule_id:Many2one`, `name:Char`, `min_minutes:Integer`, `max_minutes:Integer`, `step_type:Selection`, `rate_value:Float`, `fixed_amount:Float`, `penalty_calc:Selection`, `active:Boolean`; methods: `matches()`, `get_penalty()` …
  - `HrVersion` extends `hr.version` — `models/hr_version.py`; fields: `attendance_policy_id:Many2one`
  - `RmAttendanceSheet` (`_name = rm.attendance.sheet`) extends `mail.thread`, `mail.activity.mixin` — `models/rm_attendance_sheet.py`; fields: `name:Char`, `employee_id:Many2one`, `department_id:Many2one`, `version_id:Many2one`, `policy_id:Many2one`, `date_from:Date`, `date_to:Date`, `state:Selection`, `sheet_line_ids:One2many`, `total_planned_hours:Float`, `total_worked_hours:Float`, `total_overtime:Float`, `total_working_day_overtime:Float`, `total_weekend_overtime:Float`, `total_holiday_overtime:Float`, `total_late_in:Float`, `total_absence_days:Integer`, `total_difference:Float` …; methods: `action_calculate()`, `action_confirm()`, `action_cancel()`, `action_draft()`, `action_open_change_wizard()`, `action_create_payslip()` …
  - `RmAttendanceSheetLine` (`_name = rm.attendance.sheet.line`) — `models/rm_attendance_sheet.py`; fields: `name:Char`, `sheet_id:Many2one`, `employee_id:Many2one`, `date:Date`, `day_name:Char`, `day_type:Selection`, `planned_hours:Float`, `worked_hours:Float`, `overtime_hours:Float`, `overtime_type:Selection`, `late_in_minutes:Float`, `is_absent:Boolean`, `is_leave:Boolean`, `leave_id:Many2one`, `public_holiday_id:Many2one`, `difference_hours:Float`, `overtime_amount:Float`, `late_penalty:Float` …; methods: `_compute_name()`, `_compute_day_name()`
  - `RmOvertimeRule` (`_name = rm.overtime.rule`) — `models/rm_overtime_rule.py`; fields: `name:Char`, `ot_type:Selection`, `apply_after:Float`, `rate:Float`, `active:Boolean`, `policy_id:Many2one`, `company_id:Many2one`; methods: `_check_values()`
  - `HrPayslip` extends `hr.payslip` — `models/hr_payslip.py`; fields: `attendance_sheet_id:Many2one`
  - `ResourceCalendarLeaves` extends `resource.calendar.leaves` — `models/resource_calendar_leaves.py`; fields: `active_for_overtime:Boolean`, `rm_public_holiday:Boolean`, `employee_ids:Many2many`, `department_ids:Many2many`, `employee_category_ids:Many2many`; methods: `applies_to_employee()`
  - `RmAbsenceRule` (`_name = rm.absence.rule`) — `models/rm_absence_rule.py`; fields: `name:Char`, `step_ids:One2many`, `active:Boolean`, `policy_id:Many2one`, `company_id:Many2one`; methods: `get_penalty()`
  - `RmAbsenceStep` (`_name = rm.absence.step`) — `models/rm_absence_rule.py`; fields: `rule_id:Many2one`, `name:Char`, `min_days:Integer`, `max_days:Integer`, `step_type:Selection`, `rate_value:Float`, `fixed_amount:Float`, `active:Boolean`; methods: `matches()`, `get_penalty()` …
- **Menu declarations:** `Attendance Sheets`, `Attendance Sheets`, `Batch Attendance Sheets`, `Attendance Policies`, `Attendance Policies`, `Overtime Rules`, `Lateness Rules`, `Absence Rules`, `Public Holidays`
- **View architectures detected:** form: 7, list: 6, search: 1, xpath: 3
- **Record rules:** `Attendance Sheet: company`, `Attendance Sheet Line: company`
- **ACL entries:** `rm.overtime.rule user` (group `group_attendance_sheet_user/1/0/0`), `rm.overtime.rule manager` (group `group_attendance_sheet_manager/1/1/1`), `rm.lateness.rule user` (group `group_attendance_sheet_user/1/0/0`), `rm.lateness.rule manager` (group `group_attendance_sheet_manager/1/1/1`), `rm.lateness.step user` (group `group_attendance_sheet_user/1/0/0`), `rm.lateness.step manager` (group `group_attendance_sheet_manager/1/1/1`), `rm.absence.rule user` (group `group_attendance_sheet_user/1/0/0`), `rm.absence.rule manager` (group `group_attendance_sheet_manager/1/1/1`), `rm.absence.step user` (group `group_attendance_sheet_user/1/0/0`), `rm.absence.step manager` (group `group_attendance_sheet_manager/1/1/1`), `rm.attendance.policy user` (group `group_attendance_sheet_user/1/0/0`), `rm.attendance.policy manager` (group `group_attendance_sheet_manager/1/1/1`), `rm.attendance.sheet user` (group `group_attendance_sheet_user/1/1/1`), `rm.attendance.sheet manager` (group `group_attendance_sheet_manager/1/1/1`), `rm.attendance.sheet.line user` (group `group_attendance_sheet_user/1/1/1`), `rm.attendance.sheet.line manager` (group `group_attendance_sheet_manager/1/1/1`), `rm.attendance.sheet.change.wizard` (group `group_attendance_sheet_user/1/1/1`), `rm.attendance.sheet.batch.wizard` (group `group_attendance_sheet_user/1/1/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`, `security/groups.xml`; Data: `data/hr_salary_rule_data.xml`; Views: `views/rm_lateness_rule_views.xml`, `views/hr_version_views.xml`, `views/rm_overtime_rule_views.xml`, `views/hr_menu.xml`, `views/rm_attendance_policy_views.xml`, `views/rm_absence_rule_views.xml`, `views/hr_payslip_views.xml`, `views/resource_calendar_leaves_views.xml` …
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `saudi_tax_invoice` — Saudi Tax Invoice

- **Manifest version:** `1.0`  
- **Summary:** Saudi-style tax invoice PDF with action button  
- **Category / license / author:** `Accounting` / `LGPL-3` / `not declared`  
- **Dependencies:** `account`  
- **Source inventory:** 5 files; 3 Python, 1 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:** No model/class declarations detected by the static extractor; inspect source files for dynamic definitions.
- **Functional file groups:** Reports: `report/__init__.py`, `report/templates.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `smsa_express_delivery_carrier` — SMSA Express Shipping Integration

- **Manifest version:** `1.0.3`  
- **Summary:** The module allows the user to Integrate SMSA Web Services with Client Application (SECOM) with Odoo. Once integrated, the shipping method can be used on Odoo website by customers to get their orders delivered and in the Odoo backend by the user.
                    SMSA | SMSA Express | SMSA Express Odoo integration | SMSA shipping | SMSA tracking | SMSA lable generation |
                    SMSA Express API integration | SMSA shipping solution | SMSA Express Odoo | SMSA API | Odoo SMSA module |
                    SMSA Odoo | SMSA integration | Shipping | Delivery | Shipping integration | Smsa shipping extension.
                  
- **Category / license / author:** `Warehouse` / `Other proprietary` / `Webkul Software Pvt. Ltd.`  
- **Dependencies:** `odoo_shipping_service_apps`  
- **Source inventory:** 43 files; 7 Python, 3 XML, 0 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `FakeResponse` — `tests/test_smsa_shipping.py`; methods: `json()` …
  - `TestSmsaShipping` — `tests/test_smsa_shipping.py`; methods: `setUpClass()`, `test_payload_has_every_field_smsa_requires()`, `test_cash_on_delivery_collects_the_unpaid_amount()`, `test_send_to_shipper_creates_the_waybill()`, `test_waybill_without_file_keeps_the_tracking_number()`, `test_missing_data_is_reported_at_once_before_calling_smsa()`, `test_missing_passkey()`, `test_smsa_validation_errors_are_readable()`, `test_rejected_passkey()`, `test_service_down_and_timeout()`, `test_package_type_search()` …
  - `SmsaExpressAPI` — `models/smsa_delivery_carrier.py`; methods: `__init__()`, `_request_header()`, `_smsa_send_request()`
  - `SmsaDeliveryCarrier` extends `delivery.carrier` — `models/smsa_delivery_carrier.py`; methods: `smsa_rate_shipment()`, `smsa_send_shipping()`, `smsa_cancel_shipment()`, `smsa_get_tracking_link()`, `smsa_get_return_label()` …
  - `SmsaShippingService` extends `delivery.carrier` — `models/smsa_shipping_service.py`; fields: `delivery_type:Selection`, `smsa_test_passkey:Char`, `smsa_prod_passkey:Char`, `is_cod:Boolean`, `smsa_service_type:Many2one`, `smsa_return_service_type:Many2one`, `smsa_label_type:Selection`
  - `SMSAProductPackaging` extends `stock.package.type` — `models/smsa_shipping_service.py`; fields: `package_carrier_type:Selection`
  - `StockPicking` extends `stock.picking` — `models/smsa_shipping_service.py`; fields: `smsa_sawb:Char`, `wk_content_description:Char`; methods: `get_all_wk_carriers()`, `send_to_shipper()`
  - `SMSAServices` (`_name = delivery.smsa.service`) — `models/smsa_shipping_service.py`; fields: `name:Char`, `code:Char`
  - `SMSAReturnServices` (`_name = delivery.smsa.return.service`) — `models/smsa_shipping_service.py`; fields: `name:Char`, `code:Char`
- **View architectures detected:** xpath: 2
- **ACL entries:** `delivery.smsa.service` (group `stock.group_stock_user/1/0/0`), `delivery.smsa.service` (group `stock.group_stock_manager/1/1/1`), `delivery.smsa.return.service` (group `stock.group_stock_user/1/0/0`), `delivery.smsa.return.service` (group `stock.group_stock_manager/1/1/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`; Data: `data/data.xml`, `data/delivery_demo.xml`; Views: `views/smsa_shipping_service.xml`
- **Tests present:** `tests/test_smsa_shipping.py`, `tests/__init__.py`

### ODOO19 / `stock_intercompany_transfer` — Inter Company Stock Transfer

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Create counterpart Receipt/Delivery Orders between
    companies.  
- **Category / license / author:** `Inventory` / `AGPL-3` / `Cybrosys Techno Solutions`  
- **Dependencies:** `stock`, `account`  
- **Source inventory:** 94 files; 7 Python, 1 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `StockBackorderConfirmation` extends `stock.backorder.confirmation` — `wizard/stock_backorder_confirmation.py`; fields: `stock_id:Many2one`; methods: `process()`, `process_cancel_backorder()`
  - `ResCompany` extends `res.company` — `models/res_company.py`; fields: `enable_inter_company_transfer:Boolean`, `destination_warehouse_id:Many2one`, `apply_transfer_type:Selection`, `message:Text`; methods: `compute_message()`, `onchange_inter_company_transfer()`
  - `StockPickingInherit` extends `stock.picking` — `models/stock_picking.py`; fields: `auto_generated:Boolean`, `is_backorder_button_clicked:Boolean`; methods: `button_validate()`, `create_intercompany_transfer()`
- **View architectures detected:** xpath: 1
- **Functional file groups:** Wizards: `wizard/__init__.py`, `wizard/stock_backorder_confirmation.py`; Views: `views/res_company_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `test_AI_finance` — AI Finance V1

- **Manifest version:** `1.8`  
- **Summary:** Advanced AI Finance Module: Virtual CFO & OCR Engine  
- **Category / license / author:** `Accounting/Finance` / `LGPL-3` / `AI Finance Team`  
- **Dependencies:** `base`, `mail`, `account`  
- **Source inventory:** 37 files; 14 Python, 13 XML, 3 JavaScript, 3 SCSS; 0 test files.  
- **Python classes / models:**
  - `VendorBillWizard` (`_name = test.ai.vendor.bill.wizard`) — `wizards/vendor_bill_wizard.py`; fields: `document_type:Selection`, `bank_account_id:Many2one`, `reference_code:Char`, `statement_date_from:Date`, `statement_date_to:Date`, `state:Selection`, `invoice_file:Binary`, `filename:Char`, `vendor_id:Many2one`, `vendor_name_extracted:Char`, `invoice_number:Char`, `invoice_date:Date`, `due_date:Date`, `currency_id:Many2one`, `subtotal:Float`, `tax_amount:Float`, `total_amount:Float`, `line_ids:One2many` …; methods: `action_select_type()`, `action_back_to_type()`, `action_process_file()`, `action_create_bank_statement()`, `action_create_bill()`, `action_create_statement_from_review()`, `action_back_to_upload()`, `action_create_refund()` …
  - `VendorBillWizardLine` (`_name = test.ai.vendor.bill.wizard.line`) — `wizards/vendor_bill_wizard.py`; fields: `wizard_id:Many2one`, `description:Char`, `quantity:Float`, `unit_price:Float`, `discount:Float`, `total:Float`; methods: `_compute_total()`
  - `VendorBillWizardColumn` (`_name = test.ai.vendor.bill.wizard.column`) — `wizards/vendor_bill_wizard.py`; fields: `wizard_id:Many2one`, `column_name:Char`, `is_recommended:Boolean`, `display_label:Char`; methods: `_compute_display_label()`
  - `CFOQueryWizard` (`_name = test.ai.cfo.query.wizard`) — `wizards/cfo_query_wizard.py`; fields: `cfo_agent_id:Many2one`, `question:Text`, `suggested_question:Selection`, `answer:Html`, `show_answer:Boolean`; methods: `action_ask()`, `action_new_question()` …
  - `AICredential` (`_name = test.ai.credential`) — `models/ai_credential.py`; fields: `name:Char`, `provider:Selection`, `api_key:Char`, `api_base_url:Char`, `anonymize_data:Boolean`, `gemini_model:Selection`, `openai_model:Selection`, `groq_model:Selection`, `deepseek_model:Selection`, `claude_model:Selection`, `xai_model:Selection`, `mistral_model:Selection`, `cohere_model:Selection`, `custom_model_name:Char`, `model_version:Selection`, `last_tested_date:Datetime`, `status:Selection`; methods: `get_effective_model()`, `action_test_connection()` …
  - `AIFinanceConfig` extends `res.config.settings` — `models/ai_config.py`; fields: `ocr_credential_id:Many2one`, `virtual_cfo_credential_id:Many2one`; methods: `default_get()`, `get_config()`
  - `VendorStatement` (`_name = test.ai.vendor.statement`) extends `mail.thread`, `mail.activity.mixin` — `models/vendor_statement.py`; fields: `name:Char`, `partner_id:Many2one`, `statement_date:Date`, `currency_id:Many2one`, `date_from:Date`, `date_to:Date`, `statement_total_due:Monetary`, `odoo_total_due:Monetary`, `difference_amount:Monetary`, `line_ids:One2many`, `state:Selection`, `ocr_raw_text:Text`, `statement_column_ids:One2many`, `selected_column_id:Many2one`, `extracted_columns:Char`, `match_key_column:Selection`, `summary_total_lines:Integer`, `summary_matched:Integer` …; methods: `create()`, `action_match_lines()`, `action_confirm_matches()`, `action_rematch()`, `action_print_report()` …
  - `VendorStatementLine` (`_name = test.ai.vendor.statement.line`) — `models/vendor_statement.py`; fields: `statement_id:Many2one`, `date:Date`, `name:Char`, `voucher_number:Char`, `amount:Monetary`, `currency_id:Many2one`, `matched_move_line_id:Many2one`, `candidate_move_line_ids:Many2many`, `matched_partner_id:Many2one`, `odoo_amount_residual:Monetary`, `match_status:Selection`, `match_notes:Char`, `is_odoo_only:Boolean`
  - `VendorStatementColumn` (`_name = test.ai.vendor.statement.column`) — `models/vendor_statement.py`; fields: `statement_id:Many2one`, `column_name:Char`, `is_recommended:Boolean`, `display_label:Char`; methods: `_compute_display_label()`
  - `AccountBankStatementFix` extends `account.bank.statement` — `models/account_bank_statement.py`; fields: `journal_has_invalid_statements:Boolean`; methods: `_compute_journal_has_invalid_statements()`
  - `VirtualCFOAgent` (`_name = test.ai.virtual.cfo.agent`) extends `mail.thread` — `models/virtual_cfo_agent.py`; fields: `name:Char`, `user_id:Many2one`, `company_id:Many2one`, `conversation_ids:One2many`, `query_count:Integer`, `recommendation_count:Integer`; methods: `create()`, `ask_question()`, `action_new_conversation()`, `action_view_recommendations()`, `action_generate_insights()` …
  - `CFOConversation` (`_name = test.ai.cfo.conversation`) — `models/virtual_cfo_agent.py`; fields: `cfo_agent_id:Many2one`, `question:Text`, `answer:Html`, `state:Selection`, `context_used:Text`, `ai_model:Char`, `processing_time:Float`, `error_message:Text`
  - `AIFinanceDashboard` (`_name = test.ai.finance.dashboard`) — `models/ai_finance_dashboard.py`; fields: `name:Char`, `company_id:Many2one`, `currency_id:Many2one`, `date_from:Date`, `date_to:Date`, `total_sales:Monetary`, `total_purchases:Monetary`, `gross_profit:Monetary`, `profit_margin:Float`, `total_receivable:Monetary`, `total_payable:Monetary`, `invoices_to_collect:Integer`, `bills_to_pay:Integer`, `collection_rate:Float`, `payment_rate:Float`, `total_overdue_receivable:Monetary`, `total_overdue_payable:Monetary`, `total_bank_balance:Monetary` …; methods: `action_refresh()`, `action_open_receivables()`, `action_open_payables()`, `action_open_overdue()`, `action_open_bank_journals()`, `action_open_dashboard()`, `action_period_this_month()`, `action_period_last_month()`, `action_period_this_quarter()`, `action_period_this_year()`, `action_open_aging()`, `get_dashboard_data()` …
  - `BankStatement` (`_name = test.ai.bank.statement`) extends `mail.thread`, `mail.activity.mixin` — `models/bank_statement.py`; fields: `name:Char`, `bank_account_id:Many2one`, `bank_name:Char`, `account_number:Char`, `date_from:Date`, `date_to:Date`, `opening_balance:Monetary`, `closing_balance:Monetary`, `odoo_balance:Monetary`, `difference:Monetary`, `currency_id:Many2one`, `line_ids:One2many`, `state:Selection`, `ocr_raw_text:Text`, `summary_total_lines:Integer`, `summary_matched:Integer`, `summary_discrepancy:Integer`, `summary_missing_odoo:Integer` …; methods: `create()`, `action_match_lines()`, `action_confirm_matches()`, `action_rematch()`, `action_print_report()` …
  - `BankStatementLine` (`_name = test.ai.bank.statement.line`) — `models/bank_statement.py`; fields: `statement_id:Many2one`, `date:Date`, `description:Char`, `debit:Float`, `credit:Float`, `balance:Float`, `is_odoo_only:Boolean`, `matched_move_line_id:Many2one`, `candidate_move_line_ids:Many2many`, `matched_partner_id:Many2one`, `currency_id:Many2one`, `match_status:Selection`, `match_notes:Char`
  - `AIRefundTracking` (`_name = test.ai.refund.tracking`) extends `mail.thread`, `mail.activity.mixin` — `models/ai_refund_tracking.py`; fields: `ticket_number:Char`, `name:Char`, `vendor_id:Many2one`, `currency_id:Many2one`, `refund_amount:Monetary`, `state:Selection`, `request_date:Date`, `expected_credit_date:Date`, `credit_received_date:Date`, `passenger_name:Char`, `flight_details:Char`, `refund_reason:Text`, `notes:Text`, `original_bill_id:Many2one`, `credit_note_id:Many2one`, `ocr_document:Binary`, `ocr_filename:Char`, `raw_ocr_data:Text` …; methods: `action_request_refund()`, `action_mark_approved()`, `action_receive_credit_note()`, `action_close()` …
- **Menu declarations:** `AI Finance V1`, `Dashboard`, `Analytics`, `OCR Engine`, `Virtual CFO (Chatbot)`, `Reconciliation`, `Partner Statements`, `Bank Statements`, `Configuration`, `AI Credentials`, `Settings`
- **View architectures detected:** form: 7, list: 3, xpath: 1
- **ACL entries:** `test.ai.virtual.cfo.agent` (group `base.group_user/1/1/1`), `test.ai.cfo.conversation` (group `base.group_user/1/1/1`), `test.ai.vendor.bill.wizard` (group `base.group_user/1/1/1`), `test.ai.cfo.query.wizard` (group `base.group_user/1/1/1`), `test.ai.vendor.bill.wizard.line` (group `base.group_user/1/1/1`), `test.ai.credential` (group `base.group_user/1/1/1`), `test.ai.refund.tracking` (group `base.group_user/1/1/1`), `test.ai.vendor.statement` (group `base.group_user/1/1/1`), `test.ai.vendor.statement.line` (group `base.group_user/1/1/1`), `test.ai.bank.statement` (group `base.group_user/1/1/1`), `test.ai.bank.statement.line` (group `base.group_user/1/1/1`), `test.ai.vendor.bill.wizard.column` (group `base.group_user/1/1/1`), `test.ai.vendor.statement.column` (group `base.group_user/1/1/1`), `test.ai.finance.dashboard` (group `base.group_user/1/1/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`; Views: `views/menu.xml`, `views/virtual_cfo_views.xml`, `views/ai_credential_views.xml`, `views/bank_statement_views.xml`, `views/ai_finance_dashboard_views.xml`, `views/ai_config_views.xml`, `views/vendor_statement_views.xml`, `views/ai_finance_dashboard_action.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `transaction_tracker` — Transaction Tracker

- **Manifest version:** `1.0.0`  
- **Summary:** Track all user transactions across every Odoo module  
- **Category / license / author:** `Tools` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `web`  
- **Source inventory:** 21 files; 8 Python, 8 XML, 1 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `TransactionLogReport` (`_name = report.transaction_tracker.report_transaction_log`) — `report/transaction_log_report.py`; methods: `_get_report_values()`
  - `TransactionTrackerConfig` (`_name = transaction.tracker.config`) — `models/tracker_config.py`; fields: `model_id:Many2one`, `model_name:Char`, `track_create:Boolean`, `track_write:Boolean`, `track_unlink:Boolean`, `track_read:Boolean`, `active:Boolean`, `company_id:Many2one`; methods: `create()`, `write()`, `unlink()`, `action_track_all()`, `action_untrack_all()`, `action_auto_populate_models()` …
  - `TransactionLog` (`_name = transaction.log`) — `models/transaction_log.py`; fields: `name:Char`, `user_id:Many2one`, `model_name:Char`, `res_id:Integer`, `record_display_name:Char`, `operation:Selection`, `module_name:Char`, `old_values:Text`, `new_values:Text`, `changed_fields:Char`, `ip_address:Char`, `company_id:Many2one`, `is_suspicious:Boolean`, `note:Text`, `record_ref:Char`; methods: `create()`, `write()`, `unlink()`, `action_open_record()`, `action_export_pdf()`, `action_export_excel()`, `get_dashboard_data()` …
  - `Base` extends `base` — `models/base_hook.py`; methods: `create()`, `write()`, `unlink()` …
- **Menu declarations:** `Transaction Tracker`, `Transaction Logs`, `Dashboard`, `Configuration`, `Tracker Settings`, `Reports`, `Transaction Report`
- **View architectures detected:** form: 2, graph: 1, kanban: 1, list: 2, pivot: 1, search: 2
- **Record rules:** `Transaction Log: Manager sees all`, `Transaction Log: User sees own`, `Tracker Config: Manager access`
- **ACL entries:** `transaction.log.manager` (group `group_transaction_tracker_manager/1/0/0`), `transaction.log.user` (group `group_transaction_tracker_user/1/0/0`), `transaction.tracker.config.manager` (group `group_transaction_tracker_manager/1/1/1`)
- **Functional file groups:** Reports: `report/transaction_log_report_template.xml`, `report/transaction_log_report.py`, `report/__init__.py`, `report/transaction_log_report.xml`; Security: `security/ir.model.access.csv`, `security/security.xml`; Data: `data/default_config.xml`; Views: `views/dashboard_views.xml`, `views/menu_views.xml`, `views/tracker_config_views.xml`, `views/transaction_log_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `vehicle_installment` — Vehicle Installment Management

- **Manifest version:** `19.0.2.0.0`  
- **Summary:** Manage vehicle installments with automatic calculation  
- **Category / license / author:** `Fleet` / `LGPL-3` / `Abdullah Al-Habbal`  
- **Dependencies:** `base`, `mail`, `fleet`, `hr`, `hr_payroll`  
- **Source inventory:** 13 files; 6 Python, 2 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `HrPayslip` extends `hr.payslip` — `models/hr_payslip.py`; methods: `action_payslip_paid()`, `action_payslip_unpaid()`, `action_payslip_cancel()`
  - `VehicleInstallment` (`_name = vehicle.installment`) extends `mail.thread` — `models/vehicle_installment.py`; fields: `vehicle_id:Many2one`, `employee_id:Many2one`, `date:Date`, `vehicle_price:Monetary`, `rate_percentage:Float`, `monthly_payment:Monetary`, `total_amount:Monetary`, `calculated_months:Float`, `full_months:Integer`, `last_payment_amount:Monetary`, `installment_lines:One2many`, `reason:Text`, `company_id:Many2one`, `state:Selection`, `currency_id:Many2one`; methods: `compute_installments()`, `button_approve()`, `button_reject()`, `button_draft()`, `get_admins()`, `write()`, `unlink()` …
  - `VehicleInstallmentLine` (`_name = vehicle.installment.line`) — `models/vehicle_installment_line.py`; fields: `installment_id:Many2one`, `vehicle_id:Many2one`, `employee_id:Many2one`, `payment_date:Date`, `amount:Monetary`, `state:Selection`, `installment_state:Selection`, `company_id:Many2one`, `currency_id:Many2one`, `note:Html`; methods: `write()`
- **Menu declarations:** `Vehicle Installments`, `Installments`, `Payment Schedule`
- **View architectures detected:** form: 1, list: 2, search: 1
- **Record rules:** `Vehicle Installment rule`, `Vehicle Installments: Only see installments of own company`, `Vehicle Installment Lines: Only see lines of own company`
- **ACL entries:** `vehicle.installment.user` (group `vehicle_installment.group_vehicle_installment_user/1/0/0`), `vehicle.installment.line.user` (group `vehicle_installment.group_vehicle_installment_user/1/0/0`), `vehicle.installment.manager` (group `vehicle_installment.group_vehicle_installment_manager/1/1/1`), `vehicle.installment.line.manager` (group `vehicle_installment.group_vehicle_installment_manager/1/1/1`)
- **Functional file groups:** Security: `security/ir.model.access.csv`, `security/security.xml`; Views: `views/vehicle_installment_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `whatsapp_mail_messaging` — Odoo Whatsapp Connector

- **Manifest version:** `19.0.1.0.0`  
- **Summary:** Odoo18 Whatsapp, Whatsapp Odoo Integration, Odoo Whatsapp Connector, 
     Odoo Whatsapp, Whatsapp Connector, Whatsapp Integration, Odoo18, Whatsapp,
     Odoo Apps  
- **Category / license / author:** `Extra Tools` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `sale`, `account`, `website`, `sale_management`  
- **Source inventory:** 139 files; 14 Python, 11 XML, 4 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `PortalShare` extends `portal.share` — `wizard/portal_share.py`; fields: `share_type:Selection`, `mobile_number:Char`, `partner_id:Many2one`; methods: `action_send_whatsapp()` …
  - `WhatsappSendMessage` (`_name = whatsapp.send.message`) — `wizard/whatsapp_send_message.py`; fields: `partner_id:Many2one`, `mobile:Char`, `message:Text`, `image_1920:Binary`; methods: `send_message()` …
  - `Website` extends `website` — `model/website.py`; fields: `mobile_number:Char`
  - `AccountMove` extends `account.move` — `model/account_move.py`; methods: `action_send_whatsapp()`, `check_customers()`, `action_whatsapp_multi()`
  - `ResCompany` extends `res.company` — `model/res_company.py`; fields: `whatsapp_message:Text`
  - `ResConfigSettings` extends `res.config.settings` — `model/res_config_settings.py`; fields: `whatsapp_message:Text`
  - `SaleOrder` extends `sale.order` — `model/sale_order.py`; methods: `action_send_whatsapp()`, `check_customers()`, `action_whatsapp_multi()`
  - `SelectionMessage` (`_name = selection.message`) — `model/selection_message.py`; fields: `name:Char`, `message:Text`
  - `SendMessage` — `controllers/whatsapp_mail_messaging.py`; methods: `whatsapp_message()`, `mobile_number()`
- **HTTP routes:**
  - `/whatsapp_message` → `whatsapp_message()` in `controllers/whatsapp_mail_messaging.py`
  - `/mobile_number` → `mobile_number()` in `controllers/whatsapp_mail_messaging.py`
- **Menu declarations:** `Whatsapp Messages`
- **View architectures detected:** form: 2, list: 1, xpath: 8
- **ACL entries:** `access.whatsapp.send.message.user` (group `base.group_user/1/1/1`), `access.selection.message.user` (group `base.group_user/1/1/1`)
- **Functional file groups:** Wizards: `wizard/portal_share_views.xml`, `wizard/portal_share.py`, `wizard/whatsapp_send_message.py`, `wizard/__init__.py`, `wizard/whatsapp_send_message_views.xml`; Controllers: `controllers/__init__.py`, `controllers/whatsapp_mail_messaging.py`; Security: `security/ir.model.access.csv`; Views: `views/sale_order_views.xml`, `views/website_templates.xml`, `views/selection_message_views.xml`, `views/res_company_views.xml`, `views/res_config_settings_views.xml`, `views/website_views.xml`, `views/account_move_views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `wm_purchase_global_discount` — Purchase Order Global Discount (Same as Odoo Sales Discount)

- **Manifest version:** `1.0.0`  
- **Summary:** Purchase Order Global Discount (Same as Odoo Sales Discount)  
- **Category / license / author:** `Purchase` / `OPL-1` / `Ibrahim Elmasry`  
- **Dependencies:** `purchase`  
- **Source inventory:** 21 files; 7 Python, 2 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `SaleOrderDiscount` (`_name = purchase.order.discount`) — `wizard/purchase_order_discount.py`; fields: `purchase_order_id:Many2one`, `company_id:Many2one`, `currency_id:Many2one`, `discount_amount:Monetary`, `discount_percentage:Float`, `discount_type:Selection`; methods: `check_discount_amount()`, `prepare_discount_product_values()`, `prepare_discount_line_values()`, `create_discount_lines()`, `action_discount_apply()`
  - `PurchaseOrder` extends `purchase.order` — `models/purchase_order.py`; methods: `action_open_discount_wizard()`
  - `Company` extends `res.company` — `models/res_company.py`; fields: `purchase_discount_product_id:Many2one`
- **View architectures detected:** form: 1, xpath: 1
- **ACL entries:** `access_purchase_order_discount` (group `purchase.group_purchase_user/1/1/1`)
- **Functional file groups:** Wizards: `wizard/purchase_order_discount_views.xml`, `wizard/__init__.py`, `wizard/purchase_order_discount.py`; Security: `security/ir.model.access.csv`; Views: `views/purchase_order_view.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `WPS` — WPS

- **Manifest version:** `1.0`  
- **Summary:** Not declared in manifest.  
- **Category / license / author:** `not declared` / `not declared` / `not declared`  
- **Dependencies:** `base`, `hr_payroll`  
- **Source inventory:** 5 files; 4 Python, 1 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `HrPayslip` extends `hr.payslip` — `models/payroll_csv_wizard.py`; methods: `action_export_sif()`
- **Functional file groups:** Views: `views/payroll_csv_wizard.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO19 / `zk_attendance_integration_v19` — TechScope | ZK Attendance Integration

- **Manifest version:** `1.0`  
- **Summary:** Integration with ZK Attendance Machines  
- **Category / license / author:** `Human Resources` / `not declared` / `not declared`  
- **Dependencies:** `base`, `hr`, `hr_attendance`  
- **Source inventory:** 11 files; 7 Python, 2 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `HrEmployee` extends `hr.employee` — `models/models.py`; fields: `zk_emp_id:Char`; methods: `_name_search()`
  - `zk_attendance_tmp` (`_name = hr.attendance.zk.temp`) — `models/models.py`; fields: `machine_id:Many2one`, `user_number:Char`, `user:Many2one`, `date:Datetime`, `local_date:Datetime`, `date_temp:Date`, `inoutmode:Char`, `logged:Boolean`, `reversed:Boolean`; methods: `sudo_create_log()`, `process_data()` …
  - `zk_attendance_machine` (`_name = hr.attendance.zk.machine`) — `models/models.py`; fields: `machine_number:Integer`, `name:Char`, `ip:Char`, `port:Integer`, `sync:Boolean`, `model:Char`, `date_sync:Datetime`, `date_sync_success:Datetime`, `manual_upload_sync_date:Datetime`, `sync_error:Text`, `last_download_log:Datetime`; methods: `get_machine_last_download()`, `update_machine_last_download()`, `do_update_machine_last_download()`, `create()`, `process()`
  - `HrAttendance` extends `hr.attendance` — `models/models.py`; fields: `no_checkout:Boolean`, `missing_check:Boolean`, `no_check_in:Boolean`, `local_check_in:Datetime`, `local_check_out:Datetime`, `hhmm_worked:Char`; methods: `_compute_hhmm_worked()`
  - `ZKAttendanceSettings` (`_name = zk.attendance.settings`) extends `res.config.settings` — `models/zk_attendance.py`; fields: `no_checkout_mode:Selection`, `deflt_time:Float`, `api_ip:Char`, `api_port:Char`; methods: `set_values()`, `get_values()`
- **Menu declarations:** `Configuration`, `ZK Attendance Machines`, `ZK Attendance Machines`, `Attendance Machines`, `Attendance Logs`
- **View architectures detected:** field: 1, form: 2, list: 2, xpath: 1
- **ACL entries:** `hr attendance zk temp` (group `/1/1/1`), `hr_attendance_zk_machine` (group `/1/1/1`)
- **Functional file groups:** Controllers: `controllers/controllers.py`, `controllers/__init__.py`; Security: `security/ir.model.access.csv`; Views: `views/views.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO20 / `el_dashboard_builder` — Dashboard Builder

- **Manifest version:** `20.0.1.0.0`  
- **Summary:** Drag-and-drop dashboard builder with customizable widgets  
- **Category / license / author:** `Tools` / `LGPL-3` / `Elmasry`  
- **Dependencies:** `base`, `web`, `mail`, `base_setup`  
- **Source inventory:** 50 files; 12 Python, 10 XML, 22 JavaScript, 1 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestDashboardBuilder` — `tests/test_dashboard_builder.py`; methods: `setUpClass()`, `test_dashboard_creation()`, `test_dashboard_duplicate()`, `test_dashboard_item_creation()`, `test_dashboard_item_position_validation()`, `test_dashboard_item_onchange_widget()`, `test_widget_creation()`, `test_widget_xml_id_unique()`, `test_dashboard_share_creation()`, `test_dashboard_share_url()`, `test_dashboard_tag()`, `test_dashboard_favorite()` …
  - `TestDashboardBuilderUI` — `tests/test_dashboard_builder.py`; methods: `setUpClass()`, `test_dashboard_view_action()`, `test_dashboard_edit_action()`, `test_widget_test_action()`, `test_dashboard_search_filters()`
  - `DashboardBuilderReport` (`_name = report.el_dashboard_builder.dashboard_report`) — `report/report.py`; methods: `generate_dashboard_pdf()`, `generate_dashboard_excel()` …
  - `DashboardExportWizard` (`_name = dashboard.builder.export.wizard`) — `report/report.py`; fields: `dashboard_id:Many2one`, `export_format:Selection`, `include_data:Boolean`; methods: `action_export()`
  - `DashboardItemConfigWizard` (`_name = dashboard.builder.item.config.wizard`) — `wizard/item_config_wizard.py`; fields: `item_id:Many2one`, `widget_id:Many2one`, `config_schema:Json`, `config:Json`, `config_fields:Json`; methods: `default_get()`, `action_save()`, `action_reset()` …
  - `DashboardBuilderController` — `controllers/controllers.py`; methods: `dashboard_view()`, `dashboard_edit()`, `dashboard_shared()`, `widget_test()`, `dashboard_export_json()`, `dashboard_export_pdf()`, `dashboard_export_excel()`, `get_item_data()`, `get_widget_preview_data()`, `configure_item()`, `update_item()`, `duplicate_item()` …
  - `Dashboard` (`_name = dashboard.builder`) extends `mail.thread`, `mail.activity.mixin` — `models/dashboard.py`; fields: `name:Char`, `description:Html`, `sequence:Integer`, `active:Boolean`, `company_id:Many2one`, `user_id:Many2one`, `is_public:Boolean`, `group_ids:Many2many`, `layout_config:Json`, `item_ids:One2many`, `item_count:Integer`, `last_viewed:Datetime`, `view_count:Integer`, `background_color:Char`, `background_image:Binary`, `custom_css:Text`, `refresh_interval:Integer`, `filter_domain:Char` …; methods: `action_open_dashboard()`, `action_edit_dashboard()`, `action_duplicate()`, `action_toggle_favorite()`, `action_export_config()`, `import_dashboard_config()` …
  - `DashboardTag` (`_name = dashboard.builder.tag`) — `models/dashboard.py`; fields: `name:Char`, `sequence:Integer`, `color:Integer`, `dashboard_count:Integer`; methods: `_compute_dashboard_count()`
  - `DashboardWidget` (`_name = dashboard.builder.widget`) — `models/dashboard.py`; fields: `name:Char`, `xml_id:Char`, `description:Html`, `sequence:Integer`, `category:Selection`, `icon:Char`, `color:Char`, `component_name:Char`, `default_width:Integer`, `default_height:Integer`, `min_width:Integer`, `min_height:Integer`, `max_width:Integer`, `max_height:Integer`, `config_schema:Json`, `default_config:Json`, `supports_filters:Boolean`, `supports_drill_down:Boolean` …; methods: `get_widget_categories()`, `action_test_widget()`
  - `DashboardItem` (`_name = dashboard.builder.item`) — `models/dashboard.py`; fields: `dashboard_id:Many2one`, `widget_id:Many2one`, `custom_widget_name:Char`, `sequence:Integer`, `pos_x:Integer`, `pos_y:Integer`, `width:Integer`, `height:Integer`, `min_width:Integer`, `min_height:Integer`, `is_locked:Boolean`, `is_visible:Boolean`, `config:Json`, `filters:Json`, `context:Json`, `drill_down_action:Char`, `refresh_interval:Integer`, `last_refreshed:Datetime` …; methods: `write()`, `action_configure()`, `action_remove()`, `action_duplicate()` …
  - `DashboardShare` (`_name = dashboard.builder.share`) — `models/dashboard.py`; fields: `dashboard_id:Many2one`, `name:Char`, `share_type:Selection`, `access_token:Char`, `password:Char`, `user_ids:Many2many`, `group_ids:Many2many`, `expiry_date:Date`, `is_active:Boolean`, `allow_export:Boolean`, `view_count:Integer`, `last_accessed:Datetime`, `embed_width:Integer`, `embed_height:Integer`; methods: `create()`, `action_regenerate_token()`, `get_share_url()`, `get_embed_code()`
- **HTTP routes:**
  - `/dashboard/builder/<int:dashboard_id>` → `dashboard_view()` in `controllers/controllers.py`
  - `/dashboard/builder/<int:dashboard_id>/edit` → `dashboard_edit()` in `controllers/controllers.py`
  - `/dashboard/builder/shared/<string:token>` → `dashboard_shared()` in `controllers/controllers.py`
  - `/dashboard/builder/widget/test/<int:widget_id>` → `widget_test()` in `controllers/controllers.py`
  - `/dashboard/builder/export/<int:dashboard_id>` → `dashboard_export_json()` in `controllers/controllers.py`
  - `/dashboard/builder/export/pdf/<int:dashboard_id>` → `dashboard_export_pdf()` in `controllers/controllers.py`
  - `/dashboard/builder/export/excel/<int:dashboard_id>` → `dashboard_export_excel()` in `controllers/controllers.py`
  - `/dashboard/builder/api/items/<int:item_id>/data` → `get_item_data()` in `controllers/controllers.py`
  - `/dashboard/builder/api/widgets/<int:widget_id>/data` → `get_widget_preview_data()` in `controllers/controllers.py`
  - `/dashboard/builder/api/items/<int:item_id>/configure` → `configure_item()` in `controllers/controllers.py`
  - `/dashboard/builder/api/items/<int:item_id>/update` → `update_item()` in `controllers/controllers.py`
  - `/dashboard/builder/api/items/<int:item_id>/duplicate` → `duplicate_item()` in `controllers/controllers.py`
  - `/dashboard/builder/api/items/<int:item_id>/delete` → `delete_item()` in `controllers/controllers.py`
  - `/dashboard/builder/api/items/create` → `create_item()` in `controllers/controllers.py`
  - `/dashboard/builder/api/items/reorder` → `reorder_items()` in `controllers/controllers.py`
  - `/dashboard/builder/api/dashboard/<int:dashboard_id>/layout` → `save_layout()` in `controllers/controllers.py`
  - `/dashboard/builder/api/dashboard/<int:dashboard_id>/duplicate` → `duplicate_dashboard()` in `controllers/controllers.py`
  - `/dashboard/builder/api/dashboard/<int:dashboard_id>/delete` → `delete_dashboard()` in `controllers/controllers.py`
- **Menu declarations:** `Dashboard Builder`, `My Dashboards`, `New Dashboard`, `Favorites`, `All Dashboards`, `Widget Library`, `Shared Dashboards`, `Configuration`, `Tags`
- **View architectures detected:** form: 5, kanban: 1, list: 4, search: 2
- **ACL entries:** `dashboard.builder.user` (group `base.group_user/1/1/1`), `dashboard.builder.manager` (group `dashboard_builder.group_dashboard_manager/1/1/1`), `dashboard.builder.item.user` (group `base.group_user/1/1/1`), `dashboard.builder.item.manager` (group `dashboard_builder.group_dashboard_manager/1/1/1`), `dashboard.builder.widget.user` (group `base.group_user/1/0/0`), `dashboard.builder.widget.manager` (group `dashboard_builder.group_dashboard_manager/1/1/1`), `dashboard.builder.share.user` (group `base.group_user/1/1/1`), `dashboard.builder.share.manager` (group `dashboard_builder.group_dashboard_manager/1/1/1`), `dashboard.builder.tag.user` (group `base.group_user/1/0/0`), `dashboard.builder.tag.manager` (group `dashboard_builder.group_dashboard_manager/1/1/1`)
- **Functional file groups:** Wizards: `wizard/item_config_wizard_views.xml`, `wizard/__init__.py`, `wizard/item_config_wizard.py`; Reports: `report/report.py`, `report/dashboard_report_templates.xml`, `report/__init__.py`; Controllers: `controllers/controllers.py`, `controllers/__init__.py`; Security: `security/ir.model.access.csv`, `security/dashboard_security.xml`; Data: `data/ir_sequence_data.xml`, `data/dashboard_demo.xml`, `data/dashboard_default_widgets.xml`; Views: `views/dashboard_views.xml`, `views/dashboard_menu.xml`, `views/dashboard_templates.xml`
- **Tests present:** `tests/test_dashboard_builder.py`, `tests/__init__.py`
- **Implemented development-batch changes:** Batch 01: sanitized controller/widget/preview error responses; earlier XML template parse defects were repaired. Runtime tests remain pending.

### ODOO20 / `el_hr_attendance_sheet` — HR Attendance Sheet And Policies

- **Manifest version:** `20.0.1.0.1`  
- **Summary:** Calculate overtime, lateness, absence from attendance and feed payslip  
- **Category / license / author:** `Human Resources/Attendance` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `hr_attendance`, `hr`, `hr_payroll`, `hr_holidays`, `mail`, `calendar`  
- **Source inventory:** 62 files; 22 Python, 18 XML, 0 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestHrAttendanceSheet` — `tests/test_hr_attendance_sheet.py`; methods: `setUpClass()`, `test_01_overtime_rule_creation()`, `test_02_lateness_step_lookup()`, `test_03_absence_step_lookup()`, `test_04_policy_get_overtime_rule()`, `test_05_sheet_sequence()`, `test_06_state_machine_transitions()`, `test_07_public_holiday_state_machine()`, `test_08_overtime_calculation()`, `test_09_lateness_tier_lookup_by_occurrence()`, `test_10_absence_tier_escalation()`, `test_11_absence_fixed_days_penalty()` …
  - `HrAttendanceSheetReport` (`_name = report.el_hr_attendance_sheet.report_hr_attendance_sheet`) — `report/hr_attendance_sheet_report.py`; methods: `_get_report_values()`
  - `HrAttendanceChangeDataWizard` (`_name = hr.attendance.change.data.wizard`) — `wizard/hr_attendance_change_data_wizard.py`; fields: `sheet_line_id:Many2one`, `new_overtime_hours:Float`, `new_late_in_minutes:Float`, `new_difference_hours:Float`, `reason:Text`; methods: `action_apply()`
  - `HrAttendanceSheetBatchWizard` (`_name = hr.attendance.sheet.batch.wizard`) — `wizard/hr_attendance_sheet_batch_wizard.py`; fields: `department_id:Many2one`, `date_from:Date`, `date_to:Date`, `employee_ids:Many2many`, `company_id:Many2one`; methods: `action_create_batch()` …
  - `HrAttendanceCreatePayslipWizard` (`_name = hr.attendance.create.payslip.wizard`) — `wizard/hr_attendance_create_payslip_wizard.py`; fields: `sheet_id:Many2one`, `employee_id:Many2one`, `date_from:Date`, `date_to:Date`, `struct_id:Many2one`, `contract_id:Many2one`; methods: `action_create_payslip()`
  - `HrAttendancePublicHoliday` (`_name = hr.attendance.public.holiday`) extends `mail.thread`, `mail.activity.mixin` — `models/hr_attendance_public_holiday.py`; fields: `name:Char`, `date_from:Date`, `date_to:Date`, `active:Boolean`, `state:Selection`, `line_ids:One2many`, `company_id:Many2one`; methods: `action_activate()`, `action_cancel()`, `action_draft()`, `is_employee_on_holiday()` …
  - `HrAttendancePublicHolidayLine` (`_name = hr.attendance.public.holiday.line`) — `models/hr_attendance_public_holiday.py`; fields: `holiday_id:Many2one`, `employee_id:Many2one`, `department_id:Many2one`, `employee_tag_ids:Many2many`, `company_id:Many2one`; methods: `matches_employee()`
  - `HrPayrollStructure` extends `hr.payroll.structure` — `models/hr_payroll_structure.py`; methods: `create()`, `action_clean_inherited_rules()`, `action_remove_duplicated_attendance_rules()`, `action_propagate_attendance_rules()` …
  - `HrAttendancePolicy` (`_name = hr.attendance.policy`) extends `mail.thread` — `models/hr_attendance_policy.py`; fields: `name:Char`, `active:Boolean`, `company_id:Many2one`, `overtime_working_id:Many2one`, `overtime_weekend_id:Many2one`, `overtime_holiday_id:Many2one`, `lateness_id:Many2one`, `absence_id:Many2one`, `contract_ids:One2many`; methods: `get_overtime_rule()`
  - `HrAttendanceSheet` (`_name = hr.attendance.sheet`) extends `mail.thread`, `mail.activity.mixin` — `models/hr_attendance_sheet.py`; fields: `name:Char`, `employee_id:Many2one`, `date_from:Date`, `date_to:Date`, `contract_id:Many2one`, `policy_id:Many2one`, `state:Selection`, `company_id:Many2one`, `currency_id:Many2one`, `line_ids:One2many`, `total_overtime:Float`, `total_late_in:Float`, `total_absence:Float`, `total_late_penalty_hours:Float`, `total_absence_penalty_days:Float`, `total_difference:Float`, `total_planned:Float`, `total_worked:Float` …; methods: `create()`, `action_compute()`, `action_approve()`, `action_done()`, `action_cancel()`, `action_draft()`, `action_create_payslip()`, `action_print_report()`, `action_open_payslip()` …
  - `HrAttendanceSheetLine` (`_name = hr.attendance.sheet.line`) — `models/hr_attendance_sheet.py`; fields: `sheet_id:Many2one`, `date:Date`, `day_type:Selection`, `planned_hours:Float`, `worked_hours:Float`, `overtime_hours:Float`, `late_in_minutes:Float`, `is_absent:Boolean`, `is_leave:Boolean`, `leave_id:Many2one`, `difference_hours:Float`, `absence_occurrence:Integer`, `late_occurrence:Integer`, `late_penalty:Float`, `absence_penalty_days:Float`, `note:Text`, `attendance_ids:Many2many`, `changed_manually:Boolean`; methods: `action_open_change_wizard()` …
  - `HrPayslip` extends `hr.payslip` — `models/hr_payslip.py`; fields: `attendance_sheet_id:Many2one`, `no_attendance_sheet:Boolean`, `overtime_hours:Float`, `late_in_hours:Float`, `absence_days:Float`, `difference_hours:Float`, `late_penalty_hours:Float`, `absence_penalty_days:Float`, `number_late_occurrences:Integer`, `number_absence_occurrences:Integer`; methods: `action_link_attendance_sheet()`, `action_open_attendance_sheet()`, `create()` …
  - `HrContract` extends `hr.version` — `models/hr_contract.py`; fields: `attendance_policy_id:Many2one`
  - `HrEmployee` extends `hr.employee` — `models/hr_contract.py`; fields: `attendance_policy_id:Many2one`
  - `HrAttendanceSheetBatch` (`_name = hr.attendance.sheet.batch`) extends `mail.thread` — `models/hr_attendance_sheet_batch.py`; fields: `name:Char`, `department_id:Many2one`, `date_from:Date`, `date_to:Date`, `state:Selection`, `company_id:Many2one`, `line_ids:One2many`; methods: `create()`, `action_generate_sheets()`, `action_confirm()`, `action_done()`, `action_cancel()`, `action_draft()` …
  - `HrAttendanceSheetBatchLine` (`_name = hr.attendance.sheet.batch.line`) — `models/hr_attendance_sheet_batch.py`; fields: `batch_id:Many2one`, `employee_id:Many2one`, `sheet_id:Many2one`, `company_id:Many2one`
  - `HrAttendanceRuleOvertime` (`_name = hr.attendance.rule.overtime`) — `models/hr_attendance_rule.py`; fields: `name:Char`, `type:Selection`, `apply_after_minutes:Float`, `rate:Float`, `active:Boolean`, `company_id:Many2one`
  - `HrAttendanceRuleLateness` (`_name = hr.attendance.rule.lateness`) — `models/hr_attendance_rule.py`; fields: `name:Char`, `active:Boolean`, `unit:Selection`, `tier_ids:One2many`, `company_id:Many2one`; methods: `get_tier()`, `get_step()`, `get_step_for_minutes()`, `get_step_for_hours()`
  - `HrAttendanceRuleLatenessTier` (`_name = hr.attendance.rule.lateness.tier`) — `models/hr_attendance_rule.py`; fields: `name:Char`, `lateness_id:Many2one`, `sequence:Integer`, `occurrence_from:Integer`, `occurrence_to:Integer`, `step_ids:One2many`, `step_count:Integer`, `unit:Selection`, `company_id:Many2one`; methods: `get_step_for_minutes()`, `get_step_for_hours()`, `action_open_rule()`, `action_open_tier()` …
  - `HrAttendanceRuleLatenessStep` (`_name = hr.attendance.rule.lateness.step`) — `models/hr_attendance_rule.py`; fields: `tier_id:Many2one`, `from_minutes:Float`, `to_minutes:Float`, `from_hours:Float`, `to_hours:Float`, `penalty_type:Selection`, `rate:Float`, `penalty_hours:Float`, `initial_rate:Float`, `amount:Float`, `lateness_id:Many2one`, `company_id:Many2one`; methods: `_compute_hour_range()`, `_inverse_hour_range()`, `_check_ranges()`
  - `HrAttendanceRuleAbsence` (`_name = hr.attendance.rule.absence`) — `models/hr_attendance_rule.py`; fields: `name:Char`, `active:Boolean`, `tier_ids:One2many`, `company_id:Many2one`; methods: `get_tier()`, `get_step_for_days()`
  - `HrAttendanceRuleAbsenceTier` (`_name = hr.attendance.rule.absence.tier`) — `models/hr_attendance_rule.py`; fields: `name:Char`, `absence_id:Many2one`, `sequence:Integer`, `occurrence_from:Integer`, `occurrence_to:Integer`, `step_ids:One2many`, `step_count:Integer`, `company_id:Many2one`; methods: `get_step_for_days()`, `action_open_rule()`, `action_open_tier()` …
  - `HrAttendanceRuleAbsenceStep` (`_name = hr.attendance.rule.absence.step`) — `models/hr_attendance_rule.py`; fields: `tier_id:Many2one`, `from_days:Integer`, `to_days:Integer`, `penalty_type:Selection`, `rate:Float`, `deduction_days:Float`, `absence_id:Many2one`, `company_id:Many2one`; methods: `compute_deduction_days()` …
- **Menu declarations:** `Attendance Sheets`, `Attendance Sheets`, `Batches`, `Configuration`, `Public Holidays`, `Rules`, `Overtime Rules`, `Lateness Rules`, `Absence Rules`, `Attendance Policies`
- **View architectures detected:** form: 12, graph: 1, kanban: 1, list: 9, pivot: 1, search: 7, xpath: 3
- **Functional file groups:** Wizards: `wizard/hr_attendance_sheet_batch_wizard_views.xml`, `wizard/__init__.py`, `wizard/hr_attendance_change_data_wizard_views.xml`, `wizard/hr_attendance_change_data_wizard.py`, `wizard/hr_attendance_sheet_batch_wizard.py`, `wizard/hr_attendance_create_payslip_wizard_views.xml`, `wizard/hr_attendance_create_payslip_wizard.py`; Reports: `report/hr_attendance_sheet_report.xml`, `report/hr_attendance_sheet_report.py`, `report/hr_attendance_sheet_report_templates.xml`, `report/__init__.py`; Security: `security/ir.access.csv`, `security/hr_attendance_sheet_groups.xml`; Data: `data/hr_payroll_structure_data.xml`, `data/ir_sequence_data.xml`, `data/hr_structure_attendance_rules_action.xml`, `data/hr_salary_rule_data.xml`; Views: `views/hr_attendance_policy_views.xml`, `views/hr_attendance_sheet_batch_views.xml`, `views/hr_attendance_public_holiday_views.xml`, `views/hr_attendance_rule_views.xml`, `views/hr_payslip_views.xml`, `views/hr_contract_views.xml`, `views/hr_attendance_sheet_views.xml`, `views/hr_attendance_sheet_menus.xml`
- **Tests present:** `tests/__init__.py`, `tests/test_hr_attendance_sheet.py`

### ODOO20 / `el_inter_company_transfer` — Inter Company Internal Transfer

- **Manifest version:** `20.0.1.0.1`  
- **Summary:** Request stock transfers between warehouses of different companies  
- **Category / license / author:** `Inventory/Warehouse Management` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `base`, `stock`, `mail`, `portal`  
- **Source inventory:** 11 files; 6 Python, 3 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `InterCompanyTransferRequestLine` (`_name = inter.company.transfer.request.line`) — `models/transfer_request_line.py`; fields: `request_id:Many2one`, `sequence:Integer`, `product_id:Many2one`, `product_uom_id:Many2one`, `product_qty:Float`, `available_qty:Float`, `company_id:Many2one`; methods: `_onchange_product_id()`, `_compute_available_qty()`, `_check_quantity()`
  - `StockWarehouse` extends `stock.warehouse` — `models/stock_warehouse.py`; methods: `name_search()`
  - `InterCompanyTransferRequest` (`_name = inter.company.transfer.request`) extends `mail.thread`, `mail.activity.mixin` — `models/transfer_request.py`; fields: `name:Char`, `state:Selection`, `company_id:Many2one`, `source_warehouse_id:Many2one`, `dest_company_id:Many2one`, `dest_warehouse_id:Many2one`, `line_ids:One2many`, `user_id:Many2one`, `confirmed_by:Many2one`, `confirmed_date:Datetime`, `picking_id:Many2one`, `incoming_picking_id:Many2one`, `note:Text`, `is_draft:Boolean`, `can_confirm:Boolean`; methods: `create()`, `action_confirm()`, `action_done()`, `action_cancel()`, `action_reset_to_draft()`, `action_view_picking()`, `action_view_incoming_picking()` …
- **Menu declarations:** `Inter Company Transfers`, `Transfer Requests`
- **View architectures detected:** form: 1, kanban: 1, list: 1, search: 1
- **Functional file groups:** Security: `security/ir.access.csv`; Data: `data/ir_sequence_data.xml`; Views: `views/transfer_request_views.xml`, `views/transfer_request_menus.xml`
- **Tests present:** No test files detected in the addon archive.

### ODOO20 / `el_pos_customer_payment_method` — POS Customer Payment Method

- **Manifest version:** `20.0.1.0.0`  
- **Summary:** Restrict POS payment methods per customer, with POS-level defaults for customers without a specific list.  
- **Category / license / author:** `Sales/Point of Sale` / `LGPL-3` / `Ibrahim Elmasry`  
- **Dependencies:** `point_of_sale`  
- **Source inventory:** 13 files; 8 Python, 2 XML, 1 JavaScript, 0 SCSS; 2 test files.  
- **Python classes / models:**
  - `TestElPosPaymentMethodFilter` — `tests/test_payment_filter.py`; methods: `setUpClass()`, `test_01_partner_field_stored()`, `test_02_pos_data_fields_include_allowed_methods()`, `test_03_child_partner_resolves_to_commercial_partner()`, `test_04_partner_data_read_returns_method_ids()`, `test_05_pos_config_defaults_field_loaded()`, `test_06_settings_related_field_roundtrip()`
  - `ResPartner` extends `res.partner` — `models/res_partner.py`; fields: `el_allowed_pos_payment_method_ids:Many2many`; methods: `_load_pos_data_fields()`
  - `ResConfigSettings` extends `res.config.settings` — `models/res_config_settings.py`; fields: `pos_el_default_payment_method_ids:Many2many`
  - `PosConfig` extends `pos.config` — `models/pos_config.py`; fields: `el_pos_default_payment_method_ids:Many2many`
- **View architectures detected:** xpath: 2
- **Functional file groups:** Views: `views/res_partner_views.xml`, `views/res_config_settings_views.xml`
- **Tests present:** `tests/__init__.py`, `tests/test_payment_filter.py`

### ODOO20 / `meno` — meno

- **Manifest version:** `1.1`  
- **Summary:** Crack odoo v20  
- **Category / license / author:** `not declared` / `not declared` / `meno`  
- **Dependencies:** `base`, `base_setup`  
- **Source inventory:** 10 files; 6 Python, 3 XML, 0 JavaScript, 0 SCSS; 0 test files.  
- **Python classes / models:**
  - `ir_module_module` extends `ir.module.module` — `models/models.py`; methods: `crack()`, `cracks()`, `button_immediate_upgrade()`
  - `IrConfigParameter` extends `ir.config_parameter` — `models/models.py`; methods: `cracks()`
- **ACL entries:** `crack.crack` (group `/1/0/0`)
- **Functional file groups:** Controllers: `controllers/controllers.py`, `controllers/__init__.py`; Security: `security/ir.model.access.csv`; Data: `data/cracks_test.xml`; Views: `views/views.xml`, `views/templates.xml`
- **Tests present:** No test files detected in the addon archive.

## Cross-Module Review Notes
### High-priority items not considered fixed
- `odoo19/advanced_accounting_reports`: review the destructive `pre_init_hook` on a cloned database before install/upgrade; it may affect views/constraints beyond the addon.
- `odoo18/odoo_multi_channel_sale`: public webhook routes require a unified signature/secret authentication design and tests before production use.
- `odoo19/el_button_access_control` and `odoo18/pos_refund_restriction`: UI visibility/client-side restrictions are not equivalent to server-side authorization; verify RPC/backend bypass paths.
- `odoo17/meno`, `odoo18/meno`, `odoo19/meno`, `odoo20/meno`: repository notes describe subscription-expiry bypass behavior. Do not deploy or redistribute; replace with a legitimate licensing path.
- Missing dependencies remain: `nmo_sale_order_approval_workflow`, `nmo_stock_user_restriction`, `odoo_shipping_service_apps`. The `el_nmo_sale_payment_gateway` dependency is now present in this repository.

### Validation status
The delivered batch report records successful static checks for Python AST parsing (1,140 files), XML parsing (706 files), manifest parsing (112 manifests), JavaScript syntax (89 files), and patch dry-run (15 changed files). No Odoo runtime installation, database migration, multi-company functional test, external-provider integration test, or browser end-to-end test is claimed.
