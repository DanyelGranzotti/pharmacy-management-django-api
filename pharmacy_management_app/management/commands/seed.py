from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from pharmacy_management_app.models.bank_account import BankAccount
from pharmacy_management_app.models.product import Product
from pharmacy_management_app.models.suppliers import Suppliers

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        self.create_users()
        self.create_bank_accounts()
        self.create_suppliers()
        self.create_products()
        self.stdout.write('Data seeded successfully.')

    def create_users(self):
        users_data = [
            {'email': 'user1@example.com', 'name': 'User One', 'password': 'password123'},
            {'email': 'user2@example.com', 'name': 'User Two', 'password': 'password123'},
            {'email': 'user3@example.com', 'name': 'User Three', 'password': 'password123'},
        ]
        for user_data in users_data:
            user, created = User.objects.get_or_create(email=user_data['email'], defaults=user_data)
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f'Created user: {user.email}')
            else:
                self.stdout.write(f'User already exists: {user.email}')

    def create_bank_accounts(self):
        bank_accounts_data = [
            {'user': User.objects.get(email='user1@example.com'), 'account_number': '1234567890', 'bank_name': 'Bank A', 'branch_code': '001', 'account_type': 'Savings', 'balance': 1000.00},
            {'user': User.objects.get(email='user2@example.com'), 'account_number': '2345678901', 'bank_name': 'Bank B', 'branch_code': '002', 'account_type': 'Checking', 'balance': 2000.00},
            {'user': User.objects.get(email='user3@example.com'), 'account_number': '3456789012', 'bank_name': 'Bank C', 'branch_code': '003', 'account_type': 'Savings', 'balance': 3000.00},
        ]
        for account_data in bank_accounts_data:
            bank_account, created = BankAccount.objects.get_or_create(user=account_data['user'], defaults=account_data)
            if created:
                self.stdout.write(f'Created bank account for user: {account_data["user"].email}')
            else:
                self.stdout.write(f'Bank account already exists for user: {account_data["user"].email}')

    def create_suppliers(self):
        suppliers_data = [
            {'name': 'Supplier 1', 'contact_info': 'Contact info for supplier 1'},
            {'name': 'Supplier 2', 'contact_info': 'Contact info for supplier 2'},
            {'name': 'Supplier 3', 'contact_info': 'Contact info for supplier 3'},
        ]
        for supplier_data in suppliers_data:
            supplier, created = Suppliers.objects.get_or_create(name=supplier_data['name'], defaults=supplier_data)
            if created:
                self.stdout.write(f'Created supplier: {supplier.name}')
            else:
                self.stdout.write(f'Supplier already exists: {supplier.name}')

    def create_products(self):
        supplier1 = Suppliers.objects.get(name='Supplier 1')
        supplier2 = Suppliers.objects.get(name='Supplier 2')
        supplier3 = Suppliers.objects.get(name='Supplier 3')

        products_data = [
            {'name': 'Product 1', 'description': 'Description for product 1', 'cost_price': 5.00, 'profit_margin': 0.5, 'quantity': 100, 'supplier': supplier1},
            {'name': 'Product 2', 'description': 'Description for product 2', 'cost_price': 10.00, 'profit_margin': 0.6, 'quantity': 200, 'supplier': supplier2},
            {'name': 'Product 3', 'description': 'Description for product 3', 'cost_price': 15.00, 'profit_margin': 0.7, 'quantity': 300, 'supplier': supplier3},
        ]
        for product_data in products_data:
            product, created = Product.objects.get_or_create(name=product_data['name'], defaults=product_data)
            if created:
                self.stdout.write(f'Created product: {product.name}')
            else:
                self.stdout.write(f'Product already exists: {product.name}')
