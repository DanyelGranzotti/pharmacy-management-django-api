from rest_framework import serializers
from ..models.suppliers import Suppliers

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = ['id', 'name', 'contact_info', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        ref_name = 'SupplierSerializer'
