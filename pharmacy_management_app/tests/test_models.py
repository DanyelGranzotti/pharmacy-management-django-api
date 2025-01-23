from django.test import TestCase
from django.contrib.auth import get_user_model
from pharmacy_management_app.models.bank_account import BankAccount
from pharmacy_management_app.models.suppliers import Suppliers

User = get_user_model()

class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='password123', name='Test User')

class UserModelTest(BaseTestCase):
    def test_user_creation(self):
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('password123'))
        self.assertEqual(self.user.name, 'Test User')

class BankAccountModelTest(BaseTestCase):
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

    def test_bank_account_creation(self):
        self.assertEqual(self.bank_account.user, self.user)
        self.assertEqual(self.bank_account.account_number, '1234567890')
        self.assertEqual(self.bank_account.bank_name, 'Test Bank')
        self.assertEqual(self.bank_account.branch_code, '001')
        self.assertEqual(self.bank_account.account_type, 'Savings')
        self.assertEqual(self.bank_account.balance, 1000.00)
