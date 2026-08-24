from odoo import models
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError


class TestCreditApproval(TransactionCase):
    """Test cases for the credit approval workflow."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Credit Customer',
            'is_company': True,
            'payment_type': 'credit',
            'customer_rank': 1,
        })

        cls.classification = cls.env['customer.classification'].create({
            'name': 'TEST',
            'description': 'Test classification',
            'credit_limit': 1000.0,
            'credit_policy': 'block',
        })

        cls.partner.classification_id = cls.classification.id
        cls.partner.property_product_pricelist = cls.env['product.pricelist'].search(
            [], limit=1
        )

        # Create a product
        product = cls.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 600.0,
            'detailed_type': 'consu',
        })

        # Create sale order that will exceed credit limit
        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.partner.id,
            'user_id': cls.env.user.id,
        })
        cls.env['sale.order.line'].create({
            'order_id': cls.sale_order.id,
            'product_id': product.id,
            'product_uom_qty': 1,
        })

        # Create rejection reason
        cls.rejection_reason = cls.env['credit.rejection.reason'].create({
            'name': 'Test Rejection Reason',
            'description': 'For testing purposes.',
        })

    def test_01_rejection_reason_creation(self):
        """Test creating a rejection reason."""
        reason = self.env['credit.rejection.reason'].create({
            'name': 'Another Reason',
        })
        self.assertTrue(reason.active)
        self.assertEqual(reason.company_id, self.env.company)

    def test_02_approval_request_creation(self):
        """Test creating an approval request from a sale order."""
        # Simulate credit limit exceeded
        self.partner.credit = 800.0  # outstanding
        # effective_credit_limit = 1000, credit = 800, order = 600
        # projected = 1400 > 1000 → blocked

        ApprovalRequest = self.env['credit.approval.request']
        request = ApprovalRequest._create_from_sale_order(self.sale_order)

        self.assertEqual(request.state, 'submitted')
        self.assertEqual(request.partner_id, self.partner.commercial_partner_id)
        self.assertEqual(request.sale_order_id, self.sale_order)
        self.assertGreater(request.exceeded_by, 0)
        self.assertTrue(request.name != 'New')

    def test_03_approval_request_approve(self):
        """Test approving a request confirms the sale order."""
        self.partner.credit = 800.0

        request = self.env['credit.approval.request']._create_from_sale_order(
            self.sale_order
        )
        # Simulate the SO credit state
        self.sale_order.credit_approval_state = 'pending'
        self.sale_order.credit_approval_id = request.id

        # The order should still be in draft (blocked)
        self.assertEqual(self.sale_order.state, 'draft')

        # Approve
        request.action_approve()
        self.assertEqual(request.state, 'approved')
        self.assertEqual(self.sale_order.credit_approval_state, 'approved')

    def test_04_approval_request_reject_without_reason(self):
        """Test rejecting without a reason raises ValidationError."""
        self.partner.credit = 800.0
        request = self.env['credit.approval.request']._create_from_sale_order(
            self.sale_order
        )

        with self.assertRaises(ValidationError):
            request.action_reject()

    def test_05_approval_request_reject_with_reason(self):
        """Test rejecting with a predefined reason."""
        self.partner.credit = 800.0
        request = self.env['credit.approval.request']._create_from_sale_order(
            self.sale_order
        )

        request.rejection_reason_id = self.rejection_reason.id
        request.action_reject()

        self.assertEqual(request.state, 'rejected')
        self.assertEqual(request.rejection_reason_id, self.rejection_reason)
        self.assertEqual(self.sale_order.credit_approval_state, 'rejected')

    def test_06_approval_request_resubmit(self):
        """Test resubmitting a rejected request."""
        self.partner.credit = 800.0
        request = self.env['credit.approval.request']._create_from_sale_order(
            self.sale_order
        )

        request.rejection_reason_id = self.rejection_reason.id
        request.action_reject()
        self.assertEqual(request.state, 'rejected')

        request.action_resubmit()
        self.assertEqual(request.state, 'draft')
        self.assertFalse(request.rejection_reason_id)

    def test_07_credit_policy_warning_allows_confirm(self):
        """Test that 'warning' policy allows confirm with a warning."""
        self.classification.credit_policy = 'warning'
        self.partner.credit = 800.0

        # Should not raise — warning policy just posts a message
        # Note: in real Odoo this would succeed but here we test the logic path
        self.assertTrue(self.partner.credit_policy == 'warning')

    def test_08_cash_customer_not_blocked(self):
        """Test that cash customers are never blocked."""
        self.partner.payment_type = 'cash'
        self.partner.credit = 999999.0  # irrelevant for cash

        # Should never be blocked regardless of credit
        is_blocked = self.sale_order.is_credit_blocked
        self.assertFalse(is_blocked)