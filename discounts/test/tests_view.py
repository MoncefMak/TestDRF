from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from accounts.models import CustomerUser, BrndAdmin
from discounts.models import DiscountCode


class DiscountCodeAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a CustomerUser (Customer)
        customer_user = User.objects.create_user(username='customer_user_test', password='test_password')
        self.customer_user = CustomerUser.objects.create(phone_number='123456789', is_active=True, user=customer_user)

        # Create a BrndAdmin (Brand Admin)
        brand_admin = User.objects.create_user(username='brand_admin_test', password='test_password')
        self.brand_admin = BrndAdmin.objects.create(phone_number='987654321', is_active=True, user=brand_admin)

        # Create a DiscountCode with the BrandAdmin as the creator
        self.discount_code = DiscountCode.objects.create(code='TESTCODE', discount_amount=10,
                                                         created_by=self.brand_admin.user)

    def test_discount_code_list_brand_admin(self):
        url = reverse('discount-code-list')
        self.client.force_authenticate(user=self.brand_admin.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_discount_code_list_customer(self):
        url = reverse('discount-code-list')
        self.client.force_authenticate(user=self.customer_user.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_discount_code_create(self):
        self.client.force_authenticate(user=self.brand_admin.user)
        url = reverse('discount-code-create')
        data = {'discount_amount': 20, 'created_by': self.brand_admin.user.id}  # Provide the created_by field
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DiscountCode.objects.count(), 2)

    def test_discount_code_update(self):
        self.client.force_authenticate(user=self.brand_admin.user)
        url = reverse('discount-code-update', kwargs={'pk': self.discount_code.pk})
        data = {'discount_amount': 15}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.discount_code.refresh_from_db()
        self.assertEqual(self.discount_code.discount_amount, 15)

    def test_consume_discount_code(self):
        self.client.force_authenticate(user=self.customer_user.user)
        url = reverse('consume-discount-code')
        data = {'code': 'TESTCODE'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
