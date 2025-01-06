from rest_framework import serializers
from ..models.product import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'cost_price', 'profit_margin', 'price', 'quantity', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        ref_name = 'ProductSerializer'
