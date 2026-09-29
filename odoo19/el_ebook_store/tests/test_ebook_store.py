from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestEbookStore(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ProductTemplate = cls.env['product.template']
        cls.EbookCode = cls.env['ebook.code']
        cls.EbookLibrary = cls.env['ebook.library']
        cls.Partner = cls.env['res.partner']

        cls.partner = cls.Partner.create({'name': 'Test Customer', 'email': 'test@test.com'})
        cls.ebook = cls.ProductTemplate.create({
            'name': 'Test E-Book',
            'is_ebook': True,
            'ebook_author': 'Test Author',
            'ebook_pages': 200,
            'ebook_access_type': 'both',
            'list_price': 19.99,
            'type': 'consu',
        })

    def test_01_product_ebook_fields(self):
        self.assertTrue(self.ebook.is_ebook)
        self.assertEqual(self.ebook.ebook_access_type, 'both')

    def test_02_generate_random_codes(self):
        codes = self.EbookCode.generate_codes(self.ebook.id, 5, generation_mode='auto')
        self.assertEqual(len(codes), 5)
        for code in codes:
            self.assertTrue(code.name.startswith('EBK-'))
            self.assertEqual(code.state, 'available')

    def test_03_generate_manual_codes(self):
        manual = ['CODE-001', 'CODE-002', 'CODE-003']
        codes = self.EbookCode.generate_codes(self.ebook.id, 3, generation_mode='manual', manual_codes=manual)
        self.assertEqual(len(codes), 3)

    def test_04_code_uniqueness(self):
        c1 = self.EbookCode.generate_codes(self.ebook.id, 1, generation_mode='auto')[0]
        c2 = self.EbookCode.generate_codes(self.ebook.id, 1, generation_mode='auto')[0]
        self.assertNotEqual(c1.name, c2.name)

    def test_05_assign_and_expire(self):
        """Code is assigned and immediately expired — one-time use."""
        code = self.EbookCode.generate_codes(self.ebook.id, 1, generation_mode='auto')[0]
        result = code.action_assign_and_expire(self.partner.id, False)
        self.assertTrue(result)
        self.assertEqual(code.state, 'expired')
        self.assertEqual(code.partner_id, self.partner)

    def test_06_expired_code_cannot_be_reused(self):
        """An expired code can never be assigned again."""
        code = self.EbookCode.generate_codes(self.ebook.id, 1, generation_mode='auto')[0]
        code.action_assign_and_expire(self.partner.id, False)
        # Try to assign to another customer
        partner2 = self.Partner.create({'name': 'Customer 2'})
        result = code.action_assign_and_expire(partner2.id, False)
        self.assertFalse(result)  # should fail — code is expired

    def test_07_code_stats(self):
        self.EbookCode.generate_codes(self.ebook.id, 10, generation_mode='auto')
        self.assertEqual(self.ebook.ebook_total_codes, 10)
        self.assertEqual(self.ebook.ebook_codes_available, 10)

    def test_08_library_accessible_after_purchase(self):
        """Library entry is 'accessible' — customer can open the book anytime."""
        code = self.EbookCode.generate_codes(self.ebook.id, 1, generation_mode='auto')[0]
        code.action_assign_and_expire(self.partner.id, False)
        library = self.EbookLibrary.create({
            'partner_id': self.partner.id,
            'product_tmpl_id': self.ebook.id,
            'code_id': code.id,
            'state': 'accessible',
        })
        self.assertEqual(library.state, 'accessible')

    def test_09_library_permanent_access(self):
        """Library stays accessible — code expiry doesn't affect library."""
        code = self.EbookCode.generate_codes(self.ebook.id, 1, generation_mode='auto')[0]
        code.action_assign_and_expire(self.partner.id, False)
        library = self.EbookLibrary.create({
            'partner_id': self.partner.id,
            'product_tmpl_id': self.ebook.id,
            'code_id': code.id,
            'state': 'accessible',
        })
        # Code is expired but library is still accessible
        self.assertEqual(code.state, 'expired')
        self.assertEqual(library.state, 'accessible')

    def test_10_access_log_created(self):
        code = self.EbookCode.generate_codes(self.ebook.id, 1, generation_mode='auto')[0]
        code.action_assign_and_expire(self.partner.id, False)
        library = self.EbookLibrary.create({
            'partner_id': self.partner.id,
            'product_tmpl_id': self.ebook.id,
            'code_id': code.id,
        })
        log = self.env['ebook.access.log'].create({
            'library_id': library.id,
            'partner_id': self.partner.id,
            'product_tmpl_id': self.ebook.id,
        })
        self.assertTrue(log.id)

    def test_11_reset_code(self):
        code = self.EbookCode.generate_codes(self.ebook.id, 1, generation_mode='auto')[0]
        code.action_assign_and_expire(self.partner.id, False)
        code.action_reset()
        self.assertEqual(code.state, 'available')

    def test_12_each_customer_gets_different_code(self):
        """Two different customers get two different codes."""
        codes = self.EbookCode.generate_codes(self.ebook.id, 2, generation_mode='auto')
        partner2 = self.Partner.create({'name': 'Customer 2'})
        codes[0].action_assign_and_expire(self.partner.id, False)
        codes[1].action_assign_and_expire(partner2.id, False)
        self.assertNotEqual(codes[0].name, codes[1].name)
        self.assertEqual(codes[0].partner_id, self.partner)
        self.assertEqual(codes[1].partner_id, partner2)

    def test_13_expire_code_directly(self):
        code = self.EbookCode.generate_codes(self.ebook.id, 1, generation_mode='auto')[0]
        code.action_expire()
        self.assertEqual(code.state, 'expired')
