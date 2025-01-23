from django.test import TestCase
from django.contrib.auth import get_user_model
from pharmacy_management_app.serializers.user import UserSerializer, RegisterSerializer
from pharmacy_management_app.serializers.bank_account import BankAccountSerializer
from pharmacy_management_app.models.bank_account import BankAccount
from pharmacy_management_app.models.suppliers import Suppliers

User = get_user_model()

class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='password123', name='Test User')

class UserSerializerTest(BaseTestCase):
    def test_user_serializer(self):
        serializer = UserSerializer(self.user)
        data = serializer.data
        self.assertEqual(data['email'], 'testuser@example.com')
        self.assertEqual(data['name'], 'Test User')

class RegisterSerializerTest(TestCase):
    def test_register_serializer(self):
        data = {'email': 'newuser@example.com', 'name': 'New User', 'password': 'Str0ngP@ssw0rd!', 'password2': 'Str0ngP@ssw0rd!'}
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)
        user = serializer.save()
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertTrue(user.check_password('Str0ngP@ssw0rd!'))

class BankAccountSerializerTest(BaseTestCase):
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

    def test_bank_account_serializer(self):
        serializer = BankAccountSerializer(self.bank_account)
        data = serializer.data
        self.assertEqual(data['account_number'], '1234567890')
        self.assertEqual(data['bank_name'], 'Test Bank')
        self.assertEqual(data['branch_code'], '001')
        self.assertEqual(data['account_type'], 'Savings')
        self.assertEqual(data['balance'], '1000.00')
