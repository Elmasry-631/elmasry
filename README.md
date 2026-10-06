# Odoo Addons by Elmasry

Custom and third-party Odoo addons, one folder per Odoo version. Every folder under `odoo17/` … `odoo20/` is a self-contained addon with its own `__manifest__.py` — add the version folder to your `addons_path` and install the module from the Apps screen.

| | |
|---|---|
| Addons | **109** |
| Odoo 17 | 4 |
| Odoo 18 | 46 |
| Odoo 19 | 56 |
| Odoo 20 | 3 |

## Contents

- [Odoo 17](#odoo-17) — 4 addons
- [Odoo 18](#odoo-18) — 46 addons
- [Odoo 19](#odoo-19) — 56 addons
- [Odoo 20](#odoo-20) — 3 addons

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

> **Note** — Depends on `el_nmo_sale_payment_gateway`, a module not present in this repository.

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

**Depends on** `base`, `mail`, `hr`, `stock`, `account`, `sale_management`, `web`

### E-Commerce & Connectors

#### `connector_foodics` — Foodics Connector

> version `19.0.1.0.0` · license `LGPL-3` · author: Woledge · category: Sales/Point of Sale · tests

Bidirectional synchronization bridge between Odoo and Foodics POS.

- Bidirectional sync with the Foodics POS API v2
- Products, categories, customers, orders, inventory, taxes
- Webhooks, mapping, monitoring and retries
- Unit tests

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

These addons declare a dependency that is **not present** in this repository, in the Odoo Community addons or in the Enterprise tree — they will not install until the missing addon is supplied.

| Missing addon | Required by |
|---|---|
| `el_nmo_sale_payment_gateway` | `odoo19/el_nmo_classification` |
| `nmo_sale_order_approval_workflow` | `odoo19/el_prevent_negative_stock` |
| `nmo_stock_user_restriction` | `odoo19/el_prevent_negative_stock` |
| `odoo_shipping_service_apps` | `odoo19/smsa_express_delivery_carrier` |

## Conventions

**Layout** — `<version>/<addon>/`, addon folder name equals the Python module name.

**Manifest** — `name`, `summary`, `version` (`<odoo>.0.x.y.z`), `license`, `author`, `depends`, `data`.

**Tests** — `tests/test_*.py` using `odoo.tests.common.TransactionCase`; enable with `--test-enable`.

**Commits** — `[ADD]` for a new addon, `[UPD]` for changes to an existing one.

