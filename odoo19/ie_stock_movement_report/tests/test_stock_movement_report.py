"""Tests for Stock Movement Report.

Covers:
    1. Wizard creation with required dates
    2. Wizard date validation (date_from > date_to raises UserError)
    3. Optional fields default falsy
    4. action_print_pdf returns ir.actions.report dict
    5. Empty period returns empty payload (no crash)
    6. Invalid date range raises UserError in report model
    7. _build_base_domain with no filters returns company-only domain
    8. _build_base_domain with warehouse adds location restriction
    9. _build_base_domain with location adds child_of restriction
    10. _build_base_domain with product adds product_id filter
    11. _build_base_domain with category adds categ_id child_of filter
    12. _prefetch_product_data returns dict with expected keys
    13. _prefetch_names returns {id: display_name} dict
    14. _empty_payload returns expected structure
"""

from datetime import date

from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('standard')
class TestStockMovementReportWizard(TransactionCase):
    """Wizard model tests (13 methods — STEP 6 requirement)."""

    def setUp(self):
        """Set up test fixtures."""
        super().setUp()
        self.Wizard = self.env['stock.movement.report.wizard']

    def test_01_wizard_creates_with_required_dates(self):
        """Wizard can be created with date_from and date_to."""
        wiz = self.Wizard.create({
            'date_from': date(2026, 1, 1),
            'date_to': date(2026, 1, 31),
        })
        self.assertEqual(wiz.date_from, date(2026, 1, 1))
        self.assertEqual(wiz.date_to, date(2026, 1, 31))

    def test_02_wizard_rejects_invalid_dates(self):
        """Wizard raises UserError when date_from > date_to."""
        with self.assertRaises(UserError):
            self.Wizard.create({
                'date_from': date(2026, 2, 1),
                'date_to': date(2026, 1, 1),
            })

    def test_03_optional_fields_default_falsy(self):
        """All filter fields default to falsy (no filter)."""
        wiz = self.Wizard.create({
            'date_from': date(2026, 1, 1),
            'date_to': date(2026, 1, 31),
        })
        self.assertFalse(wiz.warehouse_id)
        self.assertFalse(wiz.location_id)
        self.assertFalse(wiz.product_id)
        self.assertFalse(wiz.categ_id)

    def test_04_action_print_pdf_returns_dict(self):
        """Print action returns a report_action dict."""
        wiz = self.Wizard.create({
            'date_from': date(2026, 1, 1),
            'date_to': date(2026, 1, 31),
        })
        result = wiz.action_print_pdf()
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('type'), 'ir.actions.report')


@tagged('standard')
class TestStockMovementReportModel(TransactionCase):
    """Business logic model tests (9 methods)."""

    def setUp(self):
        """Set up test fixtures."""
        super().setUp()
        self.ReportModel = self.env['stock.movement.report']
        self.company = self.env.company

    def test_05_empty_period_returns_empty_payload(self):
        """Calling report with a date range having no movements returns empty products list."""
        payload = self.ReportModel.get_report_data(
            date_from='2099-01-01',
            date_to='2099-01-31',
        )
        self.assertEqual(payload['products'], [])
        self.assertIn('company', payload)
        self.assertIn('date_from', payload)

    def test_06_invalid_date_range_raises_usererror(self):
        """get_report_data raises UserError if date_from > date_to."""
        with self.assertRaises(UserError):
            self.ReportModel.get_report_data(
                date_from='2026-02-01',
                date_to='2026-01-01',
            )

    def test_07_build_base_domain_no_filters(self):
        """_build_base_domain with no filters returns company-only domain."""
        domain = self.ReportModel._build_base_domain(
            self.company, False, False, False, False
        )
        self.assertIn(('company_id', '=', self.company.id), domain)

    def test_08_build_base_domain_with_warehouse(self):
        """_build_base_domain with warehouse adds location restriction."""
        wh = self.env['stock.warehouse'].search([], limit=1)
        if not wh:
            self.skipTest("No warehouse in test DB")
        domain = self.ReportModel._build_base_domain(
            self.company, wh, False, False, False
        )
        # Domain should contain '|', location_id, location_dest_id
        self.assertTrue(any('location_id' in str(d) for d in domain))

    def test_09_build_base_domain_with_location(self):
        """_build_base_domain with location adds child_of restriction."""
        loc = self.env['stock.location'].search([('usage', '=', 'internal')], limit=1)
        if not loc:
            self.skipTest("No internal location in test DB")
        domain = self.ReportModel._build_base_domain(
            self.company, False, loc, False, False
        )
        self.assertTrue(any('child_of' in str(d) for d in domain))

    def test_10_build_base_domain_with_product(self):
        """_build_base_domain with product adds product_id filter."""
        prod = self.env['product.product'].create({'name': 'Test Product'})
        domain = self.ReportModel._build_base_domain(
            self.company, False, False, prod, False
        )
        self.assertIn(('product_id', '=', prod.id), domain)

    def test_11_build_base_domain_with_category(self):
        """_build_base_domain with category adds categ_id child_of filter."""
        categ = self.env['product.category'].search([], limit=1)
        domain = self.ReportModel._build_base_domain(
            self.company, False, False, False, categ
        )
        self.assertTrue(any('categ_id' in str(d) and 'child_of' in str(d) for d in domain))

    def test_12_prefetch_product_data_returns_expected_keys(self):
        """_prefetch_product_data returns dict with expected keys."""
        prod = self.env['product.product'].create({
            'name': 'Test Product',
            'default_code': 'TEST001',
            'standard_price': 100.0,
        })
        result = self.ReportModel._prefetch_product_data(prod)
        self.assertIn(prod.id, result)
        self.assertEqual(result[prod.id]['name'], 'Test Product')
        self.assertEqual(result[prod.id]['code'], 'TEST001')
        self.assertEqual(result[prod.id]['cost'], 100.0)
        self.assertIn('uom_name', result[prod.id])
        self.assertIn('category', result[prod.id])

    def test_13_prefetch_names_returns_id_to_name_dict(self):
        """_prefetch_names returns {id: display_name} dict."""
        prod = self.env['product.product'].create({'name': 'Test'})
        result = self.ReportModel._prefetch_names(prod)
        self.assertEqual(result[prod.id], prod.display_name)

    def test_14_empty_payload_structure(self):
        """_empty_payload returns expected structure."""
        payload = self.ReportModel._empty_payload(
            '2026-01-01', '2026-01-31', False, False, self.company
        )
        self.assertEqual(payload['date_from'], '2026-01-01')
        self.assertEqual(payload['date_to'], '2026-01-31')
        self.assertEqual(payload['products'], [])
        self.assertEqual(payload['company'], self.company)
