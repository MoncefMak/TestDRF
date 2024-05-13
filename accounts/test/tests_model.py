# Create your test here.
from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import BaseUser, CustomerUser, BrndAdmin


class CustomerUserTestCase(TestCase):
    def test_customer_user_creation(self):
        """Test creation of a customer user"""
        user = User.objects.create(username='customer_user')
        customer_user = CustomerUser.objects.create(
            phone_number='987654321',
            user=user
        )
        self.assertEqual(customer_user.phone_number, '987654321')
        self.assertEqual(customer_user.user, user)
        self.assertTrue(customer_user.is_active)


class BrndAdminTestCase(TestCase):
    def test_brnd_admin_creation(self):
        """Test creation of a brand admin"""
        user = User.objects.create(username='brand_admin')
        brnd_admin = BrndAdmin.objects.create(
            phone_number='456789012',
            user=user
        )
        self.assertEqual(brnd_admin.phone_number, '456789012')
        self.assertEqual(brnd_admin.user, user)
        self.assertTrue(brnd_admin.is_active)
