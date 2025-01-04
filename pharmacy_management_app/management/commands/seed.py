from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from pharmacy_management_app.models.bank_account import BankAccount

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        self.create_users()
        self.create_bank_accounts()
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
