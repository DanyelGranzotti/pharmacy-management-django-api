from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from ..models.suppliers import Suppliers
from django.db.models import Q

def create_supplier(data: dict):
    try:
        supplier = Suppliers.objects.create(**data)
    except IntegrityError as e:
        error_message = str(e)
        raise IntegrityError(error_message)
    return supplier

def get_supplier(supplier_id: int):
    try:
        return Suppliers.objects.get(pk=supplier_id)
    except ObjectDoesNotExist as e:
        raise ObjectDoesNotExist("Supplier not found.") from e

def get_all_suppliers(name_contains: str = "", **kwargs) -> list[Suppliers]:
    try:
        query = Q(**kwargs)
        if name_contains:
            query &= Q(name__icontains=name_contains)
        return Suppliers.objects.filter(query)
    except ObjectDoesNotExist as e:
        raise ObjectDoesNotExist("Supplier not found.") from e

def update_supplier(supplier_id: int, data: dict):
    supplier = get_supplier(supplier_id)
    for field, value in data.items():
        setattr(supplier, field, value)
    try:
        supplier.save()
    except IntegrityError as e:
        error_message = str(e)
        raise IntegrityError(error_message)
    return supplier

def delete_supplier(supplier_id: int):
    supplier = get_supplier(supplier_id)
    supplier.delete()
    return supplier
