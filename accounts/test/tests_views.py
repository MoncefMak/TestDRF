from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import BrndAdmin, CustomerUser


class AccountsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # brnd_admin_data for BrndAdmin
        self.brnd_admin_data = {
            "phone_number": "1234567890",
            "user": {
                "username": "brndadmin",
                "password": "password123"
            }
        }
        self.brnd_admin_login_data = {
            "username": "brndadmin",
            "password": "password123"
        }

        self.customer_user_data = {
            "phone_number": "9876543210",
            "user": {
                "username": "customeruser",
                "password": "password456"
            }
        }
        self.customer_user_login_data = {
            "username": "customeruser",
            "password": "password456"
        }

    def test_brnd_admin_registration(self):
        url = reverse('brnd_admin_registration')
        response = self.client.post(url, self.brnd_admin_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BrndAdmin.objects.count(), 1)  # Since we already created one in setUp

    def test_customer_user_registration(self):
        url = reverse('customer_user_registration')
        response = self.client.post(url, self.customer_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomerUser.objects.count(), 1)  # Since we already created one in setUp

    def test_login_customer(self):
        url = reverse('login')
        CustomerUser.objects.create(phone_number=self.customer_user_data["phone_number"],
                                    user=User.objects.create_user(**self.customer_user_data["user"]))

        response = self.client.post(url, self.customer_user_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_brand(self):
        url = reverse('login')
        BrndAdmin.objects.create(phone_number=self.brnd_admin_data["phone_number"],
                                 user=User.objects.create_user(**self.brnd_admin_data["user"]))
        response = self.client.post(url, self.brnd_admin_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        CustomerUser.objects.create(phone_number=self.customer_user_data["phone_number"],
                                    user=User.objects.create_user(**self.customer_user_data["user"]))
        # Assuming you have a refresh token
        refresh_token = self.client.post(reverse('login'), self.customer_user_login_data, format='json').data['refresh']
        url = reverse('token_refresh')
        response = self.client.post(url, {'refresh': refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
