from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from ..models.user import User
from ..models.product import Product
from ..models.bank_account import BankAccount

class PurchaseProductTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass', name='Test User')
        self.bank_account = BankAccount.objects.create(user=self.user, account_number='1234567890', bank_name='Test Bank', branch_code='0001', account_type='Savings', balance=1000.00)
        self.product = Product.objects.create(name='Test Product', description='Test Description', cost_price=80.00, profit_margin=0.25, quantity=10)
        
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_purchase_product_success(self):
        url = reverse('purchase-product')
        data = {'product_id': self.product.id, 'quantity': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.bank_account.refresh_from_db()
        self.assertEqual(self.bank_account.balance, 800.00)

    def test_purchase_product_insufficient_balance(self):
        self.bank_account.balance = 100.00
        self.bank_account.save()
        url = reverse('purchase-product')
        data = {'product_id': self.product.id, 'quantity': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Insufficient balance')

    def test_purchase_product_not_found(self):
        url = reverse('purchase-product')
        data = {'product_id': 999, 'quantity': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Product not found')
