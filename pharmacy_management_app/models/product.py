from django.db import models
from ..models.suppliers import Suppliers

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2, default=0.20) 
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE, related_name='products')

    @property
    def price(self):
        return self.cost_price * (1 + self.profit_margin)

    def __str__(self):
        return self.name
