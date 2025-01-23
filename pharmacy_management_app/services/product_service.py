from ..models import Product
from ..serializers.product import ProductSerializer
from ..models.suppliers import Suppliers
import csv
from django.db.models import Q

def get_products(name_contains: str = "", **kwargs) -> list[Product]:
    try:
        query = Q(**kwargs)
        if name_contains:
            query &= Q(name__icontains=name_contains)
        return Product.objects.filter(query)
    except Product.DoesNotExist:
        raise ValueError("Product not found")

# def process_csv(file):
#     decoded_file = file.read().decode('utf-8').splitlines()
#     reader = csv.DictReader(decoded_file)
#     products = []
#     for row in reader:
#         supplier_name = row.get('supplier')
#         if not supplier_name or not supplier_name.strip():
#             raise ValueError("No supplier name provided.")
#         supplier_name = supplier_name.strip()
#         supplier, _ = Suppliers.objects.get_or_create(
#             name__iexact=supplier_name,
#             defaults={'name': supplier_name}
#         )
        
#         row['supplier'] = supplier.id
#         if 'cost_price' in row:
#             row['cost_price'] = float(row['cost_price'])
#         if 'profit_margin' in row:
#             row['profit_margin'] = float(row['profit_margin'])
#         serializer = ProductSerializer(data=row)
#         if serializer.is_valid():
#             products.append(serializer.save())
#         else:
#             raise ValueError(f"Invalid data: {serializer.errors}")
#     return products