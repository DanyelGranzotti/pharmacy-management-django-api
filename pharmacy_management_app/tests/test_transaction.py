from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from ..models.user import User
from ..models.product import Product
from ..models.bank_account import BankAccount
from ..models.suppliers import Suppliers

class PurchaseProductTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass', name='Test User')
        self.bank_account = BankAccount.objects.create(user=self.user, account_number='1234567890', bank_name='Test Bank', branch_code='0001', account_type='Savings', balance=1000.00)
        self.supplier = Suppliers.objects.create(name='Test Supplier', contact_info='test@example.com')
        self.product = Product.objects.create(name='Test Product', description='Test Description', cost_price=80.00, profit_margin=0.25, quantity=10, supplier=self.supplier)
        
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
