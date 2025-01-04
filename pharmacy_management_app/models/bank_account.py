from django.db import models
from .user import User

class BankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bank_account')
    account_number = models.CharField(max_length=20, unique=True)
    bank_name = models.CharField(max_length=100)
    branch_code = models.CharField(max_length=10)
    account_type = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} - {self.account_number}"
