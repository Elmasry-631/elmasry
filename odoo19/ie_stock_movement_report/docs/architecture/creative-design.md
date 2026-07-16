# Creative Design — ie_stock_movement_report

## 5 Creative Lenses (applied)

### Lens 1: Pattern Discovery
- **Pattern:** Report + Wizard (Odoo standard pattern)
- **Reference:** `account_financial_report` (OCA) — similar report/wizard split
- **Variant:** AbstractModel for business logic (not coupled to TransientModel)

### Lens 2: UX Innovation
- **8 UX strategies** — applicable subset:
  1. **Smart defaults** — date_from defaults to first day of current month
  2. **Domain filtering** — location_id domain restricts to internal/transit
  3. **One-click print** — single "Print PDF" button (no multi-step)
  4. **Page-per-product** — every product starts on new page for printing

### Lens 3: Smart Automation
- **Not applicable** — this is a read-only report, no automation triggers

### Lens 4: Future-Proofing
- **4 scalability strategies:**
  1. Batch fetch — handles 10K+ move lines without OOM
  2. In-memory computation — no temp tables, no DB-side loops
  3. Prefetch via read_group/read — single SQL per data type
  4. Pluggable cost source — switch standard_price → valuation layer later

### Lens 5: Wow Factor
- **1 differentiator:**
  - **17-column transaction table** — IN/OUT/BALANCE each split into
    Qty/Unit/Unit Price/Total. This is uncommon in Odoo reports (most
    show only Qty). Allows accountants to verify valuation per move.

## Design constraints

- No JavaScript (pure server-side QWeb) — works in any Odoo instance
- No external dependencies (no Chart.js, no CDN) — fully self-contained
- No Enterprise features — works on Community Edition
