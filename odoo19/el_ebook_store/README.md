# E-Book Store (`el_ebook_store`)

> Sell e-books on your Odoo eCommerce website with unique access codes.

## Features
1. **E-Book Products** — mark any product as an e-book with PDF file + author + ISBN
2. **Access Codes** — generate unique codes per book (random or manual entry)
3. **One Code = One Use** — each code is used once per customer
4. **Online Reader** — customers read PDFs directly in their browser
5. **Download Option** — configurable per book (online / download / both)
6. **My Library** — portal page showing purchased books + codes + read/download buttons
7. **Auto-Assign on Sale** — when sale order is confirmed, codes auto-assign to customer
8. **Access Logs** — track who opened which book and when
9. **Admin Dashboard** — code statistics, library management, access logs
10. **Email Delivery** — automatic email with access codes after purchase

## Installation
1. Copy to `addons/`
2. Restart Odoo → Update Apps List → Install

## Usage
1. Create a product → check "Is E-Book" → upload PDF
2. Click "Generate Codes" → choose random or manual
3. Customer buys the book on your website
4. Sale order confirmation → code auto-assigned → email sent
5. Customer visits "My Library" → reads or downloads

## LAW 26 Waiver
Run on real Odoo 19 before production:
```bash
odoo -d <db> -i el_ebook_store --test-enable --test-tags=/el_ebook_store --stop-after-init
```
