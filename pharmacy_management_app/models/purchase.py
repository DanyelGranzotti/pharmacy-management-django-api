from  django.db import models
from ..models.product import Product

class Purchase(models.Model):
    user = models.ForeignKey('pharmacy_management_app.user', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

