# Icon Design — el_restrict_journal

## Visual Concept

A **3D padlock** over an accounting-green background, with an amber accent ring.

## Design Rationale

| Element | Choice | Reason |
|---------|--------|--------|
| **Glyph** | Lock (`fa-lock` style) | Universal symbol for "restricted access" — instantly communicates the module's purpose |
| **Background** | Accounting green (#2E7D32) | Matches Odoo's "Accounting" category color — visual consistency with the rest of the accounting apps |
| **Accent** | Amber (#F5A623) | Warm contrast against green — draws attention to the lock; commonly used in security contexts (warning amber) |
| **Glyph color** | White (#FFFFFF) | Maximum contrast against green — readability on small thumbnails |
| **Style** | 3D | Modern look; stands out in the Odoo app dashboard grid |
| **Size** | 256x256 PNG | Odoo standard icon size; renders crisp on retina displays |
| **File size** | ~31KB | Well under 100KB limit |

## Visual Symbolism

The lock + accounting green color combination reads as: **"financial records under lock and key"** — exactly what the module delivers. The amber ring suggests "warning" / "proceed with caution", which is appropriate for a security restriction module.

## Color Palette (Hex)

| Color | Hex | RGB | Use |
|-------|-----|-----|-----|
| Background | `#2E7D32` | (46, 125, 50) | Main fill |
| Accent | `#F5A623` | (245, 166, 35) | Ring / outline |
| Glyph | `#FFFFFF` | (255, 255, 255) | Lock symbol |

## Generation Method

Generated via `scripts/gen_icon.py` (built-in skill script) using:
- Pillow (PIL) for raster rendering
- 3D-style shadow + highlight via gradient overlay
- Anti-aliased glyph rendering

No external AI image generation was used — the icon is 100% deterministic and reproducible from the command above.
