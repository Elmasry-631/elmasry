# Installation Guide

## Prerequisites
- Odoo 19 Community or Enterprise
- Python 3.10+
- `report_xlsx` module (for Excel exports)

## Steps

### 1. Place Module
```bash
cp -r advanced_accounting_reports /path/to/odoo/addons/
```

### 2. Restart Odoo
```bash
systemctl restart odoo
```

### 3. Update Apps List
- Activate Developer Mode
- Go to **Apps** → **Update Apps List**

### 4. Install Module
- Search: **Advanced Accounting Reports**
- Click **Install**

### 5. Configure
- Go to **Accounting → Configuration → Advanced Accounting**
- Set up Features, Cost Centers, and Patch Numbers
- Configure default secondary currency in Company settings

### 6. Assign Groups
- Go to **Settings → Users & Companies → Users**
- Assign **Advanced Accounting User** or **Advanced Accounting Manager**

## Post-Installation
- Create demo data (optional) via **Settings → Technical → Demo Data**
- Run tests: `./odoo-bin -u advanced_accounting_reports --test-enable`
