# User Acceptance Preview — el_restrict_journal v2.0.0 (Whitelist)

## Module Summary

- **Name:** el_restrict_journal
- **Version:** 19.0.2.0.0 (Whitelist mode)
- **Models extended:** 4 (res.users, account.move, account.payment, account.journal)
- **Views:** 2 inherited views (res.users form, account.move form)
- **Security:** 2 groups, 3 record rules (HIDE non-allowed), 1 access CSV
- **Tests:** 14 test methods (L2 PASS 14/14)

## What Changed from v1.0.0

**v1.0.0 (Blacklist):** Admin marks journals as "restricted" → user can't use them but sees them as read-only.

**v2.0.0 (Whitelist):** Admin marks journals as "allowed" → user can ONLY see and use those journals. All other journals are **completely hidden**.

## User Journey: Chief Accountant (Manager)

1. **Login** as chief accountant (must be in `group_restrict_journal_manager`)
2. **Open Settings → Users** → select the accountant you want to restrict
3. **Click "Allowed Journals" tab** (visible only to managers)
4. **Select journals** to ALLOW — use the many2many_tags widget
5. **Save** → user is automatically added to the restriction group → only allowed journals visible

## User Journey: Restricted Accountant

1. **Login** as the restricted accountant
2. **Open Accounting → Customers → Invoices → New**
3. **In the "Journal" dropdown** — you only see your ALLOWED journals. Non-allowed journals do not appear at all.
4. **Try to create an invoice** with one of the allowed journals → succeeds normally
5. **(Edge case) If somehow a non-allowed journal is selected** (e.g., via API):
   - Warning popup: "The journal 'X' is not in your allowed list. Please select one of: Y, Z."
   - Journal field is cleared
6. **(Edge case) If user persists and tries to save** with non-allowed journal:
   - `ValidationError`: "You are not allowed to create entries in the journal 'X'. Your allowed journals are: Y, Z."
7. **Open Configuration → Journals** list:
   - You only see your allowed journals
   - Non-allowed journals are completely invisible (not even read-only)

## Key Screens

### Screen 1: User Form with "Allowed Journals" Tab

- Location: Settings → Users → (select user) → Allowed Journals tab
- Field: "Allowed Journals" (many2many_tags widget)
- Help text explains:
  - "ALLOWED" semantics (whitelist)
  - Empty = unrestricted (default Odoo)
  - Auto group membership behavior
- Visibility: Only members of `group_restrict_journal_manager`

### Screen 2: account.move Form (Restricted User's View)

- Journal dropdown shows ONLY allowed journals
- Non-allowed journals do NOT appear in the dropdown

### Screen 3: Journals List (Restricted User's View)

- Only allowed journals appear
- Non-allowed journals are completely hidden (not just read-only)

## Configuration Needed After Install

1. **Assign Manager group** to chief accountant (Settings → Users → Access Rights → "Restricted Journal: Manager")
2. **Configure allowed journals** per user (Settings → Users → Allowed Journals tab)
3. **Test the restriction** by logging in as a restricted user:
   - Open any journal-related view → only allowed journals visible
   - Try API access with non-allowed journal → ValidationError

## Removing a Restriction

To remove the restriction for a user:
1. Open the user form
2. Go to **Allowed Journals** tab
3. Click the **X** next to each journal (or use "Clear All")
4. **Save**

The user is automatically removed from the restriction group and regains full access to all journals.

## Verdict

✅ The module delivers on the user's requirement:
- "اللي انا اختارو هو اللي يكون متاح" — Only selected journals are available ✓
- "اللي مخترتوش ميظهرش لليوزر اصلا" — Non-selected journals are completely hidden ✓

Ready for user acceptance.
