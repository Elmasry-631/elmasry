# Icon Design — el_cheque_tracking

## Spec

- **Size:** 200 × 200 pixels
- **Format:** PNG, optimized
- **File size:** 2702 bytes
- **Location:** `static/description/icon.png`

## Visual design

- **Background:** Solid navy blue (#21F405F → RGB 33, 64, 95)
- **Foreground text:** "CHQ" in amber (#FFC107 → RGB 255, 193, 7)
- **Font:** DejaVu Sans Bold, 48pt (centered, slightly above middle)
- **Accent stripe:** Amber rectangle at the bottom (y=170 to y=200),
  with a 5-pixel navy separator above it (y=165 to y=170)

## Design rationale

- **Navy + amber** is a classic financial color pairing (used by many
  banking apps); it signals "money" without being garish.
- **"CHQ"** is the universal abbreviation for "cheque" and is language-neutral
  (works in both English and Arabic UIs — Arabic users see the icon as a
  visual marker, not a label).
- The bottom accent stripe adds visual weight at the bottom of the icon,
  balancing the centered text.

## Generation method

Generated with Pillow (Python Imaging Library):

```python
from PIL import Image, ImageDraw, ImageFont

img = Image.new("RGB", (200, 200), color=(33, 64, 95))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48
)
# Centered "CHQ"
bbox = draw.textbbox((0, 0), "CHQ", font=font)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]
draw.text(
    ((200 - text_w) // 2, (200 - text_h) // 2 - 10),
    "CHQ", fill=(255, 193, 7), font=font
)
# Bottom accent stripe
draw.rectangle([(0, 170), (200, 200)], fill=(255, 193, 7))
draw.rectangle([(0, 165), (200, 170)], fill=(33, 64, 95))
img.save("static/description/icon.png", "PNG", optimize=True)
```

## Regeneration

To regenerate the icon (e.g. with different colors), edit the script in
`docs/icon-design.md` and re-run with Pillow installed.
