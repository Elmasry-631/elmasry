# User Acceptance Preview — ie_stock_movement_report

## Module Summary

- **Name:** ie_stock_movement_report
- **Version:** 19.0.1.0.0
- **Models:** 3 (stock.movement.report abstract, .wizard transient, .handler abstract)
- **Views:** 1 wizard form
- **Reports:** 1 QWeb PDF (A4 Landscape, one product per page)
- **Tests:** 18 test methods (14 wizard/logic + 4 permissions)
- **Docs:** 13 files in docs/ + README with 3 Mermaid diagrams
- **i18n:** 44 Arabic translations

## User Flow Walkthrough

### User Journey: Inventory Controller

1. **Login** → navigates to **Inventory → Reporting → Stock Movement Report**
2. **Wizard opens** → sees 6 fields:
   - From Date (required)
   - To Date (required)
   - Warehouse (optional)
   - Location (optional)
   - Product (optional)
   - Product Category (optional)
3. **Fill dates** → e.g., 2026-01-01 to 2026-01-31
4. **Optional filters** → e.g., select Warehouse "WH/Stock"
5. **Click "Print PDF"** → browser downloads PDF
6. **PDF opens** → first page shows:
   - Company logo + name (header)
   - Report title "Stock Movement Report"
   - Period: 2026-01-01 to 2026-01-31
   - Warehouse: WH/Stock
   - Page 1 of N
7. **First product section** →
   - Product name + internal ref + category + UoM
   - Opening Balance table (Qty, Unit Cost, Total Value)
   - Transaction Details table (17 columns: Date, Ref, Partner, Src, Dst,
     IN×4, OUT×4, BALANCE×4)
   - Product Summary table (Opening, Total In, Total Out, Closing, Value)
8. **Each subsequent product** → starts on a new page (page-break-before)
9. **Last page** → footer with page number

### Key Screens

#### Screen 1: Wizard Form
- Two groups: "Period" (date_from, date_to) + "Filters (optional)"
  (warehouse, location, product, categ)
- Footer: "Print PDF" (primary, fa-print icon) + "Cancel" (secondary,
  fa-times icon)

#### Screen 2: PDF Report (per product page)
- Header: company branding + period + filters + page number
- Product info bar (light gray background)
- Opening Balance (3-column table)
- Transaction Details (17-column table with grouped headers)
- Product Summary (5-column table)

### Limitations + Known Issues

- **Cost source:** Uses `product.standard_price` (Community Edition).
  For FIFO/LIFO, add Enterprise dependency.
- **Opening balance without scope:** When no warehouse/location filter is
  set, opening balance is 0 (conservative). For accurate whole-company
  opening balance, use `stock.quant` snapshot logic (future enhancement).
- **No QWeb rendering test:** QWeb template rendering requires Odoo runtime
  + wkhtmltopdf. Manual UAT covers this.

### Configuration Needed After Install

1. **Inventory → Reporting → Stock Movement Report** — menu auto-created
2. **Settings → Users** → assign Stock Movement Report groups:
   - User group: can run report
   - Manager group: can run + delete stuck wizards
3. **Verify product costs** are set (`standard_price` field) — required
   for accurate valuation columns

---

## User Acceptance — Awaiting Confirmation

**Do you accept this module for packaging?**

Reply with:
- "OK" / "Accept" / "Package it" → proceed to STEP 9 (Package)
- Specific changes → I will revise and re-show
- "Cancel" → stop BUILD MODE
