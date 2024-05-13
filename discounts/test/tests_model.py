# Create your test here.
from django.contrib.auth.models import User
from django.test import TestCase

from discounts.models import DiscountCode, HistoryDiscountCode


class DiscountCodeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.discount_code = DiscountCode.objects.create(
            code='TESTCODE',
            discount_amount=10.00,
            created_by=self.user
        )

    def test_discount_code_creation(self):
        """Test creation of a discount code"""
        self.assertEqual(self.discount_code.code, 'TESTCODE')
        self.assertEqual(self.discount_code.discount_amount, 10.00)
        self.assertEqual(self.discount_code.discount_percentage, None)
        self.assertEqual(self.discount_code.created_by, self.user)
        self.assertTrue(self.discount_code.is_active)

    def test_discount_code_str_method(self):
        """Test the __str__ method of the discount code model"""
        self.assertEqual(str(self.discount_code), 'TESTCODE')


class HistoryDiscountCodeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.discount_code = DiscountCode.objects.create(
            discount_amount=10.00,
            created_by=self.user
        )
        self.history_discount_code = HistoryDiscountCode.objects.create(
            discount_code=self.discount_code,
            consumed_by=self.user
        )

    def test_history_discount_code_creation(self):
        """Test creation of a history discount code"""
        self.assertEqual(self.history_discount_code.discount_code, self.discount_code)
        self.assertEqual(self.history_discount_code.consumed_by, self.user)

    def test_history_discount_code_str_method(self):
        self.assertEqual(str(self.history_discount_code), str(self.discount_code))
