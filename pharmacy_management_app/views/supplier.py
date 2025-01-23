from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from ..models.suppliers import Suppliers
from ..serializers.supplier import SupplierSerializer
from ..services.suppliers_service import (
    create_supplier,
    get_supplier,
    get_all_suppliers,
    update_supplier,
    delete_supplier
)

class SupplierViewSet(viewsets.ViewSet):
    queryset = Suppliers.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(
        operation_description="Retrieve a list of suppliers",
        responses={200: SupplierSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        suppliers = get_all_suppliers()
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new supplier",
        request_body=SupplierSerializer,
        responses={201: SupplierSerializer}
    )
    def create(self, request, *args, **kwargs):
        supplier = create_supplier(request.data)
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Retrieve a supplier by ID",
        responses={200: SupplierSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        supplier = get_supplier(kwargs['pk'])
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a supplier by ID",
        request_body=SupplierSerializer,
        responses={200: SupplierSerializer}
    )
    def update(self, request, *args, **kwargs):
        supplier = update_supplier(kwargs['pk'], request.data)
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Partially update a supplier by ID",
        request_body=SupplierSerializer,
        responses={200: SupplierSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        supplier = update_supplier(kwargs['pk'], request.data)
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Delete a supplier by ID",
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        delete_supplier(kwargs['pk'])
        return Response(status=status.HTTP_204_NO_CONTENT)
