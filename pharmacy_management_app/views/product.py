import csv
import logging
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models.product import Product
from ..serializers.product import ProductSerializer
from ..permissions import IsAdminUser
from ..services.product_service import process_csv
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from ..models.suppliers import Suppliers
logger = logging.getLogger(__name__)

class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductCSVUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(
        operation_description="Upload a CSV file with a list of products",
        manual_parameters=[
            openapi.Parameter(
                'file', openapi.IN_FORM, description="CSV file", type=openapi.TYPE_FILE, required=True
            )
        ],
        responses={
            201: openapi.Response('Products uploaded successfully'),
            400: 'Bad Request',
            500: 'Internal Server Error'
        }
    )
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({'detail': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            products = process_csv(file)
            return Response({'detail': 'Products uploaded successfully.'}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            logger.error(f"Invalid data: {e}")
            return Response({'detail': f"Invalid data: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    pagination_class = ProductPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        return super().get_permissions()

    @swagger_auto_schema(
        operation_description="Retrieve a list of products",
        responses={200: ProductSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new product",
        request_body=ProductSerializer,
        responses={201: ProductSerializer}
    )
    def create(self, request, *args, **kwargs):
        supplier_id = request.data.get('supplier')
        try:
            supplier = Suppliers.objects.get(id=supplier_id)
        except Suppliers.DoesNotExist:
            return Response({'detail': 'Supplier not found.'}, status=status.HTTP_400_BAD_REQUEST)
        request.data['supplier'] = supplier.id
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a product by ID",
        responses={200: ProductSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a product by ID",
        request_body=ProductSerializer,
        responses={200: ProductSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a product by ID",
        request_body=ProductSerializer,
        responses={200: ProductSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a product by ID",
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
