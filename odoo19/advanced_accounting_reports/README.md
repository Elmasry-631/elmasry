# Advanced Accounting Reports (Odoo 19)

## Overview
A comprehensive Odoo 19 module that extends the native Accounting application with advanced analytic dimensions, multi-currency support, and professional reporting capabilities.

## Features

### 1. Analytic Dimensions
- **Features** - Hierarchical analytic features with code, name, parent, company, and notes
- **Cost Centers** - Hierarchical cost centers with code, name, parent, and company
- **Patch Numbers** - Patch tracking with number, description, and status (Draft/Confirmed/Closed)

### 2. Multi-Currency Support
- **Secondary Currency** per journal entry
- **Manual Exchange Rate** with automatic secondary amount calculation
- Formula: `Secondary Amount = Base Amount × Manual Rate`
- Automatic computation on move lines (debit, credit, balance)

### 3. Advanced Reports
- **General Ledger** - With dimension filters, secondary currency, drill-down, grouping
- **Trial Balance** - Opening/Period/Ending balances with secondary currency columns

### 4. Export Formats
- **Excel (XLSX)** - Professional formatting, RTL support, formulas, company header
- **PDF (QWeb)** - Arabic fonts, RTL support, headers/footers, signatures

### 5. Full Localization
- Arabic & English translations
- RTL layout support
- Clean translation files (ar.po + en.po)

## Installation

1. Copy the module folder to your Odoo addons directory:
   ```bash
   cp -r advanced_accounting_reports /opt/odoo/addons/
   ```

2. Update the app list and install:
   - Go to **Apps** → Update Apps List
   - Search for **Advanced Accounting Reports**
   - Click **Install**

3. Assign security groups:
   - **Advanced Accounting User** - Standard users
   - **Advanced Accounting Manager** - Administrators

## Technical Architecture

### Models
- `account.feature` - Analytic features
- `account.cost.center` - Cost centers
- `account.patch.number` - Patch numbers
- Inherited `account.move` - Secondary currency & manual rate
- Inherited `account.move.line` - Dimension fields & secondary amounts

### Reports
- `report_general_ledger` - QWeb PDF
- `report_trial_balance` - QWeb PDF
- `report_general_ledger_xlsx` - Excel export
- `report_trial_balance_xlsx` - Excel export

### Wizards
- `general.ledger.wizard` - Filter & launch GL report
- `trial.balance.wizard` - Filter & launch TB report

### Security
- Record rules for multi-company isolation
- Access rights per group (User / Manager)

## Testing
Run tests with:
```bash
./odoo-bin -u advanced_accounting_reports --test-enable
```

## Upgrade Safety
- All XML data uses `noupdate="1"` where appropriate
- Models use `_check_company_auto = True`
- Inheritance-based architecture preserves native Odoo functionality

## License
LGPL-3
