# Troubleshooting — el_payroll_wps

## Common Issues

### "No validated payslips were found for `<Month Year>`"

**Cause:** The wizard found no payslips in `validated` or `paid` state whose `date_from` falls within the chosen month. Note: Odoo 19 uses `validated` (NOT `done`).

**Fix:**
1. Go to **Payroll → Payslips**.
2. Filter by `Date From` is within `[month]`.
3. Check the `State` column — all should be `Validated` or `Paid`.
4. If any are `Draft` or `Cancelled`, select them and use **Action → Confirm**.

### The `wage` column shows 0 for every employee

**Cause:** No salary rule with code `BASIC` exists.

**Fix:** Create a rule with code `BASIC` in your salary structure.

### The `house` column shows 0 for every employee

**Cause:** No salary rule with code `HOUALLOW` exists.

**Fix:** If your company pays housing allowance: create a rule with code `HOUALLOW`. If not: column will correctly show 0 — leave it.

### The `discount` column shows 0 for every employee

**Cause:** No payslip lines are categorized under category `DED`.

**Fix:** Verify your deduction rules (insurance, tax, loans) have their `Category` set to the `DED` category.

### The `Others` column shows 0 for every employee

**Cause:** Same as `wage` + `house` + `discount` issues combined. `x_others = ALW_total − DED_total`. If both are 0, result is 0.

**Fix:** Fix the categories on your salary rules first.

### Excel shows garbled Arabic text

**Cause:** Excel opened the file with the wrong encoding.

**Fix:**
1. Close Excel.
2. Open Excel → **File → Open → Browse** → select the CSV.
3. In the Text Import Wizard: choose **Delimited**, **65001: Unicode (UTF-8)**, then Finish.

### The `WPS Export` menu doesn't appear

**Cause 1:** Not in the Payroll user group.
**Fix:** Settings → Users → select user → "Payroll" → check "Payroll: User".

**Cause 2:** `hr_work_entry_enterprise` not installed AND `post_init_hook` failed.
**Fix:** Manually edit the menu:
1. Settings → Technical → User Interface → Menu Items.
2. Search `WPS Export`.
3. Open → set `Parent Menu` to your Payroll root menu → Save.

### `x_others` resets when I save the payslip

**Expected behavior:** `x_others` only recomputes when you click **Compute Sheet**. Manual edits should persist through normal Save.

**If it's not persisting:**
1. Make sure you're not clicking **Compute Sheet** between editing and saving.
2. Check Odoo log for ORM errors on save.

### The CSV download doesn't start

**Cause:** Browser blocked the download.

**Fix:**
1. Allow pop-ups for your Odoo domain.
2. Try a different browser.
3. Check Odoo logs for errors.
