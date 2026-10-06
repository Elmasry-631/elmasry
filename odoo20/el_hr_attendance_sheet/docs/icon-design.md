# Icon Design — el_hr_attendance_sheet

> Version: 20.0.1.0.0 | Generated: 2026-06-23

## Icon Brief
- **Module Name:** el_hr_attendance_sheet
- **Module Purpose:** HR Attendance Sheet And Policies — calculate overtime, lateness, absence and link to payslip
- **Key Models:** hr.attendance.sheet, hr.attendance.policy, hr.attendance.rule.overtime
- **Key Features:** overtime calc, lateness penalty matrix, absence detection, payslip integration
- **Odoo Category:** Human Resources / Attendance
- **Primary Color:** Teal #009688 (mapped from HR category)
- **Brand Initial:** E

## Icon Description
A minimalist teal clock face with a white check-mark overlay, set against a faint spreadsheet grid in the background. The clock represents attendance/time tracking; the check-mark represents approval/validation; the grid represents the sheet layout. The teal color (#009688) is the standard Odoo HR category color.

## Design Rationale
- **Clock** = time tracking (attendance, overtime, late-in) — the core data source
- **Check-mark** = approval workflow (sheet → approved → done)
- **Grid** = the sheet itself (per-day breakdown)
- **Teal** = HR category color, ensures visual consistency with other HR modules in the Apps list
- The icon is readable at 64×64 thumbnail size because it uses bold, high-contrast shapes (clock outline + check-mark)

## Generation Method
- Tool: image-generation skill (AI)
- Prompt: "Modern Odoo module app icon, 256x256 pixels, centered composition, flat design with subtle shadow and rounded corners. Theme: HR attendance sheet with overtime calculation. Visual elements: minimalist clock with check-mark overlay on a small spreadsheet grid in background. Color palette: primary teal #009688, with white background (#FFFFFF) and subtle drop shadow. Typography: NO text inside the icon. Style: clean, modern, suitable for a business software application icon. Mood: professional, trustworthy, recognizable at 64x64 thumbnail size."
- Original size: 1024x1024 → resized to 256x256 via Pillow LANCZOS
- Dimensions: 256x256 PNG
- File size: 46.1 KB

## Color Palette
| Role | Color | Hex |
|------|-------|-----|
| Primary | Teal | #009688 |
| Background | White | #FFFFFF |
| Accent | Dark teal | #00796B |
| Check-mark | White | #FFFFFF |

---
*Author: Ibrahim Elmasry*
