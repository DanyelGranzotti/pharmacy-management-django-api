from ..models import BankAccount, User
from django.db.models import Q

def get_bank_account(user: User):
    try:
        bank_account = BankAccount.objects.get(user=user)
        return bank_account
    except BankAccount.DoesNotExist:
        return None

def debite_from_bank_account(user: User, amount: float):
    try:
        bank_account = get_bank_account(user)
        bank_account.balance -= amount
        bank_account.save()
    except Exception as e:
        print(f"Error occurred while debiting from bank account: {e}")

def get_user_bank_accounts(user: User, bank_name_contains: str = ""):
    query = Q(user=user)
    if bank_name_contains:
        query &= Q(bank_name__icontains=bank_name_contains)
    return BankAccount.objects.filter(query)

def create_bank_account(serializer, user: User):
    serializer.save(user=user)