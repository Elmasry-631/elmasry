# Module Icon Design — `direct_print_auto`

## Icon Brief

| Field | Value |
|-------|-------|
| Module name | `direct_print_auto` |
| Pretty name | Direct Print Auto |
| Summary | Auto-print invoices, SOs, delivery slips and POs to the browser's print dialog when confirmed, plus a manual Direct Print button on each form. |
| Odoo category | Sales / Sales |
| Primary color | Blue `#4A90E2` (Sales category color, mapped via `CATEGORY_COLOR_MAP`) |
| Accent color | Darker blue `#357ABD` (gradient end) |
| Glyph | White printer with paper emerging from top |
| Style | Flat, minimalist, geometric, no text |
| Output | `static/description/icon.png` (256×256, < 100 KB) |

## Design Rationale

The icon communicates the module's purpose at a glance:

- **Printer glyph** is the universal symbol for printing — instantly recognizable to any Odoo user browsing the app list.
- **Paper emerging from the top** of the printer suggests "output produced automatically" — reinforcing the auto-print behaviour that distinguishes this module from Odoo's standard "Print → Report" menu (which requires an explicit user click).
- **Blue gradient** matches the Odoo Sales category color (`#4A90E2`), since the module lives under the Sales settings tab and primarily targets sales-relevant documents (invoices, SOs, POs, delivery slips).
- **No text or letters** — Odoo icon guidelines recommend glyphs over text for clarity at small sizes (the icon is rendered at 64×64 in the app list and 32×32 in the favorites bar).

## Color Source

The primary blue `#4A90E2` is taken from the Odoo category color map (entry for "Sales") in the skill's `icon_generator.py` script. This ensures visual consistency with other Sales-category modules in the same Odoo instance.

## Generation Method

Icon was generated via the `z-ai-web-dev-sdk` image generation API using the following prompt:

> "Minimalist Odoo module icon, flat design, 256x256 square, blue gradient background #4A90E2 to #357ABD, white printer glyph with paper emerging from top, simple geometric shapes, no text, no letters, professional, clean, centered, app icon style"

Generated at 1024×1024, then resized to 256×256 using Pillow's LANCZOS resampling for a high-quality downscale.

## Verification

| Check | Result |
|-------|--------|
| Format: PNG | ✅ PNG |
| Dimensions: 256×256 | ✅ 256×256 |
| File size < 100 KB | ✅ 28.8 KB |
| Square aspect ratio | ✅ 1:1 |
| Readable in file browser | ✅ (verified with PIL.Image.open) |
| Matches module purpose | ✅ Printer glyph + blue gradient |
| Matches Odoo category color | ✅ Blue (Sales) |
