from ..models.bank_account import BankAccount
from ..models.product import Product
from ..models.user import User
from ..services.bank_account_service import get_bank_account, debite_from_bank_account
from ..services.product_service import get_products
from django.db.utils import IntegrityError
from django.db import transaction


def validate_purchase_data(user: User, product_id: int, quantity: int):
    bank_account = get_bank_account(user)
    product = get_products(product_id)
    if bank_account.balance <= product.price * quantity:
        raise ValueError('Insufficient funds')
    if product.quantity < quantity:
        raise ValueError('Product out of stock')

def create_purchase_record(user: User, product: Product, quantity: int):
    user.purchased_products.add(product, through_defaults={'quantity': quantity})

def post_purchase(user: User, product_id: int, quantity: int):
    with transaction.atomic():
        product = get_products(product_id)
        validate_purchase_data(user=user, product_id=product_id, quantity=quantity)
        debite_from_bank_account(user=user, amount=product.price * quantity)
        create_purchase_record(user=user, product=product, quantity=quantity)
