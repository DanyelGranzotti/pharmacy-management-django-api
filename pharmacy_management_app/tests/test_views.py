from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from pharmacy_management_app.models.bank_account import BankAccount
from pharmacy_management_app.models.suppliers import Suppliers

User = get_user_model()

class BaseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='password123', name='Test User')
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

class UserViewSetTest(BaseTestCase):
    def test_create_user(self):
        url = reverse('user-list')
        data = {'email': 'newuser@example.com', 'name': 'New User', 'password': 'password123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_user(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class BankAccountViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.supplier = Suppliers.objects.create(name='Test Supplier', contact_info='test@example.com')
        self.bank_account = BankAccount.objects.create(
            user=self.user,
            account_number='1234567890',
            bank_name='Test Bank',
            branch_code='001',
            account_type='Savings',
            balance=1000.00
        )

    def test_create_bank_account(self):
        url = reverse('bankaccount-list')
        data = {
            'account_number': '2345678901',
            'bank_name': 'New Bank',
            'branch_code': '002',
            'account_type': 'Checking',
            'balance': 2000.00
        }
        BankAccount.objects.filter(user=self.user).delete()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_bank_account(self):
        url = reverse('bankaccount-detail', args=[self.bank_account.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
